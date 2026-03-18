#!/usr/bin/env python3

"""
Standalone HTTP server for dataset metadata, live camera streaming, and teleop script management.
Updated to support PDF specs: V1 REST APIs, flatChartData, MP4 Video Range streaming, and Teleop POST endpoints with Native WebSocket.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import logging
import math
import os
import re
import signal
import struct
import subprocess
import sys
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import cv2
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

# ==========================================
# 路径与依赖配置
# ==========================================
PROJECT_SRC_ROOT = Path(__file__).resolve().parent / "lixun"
if str(PROJECT_SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_SRC_ROOT))

from lerobot.cameras.opencv.configuration_opencv import OpenCVCameraConfig
from lerobot.cameras.realsense.configuration_realsense import RealSenseCameraConfig
from lerobot.cameras.utils import make_cameras_from_configs

LOGGER = logging.getLogger("dataset_http_server")


# ==========================================
# 工具函数
# ==========================================
def is_missing(value: Any) -> bool:
    if value is None:
        return True
    try:
        result = pd.isna(value)
    except Exception:
        return False
    if isinstance(result, (bool, np.bool_)):
        return bool(result)
    return False

def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if is_missing(value):
        return None
    return value

def named_vector(values: Any, names: list[str]) -> dict[str, Any]:
    if values is None:
        return {}
    if isinstance(values, np.ndarray):
        flat_values = values.tolist()
    elif isinstance(values, list):
        flat_values = values
    else:
        try:
            flat_values = list(values)
        except TypeError:
            return {}
    return {
        name: to_jsonable(flat_values[idx])
        for idx, name in enumerate(names)
        if idx < len(flat_values)
    }

def extract_prefix_items(data: dict[str, Any], prefix: str) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key.startswith(prefix)}


# ==========================================
# 核心业务类
# ==========================================
class DatasetInspector:
    def __init__(self, dataset_root: Path):
        self.dataset_root = dataset_root

    @property
    def info_path(self) -> Path:
        return self.dataset_root / "meta" / "info.json"

    def _load_json(self, path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def load_info(self) -> dict[str, Any]:
        if not self.info_path.exists():
            raise FileNotFoundError(f"Dataset info not found: {self.info_path}")
        return self._load_json(self.info_path)

    def _load_parquet_dir(self, folder: Path) -> pd.DataFrame:
        files = sorted(folder.glob("chunk-*/file-*.parquet"))
        if not files:
            return pd.DataFrame()
        return pd.concat((pd.read_parquet(file) for file in files), ignore_index=True)

    def load_episodes(self) -> pd.DataFrame:
        return self._load_parquet_dir(self.dataset_root / "meta" / "episodes")

    def load_tasks(self) -> pd.DataFrame:
        path = self.dataset_root / "meta" / "tasks.parquet"
        if not path.exists():
            return pd.DataFrame()
        return pd.read_parquet(path)

    def _iter_data_files(self) -> list[Path]:
        return sorted((self.dataset_root / "data").glob("chunk-*/file-*.parquet"))

    def _read_episode_frames(self, episode_index: int) -> pd.DataFrame:
        data_files = self._iter_data_files()
        if not data_files:
            return pd.DataFrame()

        columns = [
            "timestamp", "frame_index", "episode_index", "index", "task_index",
            "observation.state", "action",
        ]
        frames: list[pd.DataFrame] = []

        for file in data_files:
            try:
                table = pq.read_table(
                    file, filters=[("episode_index", "=", episode_index)], columns=columns
                )
            except Exception:
                df = pd.read_parquet(file, columns=columns)
                df = df[df["episode_index"] == episode_index]
                if not df.empty:
                    frames.append(df)
                continue

            if table.num_rows > 0:
                frames.append(table.to_pandas())

        if not frames:
            return pd.DataFrame()

        merged = pd.concat(frames, ignore_index=True)
        merged = merged.sort_values(by=["frame_index", "timestamp"], ascending=[True, True])
        return merged.reset_index(drop=True)

    def _task_lookup(self) -> dict[int, dict[str, Any]]:
        tasks_df = self.load_tasks()
        if tasks_df.empty or "task_index" not in tasks_df.columns:
            return {}
        lookup: dict[int, dict[str, Any]] = {}
        for _, row in tasks_df.iterrows():
            lookup[int(row["task_index"])] = {k: to_jsonable(v) for k, v in row.to_dict().items()}
        return lookup

    def summary(self) -> dict[str, Any]:
        info = self.load_info()
        feature_map = info.get("features", {})
        camera_features = [
            {
                "feature_key": key,
                "camera_name": key.split(".")[-1],
                "dtype": feature.get("dtype"),
                "shape": list(feature.get("shape", [])),
            }
            for key, feature in feature_map.items()
            if key.startswith("observation.images.")
        ]
        action_names = feature_map.get("action", {}).get("names", []) or []
        state_names = feature_map.get("observation.state", {}).get("names", []) or []
        episodes_df = self.load_episodes()

        return {
            "dataset_root": str(self.dataset_root),
            "robot_type": info.get("robot_type"),
            "fps": info.get("fps"),
            "total_episodes": int(info.get("total_episodes", 0)),
            "total_frames": int(info.get("total_frames", 0)),
            "camera_features": camera_features,
            "observation_state_names": state_names,
            "action_names": action_names,
            "dex_hand_fields": [n for n in action_names if n in {"left_arm_gripper", "right_arm_gripper"}],
            "episode_metadata_count": int(len(episodes_df)),
            "data_files_size_in_mb": info.get("data_files_size_in_mb", 0),
            "video_files_size_in_mb": info.get("video_files_size_in_mb", 0)
        }

    def list_episodes(self, limit: int, offset: int) -> dict[str, Any]:
        episodes_df = self.load_episodes()
        if episodes_df.empty:
            return {"total": 0, "items": []}

        if "episode_index" in episodes_df.columns:
            episodes_df = episodes_df.sort_values(by="episode_index", ascending=False)

        sliced = episodes_df.iloc[offset : offset + limit]
        return {
            "total": int(len(episodes_df)),
            "items": [{k: to_jsonable(v) for k, v in row.items()} for row in sliced.to_dict("records")],
        }

    def get_episode_data_v1(self, org: str, dataset_name: str, episode_index: int, host: str) -> dict[str, Any]:
        """构建完全对齐 PDF 文档的单集回放负载 (EpisodeData) [cite: 307-460]"""
        info = self.load_info()
        fps = info.get("fps", 10)
        
        frames_df = self._read_episode_frames(episode_index)
        state_names = info.get("features", {}).get("observation.state", {}).get("names", []) or []
        action_names = info.get("features", {}).get("action", {}).get("names", []) or []
        
        flat_chart_data = []
        for _, row in frames_df.iterrows():
            frame_data = {
                "timestamp": float(row.get("timestamp", 0.0)),
                "task_index": int(row.get("task_index", 0)) if not pd.isna(row.get("task_index")) else 0,
            }
            state_vec = row.get("observation.state", [])
            for i, val in enumerate(state_vec):
                if i < len(state_names): frame_data[f"obs_state_{state_names[i]}"] = float(val)
            action_vec = row.get("action", [])
            for i, val in enumerate(action_vec):
                if i < len(action_names): frame_data[f"action_{action_names[i]}"] = float(val)
            flat_chart_data.append(frame_data)

        cameras = [key for key, feat in info.get("features", {}).items() if feat.get("dtype") == "video"]
        duration = len(frames_df) / fps if not frames_df.empty else 0.0
        
        videos_info = []
        for cam in cameras:
            videos_info.append({
                "filename": cam,
                "url": f"http://{host}/api/v1/datasets/{org}/{dataset_name}/episodes/{episode_index}/videos/{cam}",
                "isSegmented": True, 
                "segmentStart": 0.0,
                "segmentEnd": duration,
                "segmentDuration": duration
            })

        task_lookup = self._task_lookup()
        tasks_list = [t.get("task", "") for _, t in sorted(task_lookup.items())]

        dataset_summary = self.summary()
        dataset_summary["repoId"] = f"{org}/{dataset_name}"
        dataset_summary["codebase_version"] = "v3.0"

        return {
            "datasetInfo": dataset_summary,
            "episodeId": episode_index,
            "videosInfo": videos_info,
            "flatChartData": flat_chart_data,
            "episodes": [int(ep) for ep in self.load_episodes().get("episode_index", [])],
            "ignoredColumns": ["index", "episode_index", "frame_index"],
            "duration": duration,
            "task": tasks_list[0] if tasks_list else "",
            "tasks": tasks_list
        }


class LiveCameraManager:
    def __init__(self, camera_spec: dict[str, Any] | None):
        self.camera_spec = camera_spec or {}
        self._cameras: dict[str, Any] = {}
        self._start_lock = threading.Lock()
        self._frame_lock = threading.Lock()
        self._started = False
        self._start_error: str | None = None

    def _build_camera_configs(self) -> dict[str, Any]:
        configs = {}
        for camera_name, spec in self.camera_spec.items():
            camera_type = spec.get("type")
            if camera_type == "intelrealsense":
                configs[camera_name] = RealSenseCameraConfig(
                    serial_number_or_name=str(spec["serial_number_or_name"]),
                    fps=int(spec["fps"]), width=int(spec["width"]), height=int(spec["height"]),
                )
            elif camera_type == "opencv":
                index_or_path = spec["index_or_path"]
                if isinstance(index_or_path, str) and index_or_path.isdigit():
                    index_or_path = int(index_or_path)
                configs[camera_name] = OpenCVCameraConfig(
                    index_or_path=index_or_path, fps=int(spec["fps"]),
                    width=int(spec["width"]), height=int(spec["height"]),
                )
            else:
                raise ValueError(f"Unsupported camera type: {camera_type}")
        return configs

    def ensure_started(self) -> None:
        if self._started or self._start_error is not None:
            return
        if not self.camera_spec:
            self._start_error = "Live camera is not configured."
            return

        with self._start_lock:
            if self._started or self._start_error is not None:
                return
            try:
                self._cameras = make_cameras_from_configs(self._build_camera_configs())
                for camera in self._cameras.values():
                    camera.connect()
                self._started = True
                LOGGER.info("Live camera manager started with cameras: %s", list(self._cameras))
            except Exception as exc:
                self._start_error = str(exc)
                LOGGER.exception("Failed to start live camera manager")

    def status(self) -> dict[str, Any]:
        return {
            "configured": bool(self.camera_spec),
            "started": self._started,
            "error": self._start_error,
            "cameras": list(self.camera_spec.keys()),
        }

    def get_frame_jpeg(self, camera_name: str, jpeg_quality: int = 85) -> bytes:
        self.ensure_started()
        if self._start_error is not None:
            raise RuntimeError(self._start_error)
        if camera_name not in self._cameras:
            raise KeyError(f"Unknown camera: {camera_name}")

        with self._frame_lock:
            frame = self._cameras[camera_name].async_read(timeout_ms=500)

        if frame is None:
            raise RuntimeError(f"Camera '{camera_name}' returned no frame.")

        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        ok, encoded = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), int(jpeg_quality)])
        if not ok:
            raise RuntimeError(f"Failed to JPEG-encode frame from camera '{camera_name}'.")
        return encoded.tobytes()

    def close(self) -> None:
        for camera in self._cameras.values():
            try:
                camera.disconnect()
            except Exception:
                LOGGER.exception("Failed to disconnect camera cleanly")


class TeleopManager:
    """管理遥操作脚本的启动与停止，并提供状态信息 [cite: 726-799, 892-1032]"""
    def __init__(self):
        self.process: subprocess.Popen | None = None
        self.lock = threading.Lock()
        
        # TODO: 替换为你实际的 bash 脚本路径
        self.START_SCRIPT = "/path/to/your/start_teleop.sh"
        self.STOP_SCRIPT = "/path/to/your/stop_teleop.sh"
        
        self._start_time = 0.0
        self._frame_count = 0

    def start(self, goal_id: str = "") -> tuple[int, str]:
        with self.lock:
            if self.process is not None and self.process.poll() is None:
                return 1, "遥操作服务已在运行中"

            try:
                LOGGER.info(f"正在启动遥操作脚本... goal_id: {goal_id}")
                self.process = subprocess.Popen(
                    ["bash", self.START_SCRIPT, goal_id],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self._start_time = time.time()
                self._frame_count = 0
                return 0, "ok"
            except Exception as e:
                LOGGER.error(f"启动遥操作脚本失败: {e}")
                return 1, f"启动失败: {str(e)}"

    def stop(self) -> tuple[int, str]:
        with self.lock:
            try:
                LOGGER.info("正在停止遥操作脚本...")
                if self.process and self.process.poll() is None:
                    self.process.terminate()
                    self.process.wait(timeout=5)
                self.process = None
                self._start_time = 0.0
                self._frame_count = 0
                return 0, "ok"
            except Exception as e:
                LOGGER.error(f"停止遥操作脚本失败: {e}")
                return 1, f"停止失败: {str(e)}"

    def get_telemetry(self) -> tuple[int, int, int]:
        """返回 (status, duration, frame_count)"""
        with self.lock:
            if self.process is None:
                return 0, 0, 0 # 0=空闲 [cite: 765, 996]
            
            if self.process.poll() is None:
                duration = int(time.time() - self._start_time)
                # 模拟帧数增长，生产环境可替换为读取实际录制帧数
                self._frame_count = int(duration * 10) 
                return 1, duration, self._frame_count # 1=采集中 [cite: 766, 997]
            
            return -1, 0, 0 # -1=异常 [cite: 767, 998]


class App:
    def __init__(self, dataset_root: Path, camera_spec: dict[str, Any] | None, jpeg_quality: int):
        self.dataset = DatasetInspector(dataset_root)
        self.live_camera = LiveCameraManager(camera_spec)
        self.teleop = TeleopManager()
        self.jpeg_quality = jpeg_quality


# ==========================================
# HTTP / WebSocket 路由处理
# ==========================================
class RequestHandler(BaseHTTPRequestHandler):
    server_version = "StandaloneDatasetHTTP/2.0"

    @property
    def app(self) -> App:
        return self.server.app  # type: ignore[attr-defined]

    def _send_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
        body = json.dumps(to_jsonable(payload), ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_error_json(self, message: str, status: int = HTTPStatus.BAD_REQUEST) -> None:
        self._send_json({"ok": False, "error": message}, status=status)
        
    def _send_teleop_resp(self, code: int, message: str, data: Any = None) -> None:
        self._send_json({"code": code, "message": message, "data": data}, status=HTTPStatus.OK)

    def _serve_mp4_with_range(self, filepath: Path) -> None:
        """处理带有 Range 头的 MP4 切片请求 [cite: 471-495]"""
        if not filepath.exists():
            self._send_error_json(f"Video file not found: {filepath.name}", HTTPStatus.NOT_FOUND)
            return

        file_size = filepath.stat().st_size
        range_header = self.headers.get('Range', '')
        
        start_byte = 0
        end_byte = file_size - 1

        if range_header:
            match = re.search(r'bytes=(\d+)-(\d*)', range_header)
            if match:
                start_byte = int(match.group(1))
                if match.group(2):
                    end_byte = int(match.group(2))
        
        length = end_byte - start_byte + 1
        
        self.send_response(HTTPStatus.PARTIAL_CONTENT if range_header else HTTPStatus.OK)
        self._send_cors_headers()
        self.send_header("Content-Type", "video/mp4")
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {start_byte}-{end_byte}/{file_size}")
        self.send_header("Content-Length", str(length))
        self.end_headers()

        with open(filepath, 'rb') as f:
            f.seek(start_byte)
            chunk_size = 1024 * 1024 # 1MB chunks
            to_read = length
            while to_read > 0:
                data = f.read(min(chunk_size, to_read))
                if not data:
                    break
                self.wfile.write(data)
                to_read -= len(data)

    def _handle_websocket(self):
        """原生处理 WebSocket 握手与服务端到客户端的单向数据推送 [cite: 979-1032]"""
        upgrade = self.headers.get('Upgrade', '').lower()
        if upgrade != 'websocket':
            self.send_error(HTTPStatus.BAD_REQUEST, "Expected WebSocket upgrade")
            return

        key = self.headers.get('Sec-WebSocket-Key')
        if not key:
            self.send_error(HTTPStatus.BAD_REQUEST, "Missing Sec-WebSocket-Key")
            return

        magic_string = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        accept_key = base64.b64encode(hashlib.sha1(key.encode('utf-8') + magic_string).digest()).decode('utf-8')

        response = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
        self.wfile.flush()
        LOGGER.info(f"WebSocket 客户端已连接: {self.client_address}")

        try:
            while True:
                status, duration, frame_count = self.app.teleop.get_telemetry()
                payload_dict = {
                    "status": status,
                    "duration": duration,
                    "frame_count": frame_count
                }
                payload_bytes = json.dumps(payload_dict).encode('utf-8')
                
                length = len(payload_bytes)
                if length < 126:
                    header = struct.pack('!BB', 0x81, length)
                elif length < 65536:
                    header = struct.pack('!BBH', 0x81, 126, length)
                else:
                    header = struct.pack('!BBQ', 0x81, 127, length)
                
                self.wfile.write(header + payload_bytes)
                self.wfile.flush()
                
                time.sleep(1.0) # 1Hz 推送频率
        except (BrokenPipeError, ConnectionResetError):
            LOGGER.info(f"WebSocket 客户端断开连接: {self.client_address}")
        except Exception as e:
            LOGGER.error(f"WebSocket 推送异常: {e}")

    def do_OPTIONS(self) -> None:
        self.send_response(HTTPStatus.NO_CONTENT)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else b""
            payload = json.loads(post_data.decode('utf-8')) if post_data else {}

            # T2. 启动遥操作 [cite: 892-944]
            if path == "/api/teleop/start":
                goal_id = payload.get("goal_id", "")
                code, msg = self.app.teleop.start(goal_id=goal_id)
                self._send_teleop_resp(code, msg)
                return
            
            # T3. 停止遥操作 [cite: 945-978]
            if path == "/api/teleop/stop":
                code, msg = self.app.teleop.stop()
                self._send_teleop_resp(code, msg)
                return

            self._send_error_json(f"Unknown POST endpoint: {path}", status=HTTPStatus.NOT_FOUND)
        except Exception as exc:
            LOGGER.exception("POST request handling failed")
            self._send_error_json(str(exc), status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        host = self.headers.get('Host', 'localhost:8000')

        try:
            # ---------------------------------------------------------
            # T4 遥操作采集状态 (原生 WebSocket) [cite: 979-1032]
            # ---------------------------------------------------------
            if path == "/api/teleop/feedback":
                self._handle_websocket()
                return 

            # ---------------------------------------------------------
            # V1 RESTful APIs (回放页面)
            # ---------------------------------------------------------
            if path == "/api/v1/datasets": # [cite: 199-263]
                summary = self.app.dataset.summary()
                episodes = self.app.dataset.list_episodes(limit=1000, offset=0)
                resp = {
                    "total": 1, "page": 1, "page_size": 20,
                    "datasets": [{
                        "repoId": "local_org/local_dataset",
                        "robot_type": summary.get("robot_type"),
                        "codebase_version": "v3.0",
                        "total_episodes": summary.get("total_episodes"),
                        "total_frames": summary.get("total_frames"),
                        "fps": summary.get("fps"),
                        "data_files_size_in_mb": summary.get("data_files_size_in_mb"),
                        "video_files_size_in_mb": summary.get("video_files_size_in_mb"),
                        "episodes": [
                            {
                                "episode_index": ep["episode_index"],
                                "length": ep.get("length", 0),
                                "duration_sec": ep.get("length", 0) / (summary.get("fps") or 10),
                                "task": "Unknown task"
                            } for ep in episodes["items"]
                        ]
                    }]
                }
                self._send_json(resp)
                return

            if re.match(r"/api/v1/datasets/([^/]+)/([^/]+)/episodes/?$", path): # [cite: 264-306]
                episodes = self.app.dataset.list_episodes(limit=1000, offset=0)
                fps = self.app.dataset.summary().get("fps", 10)
                self._send_json({
                    "total": episodes["total"],
                    "episodes": [{
                        "episode_index": ep["episode_index"],
                        "task_index": 0,
                        "task": "Unknown task",
                        "length": ep.get("length", 0),
                        "duration_sec": ep.get("length", 0) / fps
                    } for ep in episodes["items"]]
                })
                return

            match_ep_data = re.match(r"/api/v1/datasets/([^/]+)/([^/]+)/episodes/(\d+)/?$", path) # [cite: 307-470]
            if match_ep_data:
                org, dataset_name, ep_id_str = match_ep_data.groups()
                episode_data = self.app.dataset.get_episode_data_v1(org, dataset_name, int(ep_id_str), host)
                self._send_json(episode_data)
                return

            match_video = re.match(r"/api/v1/datasets/([^/]+)/([^/]+)/episodes/(\d+)/videos/(.+)$", path) # [cite: 471-495]
            if match_video:
                _, _, ep_id_str, camera = match_video.groups()
                ep_id = int(ep_id_str)
                
                info = self.app.dataset.load_info()
                chunks_size = info.get("chunks_size", 1000)
                chunk_index = math.floor(ep_id / chunks_size)
                
                video_file = self.app.dataset.dataset_root / "videos" / camera / f"chunk-{chunk_index:03d}" / f"file-{chunk_index:03d}.mp4"
                self._serve_mp4_with_range(video_file)
                return

            # ---------------------------------------------------------
            # 遥操作相关接口 (Teleop)
            # ---------------------------------------------------------
            if path == "/api/teleop/cameras": # [cite: 1033-1131]
                self._send_teleop_resp(0, "ok", {
                    "cameras": [
                        {
                            "id": i,
                            "name": cam_name,
                            "topic": f"/camera/{cam_name}",
                            "stream_url": f"http://{host}/api/live/stream?camera={cam_name}",
                            "snapshot_url": f"http://{host}/api/live/frame?camera={cam_name}",
                            "status": "online" if self.app.live_camera._started else "offline"
                        } for i, cam_name in enumerate(self.app.live_camera.camera_spec.keys())
                    ]
                })
                return

            # 向下兼容旧接口/基础接口
            if path == "/health":
                self._send_json({"ok": True, "status": "running"})
                return

            self._send_error_json(f"Unknown endpoint: {path}", status=HTTPStatus.NOT_FOUND)
        except FileNotFoundError as exc:
            self._send_error_json(str(exc), status=HTTPStatus.NOT_FOUND)
        except Exception as exc:
            LOGGER.exception("GET Request handling failed")
            self._send_error_json(str(exc), status=HTTPStatus.INTERNAL_SERVER_ERROR)

    def log_message(self, fmt: str, *args: Any) -> None:
        LOGGER.info("%s - %s", self.address_string(), fmt % args)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standalone dataset HTTP server with Teleop.")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP bind host")
    parser.add_argument("--port", type=int, default=8000, help="HTTP bind port")
    parser.add_argument("--dataset-root", required=True, help="LeRobot dataset root path")
    parser.add_argument("--camera-config", default="", help="Camera config JSON")
    parser.add_argument("--jpeg-quality", type=int, default=85, help="JPEG quality")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")

    camera_spec = json.loads(args.camera_config) if args.camera_config else {}
    app = App(
        dataset_root=Path(args.dataset_root).expanduser().resolve(),
        camera_spec=camera_spec,
        jpeg_quality=args.jpeg_quality,
    )

    httpd = ThreadingHTTPServer((args.host, args.port), RequestHandler)
    httpd.app = app  # type: ignore[attr-defined]

    def shutdown_handler(signum: int, frame: Any) -> None:
        LOGGER.info("Received signal %s, shutting down.", signum)
        app.live_camera.close()
        app.teleop.stop() # 退出时安全停止遥操作脚本
        httpd.shutdown()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    LOGGER.info("HTTP/WebSocket server started: http://%s:%s", args.host, args.port)
    try:
        httpd.serve_forever()
    finally:
        app.live_camera.close()
        app.teleop.stop()
        httpd.server_close()

if __name__ == "__main__":
    main()