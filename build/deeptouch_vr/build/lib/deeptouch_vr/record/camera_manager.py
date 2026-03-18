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

import time
import threading
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union
import logging
import os
import glob
import subprocess

import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import gc


class CameraInterface(ABC):
    """Abstract base class for all camera types"""
    
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.is_streaming = False
        self.logger = logging.getLogger(f"Camera_{name}")
        
        # Stream configuration
        self.rgb_stream = config.get('rgb_stream', True)
        self.depth_stream = config.get('depth_stream', True)

        self.capture_width = config.get('width', 1280)  
        self.capture_height = config.get('height', 720)  

        self.process_width = config.get('process_width', self.capture_width)  
        self.process_height = config.get('process_height', self.capture_height) 

        # Frame buffer
        self.latest_frames = {'color': None, 'depth': None, 'timestamp': None}
        self.frame_lock = threading.Lock()
        
        self.display_buffer = {'color': None, 'depth': None, 'timestamp': None}
        self.display_lock = threading.Lock()

        # Streaming control
        self.stream_thread = None
        self.stop_streaming_event = threading.Event()

        # 🔥 添加：帧引用计数和清理，防止内存占用过多
        self.frame_update_counter = 0
        self.gc_interval = 100  # 每100帧强制清理一次
        self.camera_frame_counts = {}  # 用于存储每个相机的帧计数器  
        for camera_name in self.camera_configs:  
            self.camera_frame_counts[camera_name] = 0  # 初始化为 0  
        # Tkinter related
        self.image_show = config.get('image_show', False)
        if self.image_show:
            self.tk_root = config.get('tk_root', None)  # 接收Manager传入的Tkinter root
            if self.tk_root is None:
                raise ValueError(f"Camera {name}: image_show=True requires tk_root from CameraManager")

            self.display_window = None  # will be a Toplevel window
            self.label = None
            self.display_update_interval_ms = config.get('display_update_interval_ms', 30)  # 显示更新周期
            self._update_display_id = None  # 用于取消after任务

            # Optional: max display width/height for resizing
            self.max_display_width = config.get('width', 640)
            self.max_display_height = config.get('height', 480)
        
        self.logger.info(f"Camera {name} config: RGB={self.rgb_stream}, Depth={self.depth_stream}, Image Show={self.image_show}")

    @abstractmethod
    def start(self):
        """Start camera streaming"""
        pass

    def _initialize_display(self):
        """初始化显示窗口 - 必须在Tkinter线程中调用"""
        if self.image_show and self.tk_root:
            # 使用after确保在Tkinter线程中执行
            self.tk_root.after(0, self._create_display_window)

    def _create_display_window(self):
        """在Tkinter线程中创建显示窗口"""
        try:
            if self.display_window is None or not self.display_window.winfo_exists():
                self.display_window = tk.Toplevel(self.tk_root)
                self.display_window.title(f"{self.name} Feed")
                self.display_window.protocol("WM_DELETE_WINDOW", self._stop_display)

            if self.label is None:
                self.label = tk.Label(self.display_window)
                self.label.pack()

            # Schedule the first update
            self._schedule_update()
            self.logger.info(f"Display for camera {self.name} initialized")
            
        except Exception as e:
            self.logger.error(f"Error creating display window: {e}")
    
    def _schedule_update(self):
        """调度下一次显示更新"""
        if self.display_window and self.display_window.winfo_exists():
            self._update_display_id = self.display_window.after(
                self.display_update_interval_ms, 
                self._update_display
            )

    def _stop_display(self):
        """停止Tkinter显示"""
        if self.image_show:
            if self._update_display_id and self.display_window:
                try:
                    self.display_window.after_cancel(self._update_display_id)
                    self._update_display_id = None
                    self.logger.info(f"Stopped display updates for camera {self.name}")
                except Exception as e:
                    self.logger.debug(f"Error cancelling after: {e}")
            
            if self.display_window:
                try:
                    if self.display_window.winfo_exists():
                        self.display_window.destroy()
                    self.display_window = None
                    self.label = None
                    self.logger.info(f"Destroyed display window for camera {self.name}")
                except Exception as e:
                    self.logger.debug(f"Error destroying window: {e}")

    @abstractmethod
    def stop(self):
        """Stop camera streaming"""
        self.is_streaming = False
        self.stop_streaming_event.set()
        
        self._stop_display()

        if self.stream_thread and self.stream_thread.is_alive():
            self.stream_thread.join(timeout=1) # 等待流线程结束
            if self.stream_thread.is_alive():
                self.logger.warning(f"Stream thread for {self.name} did not terminate gracefully.")

    
    @abstractmethod
    def _streaming_loop(self):
        """Main streaming loop - must be implemented by subclasses"""
        pass
    
    def get_latest_frames(self) -> Optional[Dict]:
        """Get the latest captured frames"""
        with self.frame_lock:
            
            result = {'timestamp': self.latest_frames['timestamp']}
                
            result['color'] = self.latest_frames['color'].copy() 
            
            if self.config.get('depth_stream',True):
               result['depth'] = self.latest_frames['depth'].copy()

            return result


    def _update_latest_frames(self, color_image, depth_image):
        """统一的帧更新方法，带内存管理"""
        with self.frame_lock:
            # 🔥 先删除旧引用
            old_frames = self.latest_frames
            if old_frames['color'] is not None:
                del old_frames['color']
            if old_frames['depth'] is not None:
                del old_frames['depth']
            
            # 更新新帧
            self.latest_frames = {
                'color': color_image,
                'depth': depth_image,
                'timestamp': time.time()
            }
            
            # 🔥 定期强制垃圾回收
            self.frame_update_counter += 1
            if self.frame_update_counter % 4 == 0 and self.image_show:
                with self.display_lock:
                    if color_image is not None:
                        self.display_buffer['color'] = color_image.copy()
                    self.display_buffer['timestamp'] = time.time()

            if self.frame_update_counter % self.gc_interval == 0:
                import gc
                gc.collect()

    def _update_display(self):
        """更新显示内容 - 在Tkinter线程中通过after调用"""
        if self.image_show and self.label and self.display_window and self.display_window.winfo_exists():
            color_image_bgr = None
            with self.display_lock:
                if self.latest_frames['color'] is not None:
                    color_image_bgr = self.display_buffer['color']

            if color_image_bgr is not None:
                try:
                    # Convert BGR to RGB for PIL
                    rgb_image_array = cv2.cvtColor(color_image_bgr, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(rgb_image_array)
                    
                    # Resize for display if needed
                    if img.width > self.max_display_width or img.height > self.max_display_height:
                        aspect_ratio = img.width / img.height
                        if img.width > self.max_display_width:
                            new_width = self.max_display_width
                            new_height = int(new_width / aspect_ratio)
                        else:
                            new_height = self.max_display_height
                            new_width = int(new_height * aspect_ratio)
                        img = img.resize((new_width, new_height), Image.LANCZOS)

                    imgtk = ImageTk.PhotoImage(image=img)
                    self.label.imgtk = imgtk  # Keep a reference
                    self.label.configure(image=imgtk)
                    
                except Exception as e:
                    self.logger.error(f"Error updating frame for {self.name}: {e}")
            
            # 重新调度下一次更新
            self._schedule_update()
        elif self.image_show and (not self.display_window or not self.display_window.winfo_exists()):
            # 窗口被关闭，停止更新
            self._stop_display()

class RealSenseCamera(CameraInterface):
    """RealSense camera implementation"""
    
    def __init__(self, name: str, config: dict):
        self.camera_configs = config
        super().__init__(name, config)
        
        # Check if pyrealsense2 is available
        try:
            import pyrealsense2 as rs
            self.rs = rs
        except ImportError:
            raise ImportError("pyrealsense2 not available. Please install pyrealsense2 to use RealSense cameras.")
        
        self.serial = config.get('serial')
        self.pipeline = None
        self.align = None
        
        # Validate stream configuration
        if not self.rgb_stream and not self.depth_stream:
            raise ValueError(f"At least one stream (rgb_stream or depth_stream) must be enabled for camera {name}")
    
    def start(self):
        """Start RealSense camera streaming"""
        if self.is_streaming:
            return
        
        try:
            # Configure pipeline
            self.pipeline = self.rs.pipeline()
            config = self.rs.config()
            
            # Enable device
            if self.serial:
                config.enable_device(self.serial)
            
            # Configure streams based on settings
            width = self.capture_width
            height = self.capture_height
            fps = self.config.get('fps', 30)
            
            streams_enabled = []
            
            if self.rgb_stream:
                config.enable_stream(self.rs.stream.color, width, height, self.rs.format.bgr8, fps)
                streams_enabled.append("RGB")
            
            if self.depth_stream:
                config.enable_stream(self.rs.stream.depth, width, height, self.rs.format.z16, fps)
                streams_enabled.append("Depth")
            
            self.logger.info(f"RealSense camera {self.name} enabling streams: {', '.join(streams_enabled)}")
            
            # Start pipeline
            self.pipeline.start(config)
            
            # Create align object if both streams are enabled
            if self.rgb_stream and self.depth_stream:
                align_to = self.rs.stream.color
                self.align = self.rs.align(align_to)
            
            # Wait for auto-exposure to stabilize
            for _ in range(30):
                self.pipeline.wait_for_frames()
            
            self.is_streaming = True
            
            # Start streaming thread
            self.stop_streaming_event.clear()
            self.stream_thread = threading.Thread(target=self._streaming_loop)
            self.stream_thread.daemon = True
            self.stream_thread.start()

            if self.image_show:
                self._initialize_display()
            
            self.logger.info(f"RealSense camera {self.name} (serial: {self.serial}) started")
            
        except Exception as e:
            self.logger.error(f"Failed to start RealSense camera {self.name}: {e}")
            raise
    
    def stop(self):
        """Stop RealSense camera streaming"""
        super().stop()
        if not self.is_streaming:
            return
        
        self.is_streaming = False
        self.stop_streaming_event.set()
        
        if self.stream_thread:
            self.stream_thread.join(timeout=2.0)
        
        if self.pipeline:
            self.pipeline.stop()
        
        self.logger.info(f"RealSense camera {self.name} stopped")
    
    def _streaming_loop(self):
        """RealSense streaming loop"""
        while not self.stop_streaming_event.is_set():
            try:
                # Wait for frames
                frames = self.pipeline.wait_for_frames(timeout_ms=100)
                
                # Process frames based on enabled streams
                color_image = None
                depth_image = None
                
                if self.rgb_stream and self.depth_stream:
                    # Both streams enabled - use alignment
                    aligned_frames = self.align.process(frames)
                    
                    color_frame = aligned_frames.get_color_frame()
                    depth_frame = aligned_frames.get_depth_frame()
                    
                    if color_frame:  
                        original_color_image = np.asanyarray(color_frame.get_data())  
                        if (self.capture_width != self.process_width or self.capture_height != self.process_height):  
                            color_image = cv2.resize(  
                                original_color_image,  
                                (self.process_width, self.process_height),  
                                interpolation=cv2.INTER_AREA  
                            )  
                        else:  
                            color_image = original_color_image  
                    
                    if depth_frame:  
                        original_depth_image = np.asanyarray(depth_frame.get_data())  
                        if (self.capture_width != self.process_width or self.capture_height != self.process_height):  
                            # 使用 INTER_NEAREST (最近邻插值) 来缩放深度图，  
                            # 这可以防止在像素之间创建不存在的、错误的深度值。  
                            depth_image = cv2.resize(  
                                original_depth_image,  
                                (self.process_width, self.process_height),  
                                interpolation=cv2.INTER_NEAREST  
                            )  
                        else:  
                            depth_image = original_depth_image  
                        
                        # 在缩放之后应用深度比例变换  
                        depth_scale = self.config.get('depth_scale', 0.001)  
                        depth_image = depth_image.astype(np.float32) * depth_scale  
                        
                elif self.rgb_stream:
                    # Only RGB stream
                    color_frame = frames.get_color_frame()
                    if color_frame:  
                        original_color_image = np.asanyarray(color_frame.get_data())  
                        # 检查是否需要缩放  
                        if (self.capture_width != self.process_width or self.capture_height != self.process_height):  
                            color_image = cv2.resize(  
                                original_color_image,  
                                (self.process_width, self.process_height),  
                                interpolation=cv2.INTER_AREA  
                            )  
                        else:  
                            color_image = original_color_image  
                        
                elif self.depth_stream:
                    # Only depth stream
                    depth_frame = frames.get_depth_frame()
                    if depth_frame:
                        depth_image = np.asanyarray(depth_frame.get_data())
                        # Apply depth scaling
                        depth_scale = self.config.get('depth_scale', 0.001)
                        depth_image = depth_image.astype(np.float32) * depth_scale
                
                # Update latest frames only if we have data
                if (self.rgb_stream and color_image is not None) or (self.depth_stream and depth_image is not None):
                    self._update_latest_frames(color_image, depth_image)

                
            except Exception as e:
                if not self.stop_streaming_event.is_set():
                    self.logger.warning(f"Error in RealSense streaming loop: {e}")


class VideoCamera(CameraInterface):
    """Video camera implementation for /dev/video* devices"""
    
    def __init__(self, name: str, config: dict):
        self.camera_configs = config
        super().__init__(name, config)
        self.device_path = config.get('device_path', '/dev/video0')
        self.cap = None
        
        # Video cameras typically don't have depth
        if self.depth_stream:
            self.logger.warning(f"Video camera {name} does not support depth stream. depth_stream will return None.")
        
        # Validate stream configuration
        if not self.rgb_stream:
            if self.depth_stream:
                self.logger.warning(f"Video camera {name} only supports RGB stream. Depth stream will be None.")
            else:
                raise ValueError(f"Video camera {name} must have rgb_stream enabled")
        
    
    def start(self):
        """Start video camera streaming"""
        if self.is_streaming:
            return
        
        try:
            # Open video capture with different backends to improve compatibility
            self.cap = cv2.VideoCapture(self.device_path, cv2.CAP_V4L2)  # Try V4L2 first
            
            if not self.cap.isOpened():
                # Fallback to default backend
                self.cap = cv2.VideoCapture(self.device_path)
                
            if not self.cap.isOpened():
                raise RuntimeError(f"Cannot open video device {self.device_path} ")
            
            # Configure video capture
            width = self.config.get('width', 640)
            height = self.config.get('height', 480)
            fps = self.config.get('fps', 30)
            
            # Set buffer size to reduce latency
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Set format to MJPEG for better performance if available
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.cap.set(cv2.CAP_PROP_FPS, fps)
            
            # Get actual settings
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            actual_fps = self.cap.get(cv2.CAP_PROP_FPS)
            
            # Test capture to ensure it works
            ret, test_frame = self.cap.read()
            if not ret or test_frame is None:
                raise RuntimeError(f"Cannot read frames from video device {self.device_path}")
            
            streams_info = []
            if self.rgb_stream:
                streams_info.append("RGB")
            if self.depth_stream:
                streams_info.append("Depth(None)")
                
            self.logger.info(f"Video camera {self.name}: {actual_width}x{actual_height} @ {actual_fps} FPS")
            self.logger.info(f"Streams: {', '.join(streams_info)}")
            self.logger.info(f"Test frame shape: {test_frame.shape}")
            
            self.is_streaming = True
            
            # Start streaming thread
            self.stop_streaming_event.clear()
            self.stream_thread = threading.Thread(target=self._streaming_loop)
            self.stream_thread.daemon = True
            self.stream_thread.start()

            if self.image_show:
                self._initialize_display()
            
            self.logger.info(f"Video camera {self.name} ({self.device_path}) started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start video camera {self.name}: {e}")
            if self.cap:
                self.cap.release()
            raise
    
    def stop(self):
        """Stop video camera streaming"""
        super().stop()
        if not self.is_streaming:
            return
        
        self.is_streaming = False
        self.stop_streaming_event.set()
        
        if self.stream_thread:
            self.stream_thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
        
        self.logger.info(f"Video camera {self.name} stopped")
    
    def _streaming_loop(self):
        """Video camera streaming loop"""
        frame_count = 0
        fps_timer = time.time()
        target_fps = self.config.get('fps', 30)
        frame_interval = 1.0 / target_fps
        
        while not self.stop_streaming_event.is_set():
            try:
                start_time = time.time()
                
                color_image = None
                depth_image = None
                
                # Read frame only if RGB stream is enabled
                if self.rgb_stream:
                    ret, frame = self.cap.read()
                    
                    if not ret or frame is None:
                        self.logger.warning(f"Failed to read frame from {self.name}")
                        time.sleep(0.1)
                        continue
                    
                    color_image = frame
                    frame_count += 1
                
                # Create depth image based on configuration
                if self.depth_stream:
                    # Video cameras don't have real depth, so create dummy depth
                    if color_image is not None:
                        height, width = color_image.shape[:2]
                        depth_image = np.zeros((height, width), dtype=np.float32)
                    else:
                        # If no color image but depth requested, create default size
                        height = self.config.get('height', 480)
                        width = self.config.get('width', 640)
                        depth_image = np.zeros((height, width), dtype=np.float32)
                
                # Log FPS every 5 seconds
                current_time = time.time()
                if frame_count > 0 and current_time - fps_timer > 5.0:
                    fps = frame_count / (current_time - fps_timer)
                    self.logger.debug(f"Video camera {self.name} actual FPS: {fps:.1f}")
                    frame_count = 0
                    fps_timer = current_time
                
                # Update latest frames
                self._update_latest_frames(color_image, depth_image)
                
                # Control frame rate
                elapsed = time.time() - start_time
                if elapsed < frame_interval:
                    time.sleep(frame_interval - elapsed)
                
            except Exception as e:
                if not self.stop_streaming_event.is_set():
                    self.logger.warning(f"Error in video streaming loop for {self.name}: {e}")
                    time.sleep(0.1)


class CameraManager:
    """Manager for multiple cameras of different types"""
    
    def __init__(self, camera_configs: dict):
        self.camera_configs = camera_configs
        self.cameras = {}
        self.camera_frame_counts = {name: 0 for name in camera_configs}
        self.logger = logging.getLogger("CameraManager")
        
        for camera_name, config in camera_configs.items():  
            try:  
                camera_type = config.get('type')  
                if camera_type == 'RealSenseCamera':  
                    camera = RealSenseCamera(camera_name, config)  
                elif camera_type == 'VideoCamera':  
                    camera = VideoCamera(camera_name, config)  
                else:  
                    self.logger.warning(f"Unknown camera type {camera_type} for {camera_name}")  
                    continue  

                self.cameras[camera_name] = camera  
                
                # 为每个相机初始化帧计数  
                self.camera_frame_counts[camera_name] = 0
                
                self.logger.info(f"✅ Initialized camera: {camera_name}")  

            except Exception as e:  
                self.logger.error(f"❌ Failed to initialize camera {camera_name}: {e}")  
        
        # Tkinter相关
        self.tk_root = None
        self.tk_thread = None
        self.tk_ready = threading.Event()  # 用于同步Tkinter初始化
        
        # 如果需要显示图像，在独立线程中初始化Tkinter
        if any(config.get('image_show', False) for config in self.camera_configs.values()):
            self._start_tkinter_thread()
            # 等待Tkinter初始化完成
            if not self.tk_ready.wait(timeout=2.0):
                self.logger.error("Tkinter initialization timeout")
            else:
                self.logger.info("Tkinter thread started successfully")
        
        # List available devices
        self._list_available_devices()
        
        # Initialize cameras
        self._initialize_cameras()

    def _start_tkinter_thread(self):
        """在独立线程中启动Tkinter主循环"""
        def tk_thread_func():
            try:
                # 在新线程中创建Tkinter root
                self.tk_root = tk.Tk()
                self.tk_root.withdraw()  # 隐藏主窗口
                
                # 通知主线程Tkinter已就绪
                self.tk_ready.set()
                
                self.logger.info("Tkinter mainloop started in background thread")
                # 阻塞在这个线程中，不影响主程序
                self.tk_root.mainloop()
                self.logger.info("Tkinter mainloop ended")
                
            except Exception as e:
                self.logger.error(f"Error in Tkinter thread: {e}")
                self.tk_ready.set()  # 即使出错也要设置，避免主线程永久等待
        
        self.tk_thread = threading.Thread(target=tk_thread_func, daemon=True, name="TkinterThread")
        self.tk_thread.start()

    def _list_available_devices(self):
        """List all available camera devices"""
        self.logger.info("🔍 Scanning for available camera devices...")
        
        # Check if we need RealSense support
        need_realsense = any(config.get('type', '').lower() == 'realsense' 
                           for config in self.camera_configs.values())
        
        need_xense = any(config.get('type', '').lower() == 'xense' 
                            for config in self.camera_configs.values())
        
        need_tip = any(config.get('type', '').lower() == 'tip' 
                            for config in self.camera_configs.values())
        
        if need_realsense:
            self._list_realsense_devices()
        if need_xense:
            self._list_xense_devices()
        if need_tip:
            self._list_tip_devices()
        
    def _list_tip_devices(self):
        device_list = []
        
        # 遍历 /dev 视频设备
        for video_node in sorted(os.listdir('/dev')):
            if video_node.startswith('video'):
                full_path = os.path.join('/dev', video_node)

                # 确保该路径确实存在
                if not os.path.exists(full_path):
                    continue
                
                try:
                    # 使用 udevadm 获取设备属性
                    output_serial = subprocess.check_output(
                        ['udevadm', 'info', '--query=property', '--name=' + full_path],
                        text=True,
                        stderr=subprocess.PIPE
                    )
                    
                    serial = None
                    capture = None
                    vendor = None

                    # 解析输出以查找序列号
                    for line in output_serial.strip().split('\n'):
                        if line.startswith('USEC_INITIALIZED='):
                            serial = line.split('=', 1)[1].strip()
                        elif line.startswith('ID_V4L_CAPABILITIES='):
                            capture = line.split('=', 1)[1].strip()
                        elif line.startswith('ID_VENDOR='):
                            vendor = line.split('=', 1)[1].strip()
                        
                    if capture == ":capture:" and vendor == "YJX-230927-K":
                        device_info = {
                            'serial': serial,
                            'device_path': full_path
                        }
                        device_list.append(device_info)
                     
                except subprocess.CalledProcessError:
                    # 某些 /dev/video* 设备可能不是实际的物理摄像头，忽略错误
                    print(f"Could not retrieve info for {full_path}. Skipping...")
                    continue

        return device_list        

    def _list_xense_devices(self):
        """
        使用 v4l2-ctl 列出设备，因为 udevadm 在此环境中缺失关键信息。
        解析格式示例:
        OG000209: Tactile Sensor V0.000 (usb-0000:80:14.0-8.1.2):
                /dev/video18
                /dev/video19
        """
        device_list = []
        try:
            # 使用 v4l2-utils 工具获取列表
            output = subprocess.check_output(['v4l2-ctl', '--list-devices'], text=True)
            
            current_serial = None
            is_target_device = False
            
            for line in output.split('\n'):
                line = line.strip('\n') # 保留前面的缩进用于判断
                
                if not line:
                    continue
                    
                # 如果行首不是制表符/空格，说明是设备名称行
                if not (line.startswith('\t') or line.startswith(' ')):
                    # 检查是否包含 Tactile Sensor 或符合 OGxxxx 格式
                    # 根据你的日志: "OG000209: Tactile Sensor V0.000..."
                    if "Tactile Sensor" in line or line.startswith("OG"):
                        # 提取冒号前的部分作为序列号
                        current_serial = line.split(':')[0].strip()
                        is_target_device = True
                        # self.logger.info(f"Found Xense Serial: {current_serial}")
                    else:
                        is_target_device = False
                        current_serial = None
                
                # 如果是设备路径行 (前面有空格或制表符)
                elif is_target_device and current_serial:
                    device_path = line.strip()
                    # 只要有效的 video 设备
                    if device_path.startswith('/dev/video'):
                        device_list.append({
                            'serial': current_serial,
                            'device_path': device_path
                        })
                        # 我们只需要每个序列号对应的第一个视频节点即可，
                        # 但为了保险，可以把它们都加进去，让后面的逻辑去匹配
                        
        except FileNotFoundError:
            self.logger.error("Error: 'v4l2-ctl' not found. Please install v4l2-utils (sudo apt install v4l2-utils)")
        except Exception as e:
            self.logger.error(f"Error parsing v4l2-ctl output: {e}")
            
        return device_list
    
    def _list_realsense_devices(self):
        """List available RealSense devices"""
        try:
            import pyrealsense2 as rs
            
            ctx = rs.context()
            devices = ctx.query_devices()
            
            if len(devices) == 0:
                self.logger.warning("🟡 No RealSense devices found")
                return
            
            self.logger.info(f"✅ Found {len(devices)} RealSense device(s):")
            
            for i, device in enumerate(devices):
                try:
                    serial_number = device.get_info(rs.camera_info.serial_number)
                    name = device.get_info(rs.camera_info.name)
                    firmware_version = device.get_info(rs.camera_info.firmware_version)
                    
                    self.logger.info(f"  [{i}] {name} (Serial: {serial_number}, FW: {firmware_version})")
                    
                except Exception as e:
                    self.logger.error(f"  [{i}] Error reading device info: {e}")
                    
        except ImportError:
            self.logger.warning("🟡 pyrealsense2 not available, cannot list RealSense devices")
        except Exception as e:
            self.logger.error(f"Error listing RealSense devices: {e}")
    
    def _list_video_devices(self):
        """List available video devices"""
        video_devices = []
        
        # Check /dev/video* devices
        video_paths = glob.glob('/dev/video*')
        video_paths.sort(key=lambda x: int(x.split('video')[-1]))  # Sort by number
        
        self.logger.info(f"📹 Checking {len(video_paths)} video devices...")
        
        for path in video_paths:
            try:
                # Get device index
                index = int(path.split('/dev/video')[-1])
                
                # Try to open device briefly to check if it's accessible
                cap = cv2.VideoCapture(index, cv2.CAP_V4L2)
                if not cap.isOpened():
                    cap = cv2.VideoCapture(index)
                    
                if cap.isOpened():
                    # Test if we can read a frame
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        # Get basic info
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        fps = cap.get(cv2.CAP_PROP_FPS)
                        
                        video_devices.append({
                            'path': path,
                            'index': index,
                            'resolution': f"{width}x{height}",
                            'fps': fps,
                            'frame_shape': frame.shape
                        })
                    cap.release()
                    
            except Exception as e:
                self.logger.debug(f"Cannot access {path}: {e}")
        
        if video_devices:
            self.logger.info(f"✅ Found {len(video_devices)} accessible video device(s):")
            for device in video_devices:
                self.logger.info(f"  {device['path']} - {device['resolution']} @ {device['fps']} FPS (Shape: {device['frame_shape']})")
        else:
            self.logger.warning("🟡 No accessible video devices found")
    
    def _initialize_cameras(self):
        """Initialize all configured cameras"""
        if not self.camera_configs:
            self.logger.warning("No cameras configured")
            return
        
        xense_devices = self._list_xense_devices()  # 获取 Xense 设备
        tip_devices = self._list_tip_devices()  # 获取 Tip 设备
            
        for camera_name, config in self.camera_configs.items():
            camera_type = config.get('type', 'realsense').lower()
            
            try:
                config["tk_root"] = self.tk_root

                if camera_type == 'realsense':
                    camera = RealSenseCamera(camera_name, config)
                    
                elif camera_type == 'xense':
                    found_device = False
                    
                    # 获取所有序列号以便查找
                    serial_numbers = [device['serial'] for device in xense_devices]

                    if config['serial'] in serial_numbers:
                        for device in xense_devices:
                            if device['serial'] == config['serial']:
                                config['device_path'] = device['device_path']
                                found_device = True  # 标记为找到设备
                                break
                    
                    if not found_device:
                        self.logger.warning(f"Xense camera {camera_name} with serial {config['serial']} not found. Skipping initialization.")
                        continue

                    camera = VideoCamera(camera_name, config)
                
                elif camera_type == 'tip':
                    found_device = False
                    
                    # 获取所有序列号以便查找
                    serial_numbers = [device['serial'] for device in tip_devices]

                    if config['serial'] in serial_numbers:
                        for device in tip_devices:
                            if device['serial'] == config['serial']:
                                config['device_path'] = device['device_path']
                                found_device = True  # 标记为找到设备
                                break
                    
                    if not found_device:
                        self.logger.warning(f"Tip camera {camera_name} with serial {config['serial']} not found. Skipping initialization.")
                        continue

                    camera = VideoCamera(camera_name, config)
                
                else:
                    self.logger.error(f"Unknown camera type '{camera_type}' for camera {camera_name}")
                    continue
                
                self.cameras[camera_name] = camera
                camera.start()
                self.logger.info(f"✅ Initialized {camera_type} camera: {camera_name}")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize camera {camera_name}: {e}")
    
    def stop_streaming(self):
        """Stop all cameras"""
        for name, camera in self.cameras.items():
            try:
                camera.stop()
                self.logger.info(f"Stopped camera: {name}")
            except Exception as e:
                self.logger.error(f"Failed to stop camera {name}: {e}")

        for name, count in self.camera_frame_counts.items():  
            self.logger.info(f"Camera {name}: Total frames acquired = {count}")  # 记录总帧数  

        # Destroy the main Tkinter root after all cameras are stopped
        if self.tk_root:
            if self.tk_root.winfo_exists(): # Check if the root window still exists
                try:
                    self.tk_root.update_idletasks() 
                    self.tk_root.quit() # This safely stops the mainloop if it's running
                    self.tk_root.destroy()
                    self.tk_root = None
                    self.logger.info("Destroyed main Tkinter root.")
                except tk.TclError as e:
                    self.logger.warning(f"Error destroying Tkinter root, might already be destroyed: {e}")

    
    def get_latest_frames(self) -> Dict[str, Dict]:
        """Get latest frames from all cameras"""
        frames = {}
        
        if not hasattr(self, 'camera_frame_counts'):
            self.camera_frame_counts = {}
        
        for name, camera in self.cameras.items():
            if name not in self.camera_frame_counts:
                self.camera_frame_counts[name] = 0  # 初始化计数器

            frame_data = camera.get_latest_frames()
            if frame_data:
                self.camera_frame_counts[name] += 1  # 增加计数  
                self.logger.debug(f"Camera {name}: Frame count = {self.camera_frame_counts[name]}")  # 记录日志  
                frames[name] = frame_data  
        return frames
    def get_and_reset_frame_counts(self) -> Dict[str, int]:  
        """Get and reset frame counts for all cameras"""  
        frame_counts = self.camera_frame_counts.copy()  # 获取当前帧数的副本  
         # 重置帧计数器  
        for name in self.camera_frame_counts:  
            self.camera_frame_counts[name] = 0  
        return frame_counts  

    def get_camera_info(self) -> Dict[str, Dict]:
        """Get information about all cameras"""
        info = {}
        for name, camera in self.cameras.items():
            info[name] = {
                'type': camera.__class__.__name__,
                'is_streaming': camera.is_streaming,
                'rgb_stream': camera.rgb_stream,
                'depth_stream': camera.depth_stream,
                'config': camera.config
            }
        return info
    
    @staticmethod
    def list_available_devices() -> Dict[str, List]:
        """Static method to list all available camera devices"""
        devices = {
            'realsense': [],
            'video': []
        }
        
        # List RealSense devices
        try:
            import pyrealsense2 as rs
            ctx = rs.context()
            rs_devices = ctx.query_devices()
            
            for device in rs_devices:
                serial = device.get_info(rs.camera_info.serial_number)
                name = device.get_info(rs.camera_info.name)
                devices['realsense'].append(f"{serial} - {name}")
        except Exception:
            pass
        
        # List video devices
        video_paths = glob.glob('/dev/video*')
        for path in sorted(video_paths, key=lambda x: int(x.split('video')[-1])):
            try:
                index = int(path.split('/dev/video')[-1])
                cap = cv2.VideoCapture(index)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        devices['video'].append(path)
                    cap.release()
            except Exception:
                pass
        
        return devices


def main():
    """Test function for camera manager"""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Sample configuration with different stream combinations
    config = {
        'cameras': {
            # RealSense camera with both RGB and depth
            # 'left_camera': {
            #     'type': 'realsense',
            #     'serial': '335522070753',  # 替换为实际序列号
            #     'rgb_stream': True,
            #     'depth_stream': True,
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'depth_scale': 0.001,
            #     'image_show': True
            # },
            
            # # RealSense camera with only RGB (example)
            # 'right_camera': {
            #     'type': 'realsense',
            #     'serial': '913522071103',
            #     'rgb_stream': True,
            #     'depth_stream': False,
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'image_show': True
            # },
            
            # # Video camera with only RGB (depth not supported)
            # 'left_tactile_left_camera': {
            #     'type': 'xense',
            #     'serial': "OG000228",
            #     'rgb_stream': True,
            #     'depth_stream': False,  # Video cameras don't have depth
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'image_show': True
            # },

            # 'left_tactile_right_camera': {
            #     'type': 'xense',
            #     'serial': "OG000209",
            #     'rgb_stream': True,
            #     'depth_stream': False,  # Video cameras don't have depth
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'image_show': True
            # },
            
            # 'right_tactile_left_camera': {
            #     'type': 'xense',
            #     'serial': "OG000409",
            #     'rgb_stream': True,
            #     'depth_stream': False,  # Video cameras don't have depth
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'image_show': True
            # },

            # 'right_tactile_right_camera': {
            #     'type': 'xense',
            #     'serial': "OG000155",
            #     'rgb_stream': True,
            #     'depth_stream': False,  # Video cameras don't have depth
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30,
            #     'image_show': True
            # }
            
            'right_tip_camera': {
                'type': 'tip',
                'serial': "9309040246",
                'rgb_stream': True,
                'depth_stream': False,  # Video cameras don't have depth
                'width': 640,
                'height': 480,
                'fps': 30,
                'image_show': True
            },

            'left_tip_camera': {
                'type': 'tip',
                'serial': "9318432533",
                'rgb_stream': True,
                'depth_stream': False,  # Video cameras don't have depth
                'width': 640,
                'height': 480,
                'fps': 30,
                'image_show': True
            }
            
            
            # Video camera trying to enable depth (will show warning)
            # 'webcam': {
            #     'type': 'video',
            #     'device_index': 2,
            #     'rgb_stream': True,
            #     'depth_stream': True,  # Will warn and return None for depth
            #     'width': 640,
            #     'height': 480,
            #     'fps': 30
            # }
        }
    }
    
    print("🚀 Starting Camera Manager Test with Stream Configuration")
    print("="*60)
    
    manager = None
    
    try:
        # Create camera manager
        manager = CameraManager(config['cameras'])
        while True:
            time.sleep(0.5)

        frame_counts = manager.get_and_reset_frame_counts()  
        print("Episode finished!")  
        for name, count in frame_counts.items():  
            print(f"Camera {name}: Frames in episode = {count}")  

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        if manager is not None:
            manager.stop_streaming()
        cv2.destroyAllWindows()
        print("✅ Cleanup completed")
    
    # List all available devices
    print("\n📋 Available devices:")
    devices = CameraManager.list_available_devices()
    for device_type, device_list in devices.items():
        print(f"  {device_type.upper()}:")
        if device_list:
            for device in device_list:
                print(f"    - {device}")
        else:
            print(f"    - None found")


if __name__ == "__main__":
    main()
