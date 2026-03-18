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
TeleOpt 增量随动桥接（相对位姿）+ 录制控制
- 订阅：
    /teleoperation/left_device  (deeptouch_interface/TeleOptDevice)
    /teleoperation/right_device (deeptouch_interface/TeleOptDevice)
- 发布：
    /teleoperation/left_cmd     (deeptouch_interface/TeleOptCmd)
    /teleoperation/right_cmd    (deeptouch_interface/TeleOptCmd)
    /cmd/left_pose              (PoseStamped，可视化 Δ)
    /cmd/right_pose             (PoseStamped，可视化 Δ)

录制控制逻辑：
1. 右手 two 按钮按下 -> 开始记录
2. 两个 index_trigger 都松开 -> 结束记录，进入5秒等待期
3. 等待期内按下 primary_thumb -> 废弃数据，回到空闲
4. 等待期内按下 two -> 开始新的记录
5. 等待期超时 -> 回到空闲
"""

# [修改点 1] 引入 field
from dataclasses import dataclass, field
from typing import Optional, Tuple
import numpy as np
from scipy.spatial.transform import Rotation as R


import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import Header
from deeptouch_interface.msg import TeleOptDevice, TeleOptCmd


# ---------------- 工具 ----------------

def pose_to_rt(pose):
    """
    Convert pose to rotation matrix and translation vector
    
    Args:
        pose: 7-element array [x, y, z, qx, qy, qz, qw] or similar format
    
    Returns:
        rot: 3x3 rotation matrix
        t: 3-element translation vector
    """

    # Extract translation and quaternion
    t = np.array([pose.position.x, pose.position.y, pose.position.z])
    q_xyzw = np.array([pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w])
    
    # Check if quaternion is valid (non-zero norm)
    quat_norm = np.linalg.norm(q_xyzw)
    
    if quat_norm < 1e-6:  # Very small norm, treat as zero quaternion
        # Use identity quaternion [0, 0, 0, 1] as fallback
        q_xyzw = np.array([0.0, 0.0, 0.0, 1.0])        
        rot = R.from_quat(q_xyzw)
    else:
        # Normalize quaternion to ensure unit length
        q_xyzw = q_xyzw / quat_norm
        
        # Check if quaternion format is correct (scipy expects [x, y, z, w])
        try:
            rot = R.from_quat(q_xyzw)
        except Exception as e:
            # Fallback to identity rotation
            rot = np.eye(3)
    
    return rot, t

def rt_to_T(rot: R, t: np.ndarray):
    T = np.eye(4)
    T[0:3, 0:3] = rot.as_matrix()
    T[0:3, 3] = t
    return T

def rt_to_pose(rot: R, t: np.ndarray) -> Pose:
    qx, qy, qz, qw = rot.as_quat()
    msg = Pose()
    msg.position.x, msg.position.y, msg.position.z = float(t[0]), float(t[1]), float(t[2])
    msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w = float(qx), float(qy), float(qz), float(qw)
    return msg


# ---------------- 状态 ----------------

@dataclass
class SideState:
    index_trigger: bool = False
    index_trigger_last: bool = False
    base_hand_start_pose: Optional[Pose] = None
    base_head_start_pose: Optional[Pose] = None
    hand_fixed_rot: Optional[R] = None
    head_fixed_rot: Optional[R] = None
    head_hand_start_T: Optional[np.array] = None
    scale: float = 1.0
    one: bool = False
    two: bool = False
    one_last: bool = False
    two_last: bool = False
    primary_thumb: bool = False
    primary_thumb_last: bool = False
    
    # [修改点 2] 使用 default_factory 避免 mutable default 错误
    last_cmd_pose: Pose = field(default_factory=Pose)
    
    thumbstick_x_last: float = 0.0
    thumbstick_y_last: float = 0.0
    is_index_trigger_release: bool = False  # 用于检测 index_trigger 的上升沿

    # 本次录制的评分：1=成功, -1=失败, 0=未标记
    rating: int = 0


# ---------------- 主节点 ----------------

class TeleOptDeltaBridge(Node):
    def __init__(self):
        super().__init__('teleopt_delta_bridge')

        # 参数
        self.declare_parameter('trigger_threshold', 0.8)
        self.declare_parameter('gripper_threshold', 0.8)
        self.declare_parameter('left_device_topic',  '/teleoperation/left_device')
        self.declare_parameter('right_device_topic', '/teleoperation/right_device')
        self.declare_parameter('left_cmd_topic',     '/teleoperation/left_cmd')
        self.declare_parameter('right_cmd_topic',    '/teleoperation/right_cmd')
        self.declare_parameter('reliable_cmd', True)
        self.declare_parameter('rviz_frame_id', 'vr_world')
        self.declare_parameter('save_timeout', 10.0)
        self.declare_parameter('fixed_rotation', False)

        # 读取参数
        self.trigger_th = float(self.get_parameter('trigger_threshold').value)
        self.gripper_th = float(self.get_parameter('gripper_threshold').value)
        self.rviz_frame_id = str(self.get_parameter('rviz_frame_id').value)
        self.save_timeout = float(self.get_parameter('save_timeout').value)
        self.fixed_rotation = bool(self.get_parameter('fixed_rotation').value)

        left_device_topic  = self.get_parameter('left_device_topic').value
        right_device_topic = self.get_parameter('right_device_topic').value
        left_cmd_topic     = self.get_parameter('left_cmd_topic').value
        right_cmd_topic    = self.get_parameter('right_cmd_topic').value
        reliable_cmd       = bool(self.get_parameter('reliable_cmd').value)

        # QoS
        cmd_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE if reliable_cmd else QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST, depth=10
        )
        vr_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST, depth=50
        )
        pose_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            history=QoSHistoryPolicy.KEEP_LAST, depth=10
        )

        # 发布者
        self.pub_left_cmd   = self.create_publisher(TeleOptCmd, left_cmd_topic,  cmd_qos)
        self.pub_right_cmd  = self.create_publisher(TeleOptCmd, right_cmd_topic, cmd_qos)
        self.pub_left_pose  = self.create_publisher(PoseStamped, "/cmd/left_pose",  pose_qos)
        self.pub_right_pose = self.create_publisher(PoseStamped, "/cmd/right_pose", pose_qos)


        # 订阅者
        self.sub_left  = self.create_subscription(TeleOptDevice, left_device_topic,  self._on_left,  vr_qos)
        self.sub_right = self.create_subscription(TeleOptDevice, right_device_topic, self._on_right, vr_qos)

        # 状态
        self.left_state  = SideState()
        self.right_state = SideState()

        # 录制控制状态机
        self.recording_state = 'idle'  # 'idle', 'recording', 'stop_record', 'discard'
        self.discard_timer_start = 0.0
        
        self.get_logger().info(f"TeleOptDeltaBridge started with recording control (timeout: {self.save_timeout}s)")

    def _update_recording_state(self):
        """更新录制状态逻辑"""
        current_time = self.get_clock().now().nanoseconds / 1e9

        # 检查按键的上升沿（按下瞬间）
        two_pressed = (self.right_state.two == 1) and not self.right_state.two_last
        primary_thumb_pressed = (self.right_state.primary_thumb == 1) and not self.right_state.primary_thumb_last  # 修正逻辑


        # 状态机逻辑
        if self.recording_state == 'idle':
            if two_pressed:
                self.recording_state = 'recording'
                self.get_logger().info("🎬 Recording")
                # 清除index_trigger_release状态
                #self._clear_trigger_release_flags()
                
        elif self.recording_state == 'recording':
            #再次按下two，进入等待废止状态
            if two_pressed:
                self.recording_state = 'stop_record'
                self.discard_timer_start = current_time
                self.get_logger().info(f"⏹️  Recording STOP, {self.save_timeout}s window for saving...")
                self.get_logger().info(f"   Press primary_thumb to save, press two to start new recording")
                
        elif self.recording_state == 'stop_record':
            time_elapsed = current_time - self.discard_timer_start

            if two_pressed:
                # 在等待期间按two - 开始新的录制
                self.recording_state = 'recording'
                self.get_logger().info("🎬 New Recording")
                # 新一轮录制前重置右手评分
                self.right_state.rating = 0
            
            elif primary_thumb_pressed and time_elapsed <= self.save_timeout:
                # 在超时时间内按primary_thumb - 确认保留本次录制
                # 同时根据右手摇杆左右(thumbstick_x_last)打成功/失败标签：
                #   x >=  0.5 → 成功
                #   x <= -0.5 → 失败
                #   其他       → 未打分
                x = self.right_state.thumbstick_x_last
                if x >= 0.5:
                    self.right_state.rating = 1
                    self.get_logger().info("🏆 Episode rated as SUCCESS via thumbstick_x")
                elif x <= -0.5:
                    self.right_state.rating = -1
                    self.get_logger().info("❌ Episode rated as FAILURE via thumbstick_x")
                else:
                    self.right_state.rating = 0

                self.recording_state = 'save'
                self.get_logger().info("💾 Save")
                
            elif time_elapsed > self.save_timeout:
                # 超时 - 自动保存/丢弃逻辑保持不变，只是清空评分
                self.recording_state = 'idle'
                self.get_logger().info("✅ Idle")
                self.right_state.rating = 0

        elif self.recording_state == 'save':
            # 保存状态 - 直接回到空闲
            self.recording_state = 'idle'
            self.get_logger().info("✅ Save and Idle")
            

    def _clear_trigger_release_flags(self):
        """清除双手的index_trigger释放标志"""
        self.right_state.is_index_trigger_release = False
        self.left_state.is_index_trigger_release = False

    def _get_record_state_string(self) -> str:
        """根据录制状态返回字符串"""
        return self.recording_state

    # ---------- 回调 ----------
    def _on_left(self, msg: TeleOptDevice):
        self._process(side='left', dev=msg, st=self.left_state,
                      pub_cmd=self.pub_left_cmd, pub_pose=self.pub_left_pose,
                      child_frame="cmd_left")

    def _on_right(self, msg: TeleOptDevice):
        self._process(side='right', dev=msg, st=self.right_state,
                      pub_cmd=self.pub_right_cmd, pub_pose=self.pub_right_pose,
                      child_frame="cmd_right")
        


    # ---------- 工具：发布 PoseStamped ----------
    def _publish_pose(self, pub_pose, pose: Pose):
        now = self.get_clock().now()
        msg = PoseStamped()
        msg.header = Header(stamp=now.to_msg(), frame_id=self.rviz_frame_id)
        msg.pose = pose
        pub_pose.publish(msg)

    # ---------- 核心 ----------
    def _process(self, side: str, dev: TeleOptDevice, st: SideState,
                 pub_cmd, pub_pose, child_frame: str):

        cmd = TeleOptCmd()

        ht = dev.hand_touch
        pressed = float(ht.index_trigger) > self.trigger_th
        grip_on = float(ht.hand_trigger) > self.gripper_th
        st.index_trigger = pressed

        # 更新按键状态
        st.one = (ht.one == 1)
        st.two = (ht.two == 1)
        st.primary_thumb = (ht.primary_thumb == 1)

        # 上升沿：记录基准、构造修正旋转
        if st.index_trigger and not st.index_trigger_last:
            st.base_hand_start_pose = dev.hand_pose
            st.base_head_start_pose = dev.head_pose

            # 校正VR头部的坐标系
            st.head_fixed_rot = R.from_rotvec(np.pi * np.array([1.0, 0.0, 0.0]))  # 绕X轴180°
            st.head_fixed_rot = st.head_fixed_rot * R.from_rotvec(np.pi/2 * np.array([0.0, 0.0, 1.0]))  # 绕Z轴90°
            
            # 校正VR hand 的坐标系
            st.hand_fixed_rot = R.from_rotvec(np.pi/2 * np.array([1.0, 0.0, 0.0]))  # 绕X轴90°
            st.hand_fixed_rot = st.hand_fixed_rot * R.from_rotvec(np.pi/2 * np.array([0.0, 0.0, 1.0]))  # 绕Z轴90°

            base_hand_start_rot, base_hand_start_t = pose_to_rt(st.base_hand_start_pose)
            base_head_start_rot, base_head_start_t = pose_to_rt(st.base_head_start_pose)

            base_head_start_T = rt_to_T(base_head_start_rot * st.head_fixed_rot, base_head_start_t)
            base_hand_start_T = rt_to_T(base_hand_start_rot * st.hand_fixed_rot, base_hand_start_t)

            st.head_hand_start_T = np.linalg.inv(base_head_start_T) @ base_hand_start_T

            cmd.is_calibrate_start_pose = True
        else:
            cmd.is_calibrate_start_pose = False

        if st.index_trigger and st.base_hand_start_pose and st.base_head_start_pose and st.hand_fixed_rot and st.head_fixed_rot:
            base_hand_rot, base_hand_t = pose_to_rt(dev.hand_pose)
            base_head_rot, base_head_t = pose_to_rt(dev.head_pose)
            
            base_hand_T = rt_to_T(base_hand_rot * st.hand_fixed_rot, base_hand_t)
            base_head_T = rt_to_T(base_head_rot * st.head_fixed_rot, base_head_t)
            
            head_hand_T = np.linalg.inv(base_head_T) @ base_hand_T

            t = head_hand_T[0:3, 3]
            R_mat = head_hand_T[0:3, 0:3]

            # hand_delta = t - st.head_hand_start_T[0:3, 3]
            hand_start_hand = np.linalg.inv(st.head_hand_start_T) @ head_hand_T
            hand_delta_rot = R.from_matrix(hand_start_hand[0:3, 0:3])
            hand_delta = hand_start_hand[0:3, 3]

            # 缩放
            hand_delta = hand_delta * st.scale

            # 组装相对位姿命令
            cmd.is_absolute_pose = False
            if self.fixed_rotation:
                cmd.hand_pose = rt_to_pose(R.identity(), hand_delta)
            else:
                cmd.hand_pose = rt_to_pose(hand_delta_rot, hand_delta)

            st.last_cmd_pose = cmd.hand_pose  # 记录用于可视化
        else:
            # 未按压或尚无基准：不随动，pose 维持上一次（保证 RViz 可见）
            cmd.is_absolute_pose = False
            cmd.is_calibrate_start_pose = True # 松开时也置位，方便下次按下时重新校准
            cmd.hand_pose = Pose()  # 发给机器人可以是零增量

        # 缩放控制
        if not st.index_trigger:
            if st.thumbstick_y_last <= 0.8 and ht.thumbstick_y >= 0.8:
                st.scale = min(st.scale * 1.2, 1.0)
                self.get_logger().info(f"{side} scale: {st.scale:.2f}")
            elif st.thumbstick_y_last >= -0.8 and ht.thumbstick_y <= -0.8:
                st.scale = st.scale * 0.8
                self.get_logger().info(f"{side} scale: {st.scale:.2f}")

        if self.recording_state == 'recording':
            if st.index_trigger == False and st.index_trigger_last == True:
                st.is_index_trigger_release = True

        # 只在右手柄处理时更新录制状态
        if side == 'right':
            self._update_recording_state()
            
        # 设置命令标志位
        cmd.is_follow = st.index_trigger
        cmd.gripper_cmd = grip_on
        cmd.is_initial_pose = (ht.one == 1)
        cmd.is_absolute_pose = False

        # 默认使用位移缩放
        cmd.scale = st.scale

        # 新增 rating 字段，仅对右手在停止/保存窗口中写入：
        #   1 → 成功, 255 → 失败, 0 → 未打分
        if side == 'right' and self.recording_state in ['stop_record', 'save']:
            if st.rating == 1:
                cmd.rating = 1
            elif st.rating == -1:
                cmd.rating = 255
            else:
                cmd.rating = 0
        else:
            cmd.rating = 0

        cmd.record_state = self._get_record_state_string()
        cmd.primary_thumb = (ht.primary_thumb == 1)

        # 发布机器人命令
        pub_cmd.publish(cmd)

        # PoseStamped（严格使用 rviz_frame_id 作为 frame_id）
        self._publish_pose(pub_pose, st.last_cmd_pose if not st.index_trigger else cmd.hand_pose)

        # 记录边沿
        st.index_trigger_last = st.index_trigger
        st.one_last = st.one
        st.two_last = st.two
        st.primary_thumb_last = st.primary_thumb
        st.thumbstick_x_last = ht.thumbstick_x
        st.thumbstick_y_last = ht.thumbstick_y

def main(): 
    rclpy.init()
    node = TeleOptDeltaBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
