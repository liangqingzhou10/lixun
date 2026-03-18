#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2025 DeepTouch - 瞬恒智能科技（北京）有限公司
Author: max
Time: 2025-09-25
All rights reserved.

This software is proprietary and confidential. Unauthorized copying,
distribution, or use of this software, via any medium, is strictly prohibited.
"""
"""
ROS2 Humble: TCP接收VR帧 -> 接收线程滤波(left/right/head)；发布线程按频率发布：
- /vr/left_pose、/vr/right_pose、/vr/head_pose (PoseStamped)  [QoS: 参数 pose_qos_reliability]
- /vr/world_pose (PoseStamped, 恒等；可关)                        [同QoS]
- /teleoperation/left_device、/teleoperation/right_device (deeptouch_interface/TeleOptDevice) [BEST_EFFORT]
- TF: frame_id(默认 vr_world) -> (vr_left_hand, vr_right_hand, vr_head) 动态
- 可选静态TF: static_parent_frame -> frame_id
四元数采用几何一致滤波（slerp_ema 或 so3_log）。
"""

import math
import socket
import struct
import threading
import time
from dataclasses import dataclass
from typing import Optional, Dict, List

# ---------- ROS2 ----------
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy
from rcl_interfaces.msg import SetParametersResult
from geometry_msgs.msg import PoseStamped, Pose, TransformStamped
from std_msgs.msg import Header
from tf2_ros import TransformBroadcaster, StaticTransformBroadcaster

# 自定义消息
from deeptouch_interface.msg import TeleOptDevice, HandTouch

# ---------- 位置滤波器（沿用 OneEuro） ----------
from utils.filter import SO3LogLPFQuat, SlerpEMAQuat, OneEuroFilterVector3D



# --------------------- 协议与数据结构 ---------------------

@dataclass
class HandState:
    one: int = 0
    two: int = 0
    three: int = 0
    four: int = 0
    menu: int = 0
    primary_thumb: int = 0
    hand_trigger: float = 0.0
    index_trigger: float = 0.0
    thumbstick_x: float = 0.0
    thumbstick_y: float = 0.0


@dataclass
class PoseData:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    qw: float = 1.0
    qx: float = 0.0
    qy: float = 0.0
    qz: float = 0.0


@dataclass
class VrFrame:
    timestamp: float = 0.0
    left_hand_state: HandState = None
    right_hand_state: HandState = None
    left_hand_pose: PoseData = None
    right_hand_pose: PoseData = None
    head_pose: PoseData = None
    checksum: int = 0


class VrDataReceiver:
    PACKET_FORMAT = '=d6B4f6B4f7f7f7fI'
    PACKET_SIZE = struct.calcsize(PACKET_FORMAT)
    @staticmethod
    def _checksum(data: bytes) -> int:
        c = 0
        for b in data:
            c = ((c << 1) | (c >> 31)) ^ b
            c &= 0xFFFFFFFF
        return c
    def parse(self, data: bytes) -> Optional[VrFrame]:
        if len(data) != self.PACKET_SIZE:
            return None
        vals = struct.unpack(self.PACKET_FORMAT, data)
        ts = vals[0]
        ls = HandState(
            one=vals[1], two=vals[2], three=vals[3], four=vals[4],
            menu=vals[5], primary_thumb=vals[6],
            hand_trigger=vals[7], index_trigger=vals[8],
            thumbstick_x=vals[9], thumbstick_y=vals[10]
        )
        rs = HandState(
            one=vals[11], two=vals[12], three=vals[13], four=vals[14],
            menu=vals[15], primary_thumb=vals[16],
            hand_trigger=vals[17], index_trigger=vals[18],
            thumbstick_x=vals[19], thumbstick_y=vals[20]
        )
        lp = PoseData(x=vals[21], y=vals[22], z=vals[23], qw=vals[24], qx=vals[25], qy=vals[26], qz=vals[27])
        rp = PoseData(x=vals[28], y=vals[29], z=vals[30], qw=vals[31], qx=vals[32], qy=vals[33], qz=vals[34])
        hp = PoseData(x=vals[35], y=vals[36], z=vals[37], qw=vals[38], qx=vals[39], qy=vals[40], qz=vals[41])
        ck = vals[42]
        if self._checksum(data[:-4]) != ck:
            return None
        return VrFrame(ts, ls, rs, lp, rp, hp, ck)


# --------------------- 工具函数 ---------------------

def recv_exact(sock: socket.socket, n: int, timeout_s: float) -> Optional[bytes]:
    sock.settimeout(timeout_s)
    buf = bytearray()
    while len(buf) < n:
        try:
            chunk = sock.recv(n - len(buf))
            if not chunk:
                return None
            buf.extend(chunk)
        except (socket.timeout, socket.error):
            return None
    return bytes(buf)

def to_pose_msg(p: PoseData) -> Pose:
    msg = Pose()
    msg.position.x = p.x; msg.position.y = p.y; msg.position.z = p.z
    msg.orientation.x = p.qx; msg.orientation.y = p.qy
    msg.orientation.z = p.qz; msg.orientation.w = p.qw
    return msg

def _reliability_from_str(s: str) -> QoSReliabilityPolicy:
    s = (s or "").strip().lower()
    return QoSReliabilityPolicy.RELIABLE if s in ("reliable", "r", "reliability") else QoSReliabilityPolicy.BEST_EFFORT


# --------------------- 共享状态 ---------------------

class SharedState:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest: Dict[str, Optional[object]] = {
            "timestamp": 0.0,
            "frame_id": 0,
            "left": None,           # PoseData (filtered)
            "right": None,          # PoseData (filtered)
            "head": None,           # PoseData (filtered)
            "left_state": None,     # HandState (raw)
            "right_state": None,    # HandState (raw)
            "src_fps": 60.0,
        }
    def update(self, **kwargs):
        with self.lock:
            self.latest.update(kwargs)
    def bump_frame(self):
        with self.lock:
            self.latest["frame_id"] = (int(self.latest["frame_id"]) + 1) & 0xFFFFFFFF
    def snapshot(self) -> Dict:
        with self.lock:
            return dict(self.latest)


# --------------------- 接收线程 ---------------------

class ReceiverThread(threading.Thread):
    def __init__(self, host: str, port: int, state: SharedState,
                 min_cutoff: float, beta: float, d_cutoff: float, freq: float,
                 quat_filter_mode: str, quat_cutoff: float):
        super().__init__(daemon=True)
        self.host = host; self.port = port; self.state = state
        self.stop_event = threading.Event()
        self.rx = VrDataReceiver()
        # 位置滤波
        self.pos_filters = {
            "left":  OneEuroFilterVector3D(freq, min_cutoff, beta, d_cutoff),
            "right": OneEuroFilterVector3D(freq, min_cutoff, beta, d_cutoff),
            "head":  OneEuroFilterVector3D(freq, min_cutoff, beta, d_cutoff),
        }
        # 姿态滤波
        self.quat_filters = {
            "left":  self._make_quat_filter(quat_filter_mode, freq, quat_cutoff),
            "right": self._make_quat_filter(quat_filter_mode, freq, quat_cutoff),
            "head":  self._make_quat_filter(quat_filter_mode, freq, quat_cutoff),
        }

    @staticmethod
    def _make_quat_filter(mode: str, freq: float, cutoff: float):
        mode = (mode or "slerp_ema").lower()
        if mode == "so3_log": return SO3LogLPFQuat(freq_hz=freq, cutoff_hz=cutoff)
        return SlerpEMAQuat(freq_hz=freq, cutoff_hz=cutoff)

    def stop(self): self.stop_event.set()

    def _set_filters_freq(self, freq: float):
        for f in self.pos_filters.values(): f.set_freq(freq)
        for f in self.quat_filters.values(): f.set_freq(freq)

    def set_quat_params(self, cutoff_hz: float):
        for f in self.quat_filters.values(): f.set_params(cutoff_hz=cutoff_hz)

    def set_pos_params(self, min_cutoff: float, beta: float, d_cutoff: float):
        for f in self.pos_filters.values(): f.set_params(min_cutoff=min_cutoff, beta=beta, d_cutoff=d_cutoff)

    def run(self):
        backoff = 1.0
        while not self.stop_event.is_set():
            try:
                srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                srv.bind((self.host, self.port)); srv.listen(1); srv.settimeout(1.0)
                while not self.stop_event.is_set():
                    try:
                        conn, _ = srv.accept()
                        conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        self._handle_conn(conn)
                    except socket.timeout:
                        continue
                    finally:
                        if self.stop_event.is_set(): break
                srv.close()
            except Exception:
                time.sleep(backoff); backoff = min(backoff * 2.0, 5.0)

    def _handle_conn(self, conn: socket.socket):
        ema_fps = 60.0; alpha = 0.1; last_ts = None
        while not self.stop_event.is_set():
            data = recv_exact(conn, self.rx.PACKET_SIZE, timeout_s=2.0)
            if not data: break
            frame = self.rx.parse(data)
            if not frame: continue

            if last_ts is not None and frame.timestamp > last_ts:
                inst_fps = 1.0 / (frame.timestamp - last_ts)
                ema_fps = (1 - alpha) * ema_fps + alpha * inst_fps
                self._set_filters_freq(max(ema_fps, 1.0))
            last_ts = frame.timestamp

            filtered: Dict[str, PoseData] = {}
            for key, pose in (("left", frame.left_hand_pose),
                              ("right", frame.right_hand_pose),
                              ("head", frame.head_pose)):
                if pose is None: continue
                fp = self.pos_filters[key].filter([pose.x, pose.y, pose.z], frame.timestamp)
                fq = self.quat_filters[key].filter([pose.qw, pose.qx, pose.qy, pose.qz], frame.timestamp)
                if fp and fq:
                    filtered[key] = PoseData(x=fp[0], y=fp[1], z=fp[2], qw=fq[0], qx=fq[1], qy=fq[2], qz=fq[3])

            self.state.update(
                timestamp=frame.timestamp,
                left=filtered.get("left"),
                right=filtered.get("right"),
                head=filtered.get("head"),
                left_state=frame.left_hand_state,
                right_state=frame.right_hand_state,
                src_fps=ema_fps,
            )
            self.state.bump_frame()

        try: conn.close()
        except Exception: pass


# --------------------- 发布线程（Pose + TeleOptDevice + TF） ---------------------

class PublisherThread(threading.Thread):
    def __init__(self, node: Node, state: SharedState,
                 publish_freq: float, world_frame: str,
                 left_frame: str, right_frame: str,
                 head_frame: str,
                 static_parent_frame: str = "",
                 pose_qos_reliability: str = "reliable",
                 publish_world_pose: bool = True):
        super().__init__(daemon=True)
        self.node = node; self.state = state; self.stop_event = threading.Event()
        self.rate_hz = publish_freq
        self.world_frame = world_frame
        self.left_frame = left_frame
        self.right_frame = right_frame
        self.head_frame = head_frame
        self.publish_world_pose = publish_world_pose

        pose_qos = QoSProfile(
            reliability=_reliability_from_str(pose_qos_reliability),
            history=QoSHistoryPolicy.KEEP_LAST, depth=2
        )
        dev_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST, depth=2
        )

        self.pub_left_pose  = node.create_publisher(PoseStamped, "/vr/left_pose",  pose_qos)
        self.pub_right_pose = node.create_publisher(PoseStamped, "/vr/right_pose", pose_qos)
        self.pub_head_pose  = node.create_publisher(PoseStamped, "/vr/head_pose",  pose_qos)
        self.pub_world_pose = node.create_publisher(PoseStamped, "/vr/world_pose", pose_qos) if publish_world_pose else None
        self.pub_left_dev   = node.create_publisher(TeleOptDevice, "/teleoperation/left_device",  dev_qos)
        self.pub_right_dev  = node.create_publisher(TeleOptDevice, "/teleoperation/right_device", dev_qos)

        self.tf_broadcaster = TransformBroadcaster(self.node)
        self.static_parent_frame = static_parent_frame
        if self.static_parent_frame:
            self.static_broadcaster = StaticTransformBroadcaster(self.node)
            t = TransformStamped()
            t.header.stamp = self.node.get_clock().now().to_msg()
            t.header.frame_id = self.static_parent_frame
            t.child_frame_id = self.world_frame
            t.transform.translation.x = 0.0
            t.transform.translation.y = 0.0
            t.transform.translation.z = 0.0
            t.transform.rotation.x = 0.0
            t.transform.rotation.y = 0.0
            t.transform.rotation.z = 0.0
            t.transform.rotation.w = 1.0
            self.static_broadcaster.sendTransform(t)

    def stop(self): self.stop_event.set()

    def _make_touch(self, hs: HandState) -> HandTouch:
        t = HandTouch()
        t.one = int(hs.one); t.two = int(hs.two); t.three = int(hs.three); t.four = int(hs.four)
        t.menu = int(hs.menu); t.primary_thumb = int(hs.primary_thumb)
        t.hand_trigger = float(hs.hand_trigger); t.index_trigger = float(hs.index_trigger)
        t.thumbstick_x = float(hs.thumbstick_x); t.thumbstick_y = float(hs.thumbstick_y)
        return t

    def _publish_tf(self, stamp, pose: PoseData, child_frame: str):
        t = TransformStamped()
        t.header.stamp = stamp
        t.header.frame_id = self.world_frame
        t.child_frame_id = child_frame
        t.transform.translation.x = pose.x
        t.transform.translation.y = pose.y
        t.transform.translation.z = pose.z
        t.transform.rotation.x = pose.qx
        t.transform.rotation.y = pose.qy
        t.transform.rotation.z = pose.qz
        t.transform.rotation.w = pose.qw
        self.tf_broadcaster.sendTransform(t)

    def _publish_pose_stamped(self, pub, stamp, pose: PoseData):
        msg = PoseStamped()
        msg.header = Header(stamp=stamp, frame_id=self.world_frame)
        msg.pose = to_pose_msg(pose)
        pub.publish(msg)

    # def _transform(left: PoseData, right: PoseData, hand: PoseData):

    def run(self):
        period = 1.0 / max(self.rate_hz, 1e-3)
        next_t = time.monotonic()   
        while rclpy.ok() and not self.stop_event.is_set():
            snap = self.state.snapshot()
            stamp = self.node.get_clock().now().to_msg()

            left_pose:  Optional[PoseData] = snap.get("left")
            right_pose: Optional[PoseData] = snap.get("right")
            head_pose:  Optional[PoseData] = snap.get("head")

            # PoseStamped
            if left_pose  is not None:  self._publish_pose_stamped(self.pub_left_pose,  stamp, left_pose)
            if right_pose is not None:  self._publish_pose_stamped(self.pub_right_pose, stamp, right_pose)
            if head_pose  is not None:  self._publish_pose_stamped(self.pub_head_pose,  stamp, head_pose)

            # 可选世界原点 Pose（恒等）
            if self.publish_world_pose and self.pub_world_pose is not None:
                world_identity = PoseData()
                self._publish_pose_stamped(self.pub_world_pose, stamp, world_identity)

            # TeleOptDevice
            frame_id_val = int(snap.get("frame_id", 0))
            ts_val = float(snap.get("timestamp", 0.0))
            left_state: Optional[HandState]  = snap.get("left_state")
            right_state: Optional[HandState] = snap.get("right_state")
            head_pose:  Optional[PoseData] = snap.get("head")

            # 注意：只有在对应的 pose 存在时才发布 device，避免下游收到“旧 pose + 新 hand_touch”的错位
            if left_state is not None and left_pose is not None and head_pose is not None:
                ld = TeleOptDevice()
                ld.timestamp = ts_val; ld.frame_id = frame_id_val; ld.hand_touch = self._make_touch(left_state)
                ld.hand_pose = to_pose_msg(left_pose)
                ld.head_pose = to_pose_msg(head_pose)
                self.pub_left_dev.publish(ld)

            if right_state is not None and right_pose is not None and head_pose is not None:
                rd = TeleOptDevice()
                rd.timestamp = ts_val; rd.frame_id = frame_id_val; rd.hand_touch = self._make_touch(right_state)
                rd.hand_pose = to_pose_msg(right_pose)
                rd.head_pose = to_pose_msg(head_pose)
                self.pub_right_dev.publish(rd)

            
            # TF
            if left_pose  is not None: self._publish_tf(stamp, left_pose,  self.left_frame)
            if right_pose is not None: self._publish_tf(stamp, right_pose, self.right_frame)
            if head_pose  is not None: self._publish_tf(stamp, head_pose,  self.head_frame)

            # 固定周期对齐：尽量避免超周期时“连环 sleep”
            next_t += period
            now = time.monotonic()
            if next_t - now > 0:
                time.sleep(next_t - now)
            else:
                # 掉队了：直接把 next_t 追到当前，避免“补觉”
                next_t = now

# --------------------- ROS2 节点 ---------------------

class VrRos2Bridge(Node):
    def __init__(self):
        super().__init__("vr_ros_bridge")

        # 基础
        self.declare_parameter("host", "0.0.0.0")
        self.declare_parameter("port", 9001)
        self.declare_parameter("receiv_freq", 120.0)
        self.declare_parameter("publish_freq", 120.0)

        # 坐标系/TF
        self.declare_parameter("frame_id", "vr_world")
        self.declare_parameter("left_frame_id", "vr_left_hand")
        self.declare_parameter("right_frame_id", "vr_right_hand")
        self.declare_parameter("head_frame_id", "vr_head")
        self.declare_parameter("static_parent_frame", "")
        self.declare_parameter("publish_world_pose", True)

        # QoS
        self.declare_parameter("pose_qos_reliability", "reliable")

        # 位置滤波
        self.declare_parameter("min_cutoff", 5.0)
        self.declare_parameter("beta", 0.1)
        self.declare_parameter("d_cutoff", 20.0)

        # 姿态滤波
        self.declare_parameter("quat_filter_mode", "slerp_ema")  # slerp_ema | so3_log
        self.declare_parameter("quat_cutoff", 5.0)               # Hz

        host = self.get_parameter("host").value
        port = int(self.get_parameter("port").value)
        publish_freq = float(self.get_parameter("publish_freq").value)
        receiv_freq = float(self.get_parameter("receiv_freq").value)

        world_frame = self.get_parameter("frame_id").value
        left_frame  = self.get_parameter("left_frame_id").value
        right_frame = self.get_parameter("right_frame_id").value
        head_frame  = self.get_parameter("head_frame_id").value
        static_parent_frame = self.get_parameter("static_parent_frame").value
        publish_world_pose  = bool(self.get_parameter("publish_world_pose").value)

        pose_qos_reliability = self.get_parameter("pose_qos_reliability").value

        min_cutoff = float(self.get_parameter("min_cutoff").value)
        beta       = float(self.get_parameter("beta").value)
        d_cutoff   = float(self.get_parameter("d_cutoff").value)

        quat_filter_mode = self.get_parameter("quat_filter_mode").value
        quat_cutoff      = float(self.get_parameter("quat_cutoff").value)

        self._state = SharedState()
        self._rx_th = ReceiverThread(host, port, self._state,
                                     min_cutoff, beta, d_cutoff, receiv_freq,
                                     quat_filter_mode=quat_filter_mode, quat_cutoff=quat_cutoff)
        self._tx_th = PublisherThread(self, self._state, publish_freq,
                                      world_frame, left_frame, right_frame, head_frame,
                                      static_parent_frame=static_parent_frame,
                                      pose_qos_reliability=pose_qos_reliability,
                                      publish_world_pose=publish_world_pose)

        self._rx_th.start()
        self._tx_th.start()

        self.add_on_set_parameters_callback(self._on_param_update)
        self.get_logger().info(
            f"VR bridge {host}:{port} pub {publish_freq}Hz; TF: {world_frame}->({left_frame},{right_frame},{head_frame}); "
            f"PoseQoS={pose_qos_reliability}; QuatFilter={quat_filter_mode}, cutoff={quat_cutoff}Hz; "
            f"publish_world_pose={publish_world_pose}"
        )

    def _on_param_update(self, params):
        changed = {p.name: p.value for p in params}
        if "publish_freq" in changed:
            try:
                hz = float(changed["publish_freq"])
                if hz > 0: self._tx_th.rate_hz = hz
            except Exception:
                pass
        if any(k in changed for k in ("min_cutoff", "beta", "d_cutoff")):
            mc = float(changed.get("min_cutoff", self.get_parameter("min_cutoff").value))
            bt = float(changed.get("beta", self.get_parameter("beta").value))
            dc = float(changed.get("d_cutoff", self.get_parameter("d_cutoff").value))
            self._rx_th.set_pos_params(mc, bt, dc)
        if "quat_cutoff" in changed:
            qc = float(changed.get("quat_cutoff", self.get_parameter("quat_cutoff").value))
            self._rx_th.set_quat_params(qc)
        return SetParametersResult(successful=True)

    def destroy_node(self):
        try:
            self._rx_th.stop(); self._tx_th.stop()
            self._rx_th.join(timeout=2.0); self._tx_th.join(timeout=2.0)
        finally:
            super().destroy_node()


# --------------------- 主入口 --------------------- 

def main():
    rclpy.init()
    node = VrRos2Bridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
