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
from typing import Dict, List, Optional, Tuple, Any
from collections import deque
import logging
import copy
from datetime import datetime
from pathlib import Path
import yaml
import queue
from dataclasses import dataclass, field

import numpy as np
import gc
import weakref
import psutil

from .camera_manager import CameraManager
from .teleopt_subscriber import TeleOptSubscriber
from .robot_controller import RobotController
from .lerobot_formatter import LeRobotFormatter
import ctypes
libc = ctypes.CDLL("libc.so.6")
# 🔥🔥🔥 加入这几行调试代码 🔥🔥🔥
import inspect
import os
print("\n" + "!"*60)
print(f"🕵️ [DEBUG] 正在使用的 RobotController 文件路径:")
print(inspect.getfile(RobotController))
print("!"*60 + "\n")
# 🔥🔥🔥 结束调试代码 🔥🔥🔥
@dataclass
class FrameData:
    """Enhanced data structure for a single frame compatible with LeRobot v3.0"""
    timestamp: float
    frame_index: int
    episode_index: int
    images: Dict[str, np.ndarray] = field(default_factory=dict)
    robot_states: Dict[str, Dict] = field(default_factory=dict)
    actions: Dict[str, np.ndarray] = field(default_factory=dict)
    task_info: Optional[Dict] = None
    metadata: Optional[Dict] = None


@dataclass
class EpisodeData:
    """Enhanced data structure for a complete episode"""
    episode_index: int
    frames: List[FrameData]
    start_time: float
    end_time: float
    metadata: Dict = field(default_factory=dict)
    
    @property
    def duration(self) -> float:
        return self.end_time - self.start_time
    
    @property
    def frame_count(self) -> int:
        return len(self.frames)


class DataRecorder:
    """Enhanced data recorder for multi-robot teleoperation with LeRobot v3.0 dataset support"""
    
    def __init__(self, config_path: str):
        """Initialize data recorder with configuration file path"""
        self.config = self._load_config(config_path)
        # frame counters
        self.camera_frame_counts = {}
        # 初始化每个相机的计数器  
        for camera_name in self.config.get('cameras', {}):  
            self.camera_frame_counts[camera_name] = {  
                'color': 0,  
                'depth': 0,  
                'total': 0  
            }  
        
        self.original_config = copy.deepcopy(self.config)
        self.setup_logging()

        # Recording state
        self.is_recording = False
        self.recording_lock = threading.RLock()
        
        # Current recording buffer with enhanced structure
        self.current_episode_frames: List[FrameData] = []
        self.current_episode_start_time = 0
        
        # Save queue for background saving with priority
        self.save_queue = queue.PriorityQueue()
        self._chunk_counter = 0
        self.save_thread = None
        self.stop_save_thread = threading.Event()
        self.save_stats = {'saved': 0, 'failed': 0, 'queue_size': 0}
        
        # Recording timing with adaptive control
        self.recording_fps = self.config['recording'].get('fps', 30)
        self.recording_interval = 1.0 / self.recording_fps
        self.last_record_time = 0
        self.actual_fps_tracker = deque(maxlen=100)
        
        # Recording thread with enhanced control
        self.recording_thread = None
        self.stop_recording_event = threading.Event()
        
        # Buffer size management
        self.max_buffer_size = self.config['recording'].get('buffer_size', 1000)
        self.buffer_warning_threshold = int(self.max_buffer_size * 0.8)

                # 性能监控  
        self.performance_stats = {} 

        # --- 新增：内存监控器初始化 ---  
        self.memory_monitor_config = self.config.get('memory_monitor', {})  
        self.process = psutil.Process()  # 获取当前进程对象  
        self.memory_monitor_thread = None  
        self.stop_memory_monitor = threading.Event()  
        if self.memory_monitor_config.get('enabled', False):  
            self._start_memory_monitor()  
        
        # Performance monitoring
        self.performance_stats = {
            'frames_recorded': 0,
            'frames_dropped': 0,
            'avg_record_time': 0,
            'max_record_time': 0
        }


        
        # Initialize components
        self._initialize_components()
        
        # Start save thread
        self._start_save_thread()

        # 启动周期性清理线程
        self._start_periodic_cleanup()
        
        self.logger.info(f"DataRecorder initialized with {self.recording_fps} FPS, buffer size: {self.max_buffer_size}")
        self.logger.info(f"Starting episode counter at: {self.episode_counter}")

    def _start_memory_monitor(self):  
        """启动用于监控内存使用的后台线程。"""  
        if not self.memory_monitor_config.get('enabled', False):  
            return  

        self.stop_memory_monitor.clear()  
        self.memory_monitor_thread = threading.Thread(target=self._memory_monitor_loop, daemon=True, name="MemoryMonitor")  
        self.memory_monitor_thread.start()  
        self.logger.info("系统内存监控器已启动。")  

    def _memory_monitor_loop(self):  
        """内存监控线程的主循环。"""  
        interval = self.memory_monitor_config.get('check_interval_seconds', 5)  
        warn_threshold = self.memory_monitor_config.get('warning_threshold_percent', 75.0)  
        crit_threshold = self.memory_monitor_config.get('critical_threshold_percent', 85.0)  

        self.logger.info(f"内存监控配置：警告阈值 {warn_threshold}%, 临界阈值 {crit_threshold}%")  

        while not self.stop_memory_monitor.is_set():  
            try:  
                # 获取系统全局的虚拟内存使用情况  
                mem_info = psutil.virtual_memory()  
                mem_percent_used = mem_info.percent  
                
                # 你也可以只监控当前进程的内存占用（单位：MB）  
                # process_mem_mb = self.process.memory_info().rss / (1024 * 1024)  

                if mem_percent_used >= crit_threshold:  
                    self.logger.critical(  
                        f"内存临界警报：系统内存使用率 {mem_percent_used:.1f}%, "  
                        f"已超过临界阈值 {crit_threshold}%。正在采取紧急措施！"  
                    )  
                    self._handle_critical_memory()  
                    # 发生临界事件后，等待更长时间再检查，给系统恢复的时间  
                    time.sleep(interval * 3)  
                
                elif mem_percent_used >= warn_threshold:  
                    self.logger.warning(  
                        f"高内存使用警告：系统内存使用率 {mem_percent_used:.1f}%, "  
                        f"已超过警告阈值 {warn_threshold}%。正在触发深度清理。"  
                    )  
                    self._handle_warning_memory()  
                
                else:  
                     self.logger.debug(f"内存使用率正常：{mem_percent_used:.1f}%")  

            except Exception as e:  
                self.logger.error(f"内存监控循环出错: {e}")  

            time.sleep(interval)  

    def _handle_warning_memory(self):  
        """处理高内存使用（警告级别）的措施。"""  
        self.logger.info("因内存压力过高，正在执行深度清理...")  
        # 强制执行一轮完整的垃圾回收  
        gc.collect()  
        gc.collect()  
        gc.collect()  
        # 强制清理相机和 formatter 的缓存  
        self._force_camera_cleanup()  
        if hasattr(self, 'lerobot_formatter'):  
            self.lerobot_formatter._cleanup_memory_caches()  
        # 建议操作系统回收未使用的内存（仅Linux有效）  
        libc.malloc_trim(0)  
        self.logger.info("深度清理完成。")  

    def _handle_critical_memory(self):  
        """处理临界内存使用的措施。"""  
        with self.recording_lock:  
            if not self.is_recording:  
                self.logger.info("收到临界内存警报，但当前未在录制。仅执行清理。")  
                self._handle_warning_memory() # 仍然执行清理  
                return  

            self.logger.warning("因内存达到临界值，正在暂停录制并强制保存当前片段。")  
            
            # 1. 停止录制循环  
            self._stop_recording_internal()  

            # 2. 将当前缓冲区的数据放入队列等待保存（此操作也会清空缓冲区）  
            self._queue_current_episode_for_save()  
            
            # 3. 执行深度清理  
            self._handle_warning_memory()  

            self.logger.critical("录制已暂停且数据已保存。可能需要操作员介入以恢复录制。")  
            # 注意：此逻辑故意不自动重启录制。  
            # 临界内存事件非常严重，应由人工（例如通过遥操作手柄）发送新的开始命令来恢复。  

    def _start_periodic_cleanup(self):
        """启动周期性清理线程 - 每20秒强制清理一次"""
        def cleanup_loop():
            while not self.stop_save_thread.is_set():
                try:
                    time.sleep(20)  # 每20秒清理一次
                    
                    # 🔥 强制垃圾回收
                    collected = gc.collect()
                    
                    # 🔥 清理相机缓存
                    self._force_camera_cleanup()
                    
                    # 🔥 清理 lerobot_formatter 缓存
                    if hasattr(self, 'lerobot_formatter'):
                        self.lerobot_formatter._cleanup_memory_caches()
                    
                    # 记录内存使用
                    try:
                        import psutil
                        process = psutil.Process()
                        memory_mb = process.memory_info().rss / 1024 / 1024
                        self.logger.info(f"🧹 Periodic cleanup: collected={collected}, memory={memory_mb:.1f}MB")
                    except:
                        self.logger.info(f"🧹 Periodic cleanup: collected={collected} objects")
                        
                except Exception as e:
                    self.logger.error(f"Error in periodic cleanup: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True, name="PeriodicCleanup")
        cleanup_thread.start()
        self.logger.info("Periodic cleanup thread started (20s interval)")

    def _get_next_episode_counter(self) -> int:
        """检查现有数据并返回下一个episode计数器"""
        try:
            dataset_path = self._create_dataset_path()
            
            # 如果数据集路径不存在，从0开始
            if not dataset_path.exists():
                self.logger.info("No existing dataset found, starting from episode 0")
                return 0
            
            max_episode_index = -1
            
            # 检查data目录下的所有chunk
            data_base_path = dataset_path / 'data'
            if data_base_path.exists():
                # 遍历所有chunk目录
                for chunk_dir in data_base_path.glob('chunk-*'):
                    if not chunk_dir.is_dir():
                        continue
                        
                    # 遍历chunk目录下的parquet文件
                    for parquet_file in chunk_dir.glob('file_*.parquet'):
                        try:
                            import pandas as pd
                            df = pd.read_parquet(parquet_file)
                            
                            # 检查是否有episode_index列
                            if 'episode_index' in df.columns:
                                chunk_max = df['episode_index'].max()
                                if not pd.isna(chunk_max):
                                    max_episode_index = max(max_episode_index, int(chunk_max))
                                    
                        except Exception as e:
                            self.logger.warning(f"Error reading {parquet_file}: {e}")
                            continue
            
            # 检查meta/episodes目录
            meta_episodes_path = dataset_path / 'meta' / 'episodes'
            if meta_episodes_path.exists():
                for chunk_dir in meta_episodes_path.glob('chunk-*'):
                    if not chunk_dir.is_dir():
                        continue
                        
                    for parquet_file in chunk_dir.glob('file_*.parquet'):
                        try:
                            import pandas as pd
                            df = pd.read_parquet(parquet_file)
                            
                            if 'episode_index' in df.columns:
                                chunk_max = df['episode_index'].max()
                                if not pd.isna(chunk_max):
                                    max_episode_index = max(max_episode_index, int(chunk_max))
                                    
                        except Exception as e:
                            self.logger.warning(f"Error reading episodes metadata {parquet_file}: {e}")
                            continue
            
            # 返回下一个episode索引
            next_counter = max_episode_index + 1
            self.logger.info(f"Found existing data, max episode index: {max_episode_index}, next counter: {next_counter}")
            return next_counter
            
        except Exception as e:
            self.logger.warning(f"Error checking existing episodes, starting from 0: {e}")
            return 0

    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def setup_logging(self):
        """Setup enhanced logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Add file handler for recording logs
        log_dir = Path(self.config['output']['base_dir']) / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
    def _initialize_components(self):
        """Initialize all components with enhanced error handling"""
        try:
            # Initialize camera manager
            self.logger.info("Initializing camera manager...")
            self.camera_manager = CameraManager(self.config.get('cameras', {}))

            # Initialize robot controller
            self.logger.info("Initializing robot controller...")
            self.robot_controller = RobotController(self.config.get('robot', {}))
            
            # Initialize teleoperation subscriber
            self.logger.info("Initializing teleoperation subscriber...")
            teleop_config = self.config.get('teleoperation', {})
            self.teleop_subscriber = TeleOptSubscriber(teleop_config)
            
            # Register callback for teleoperation commands
            self.teleop_subscriber.register_callback(self._on_teleopt_cmd)
            
            # Initialize LeRobot formatter
            self.logger.info("Initializing LeRobot formatter...")  
            lerobot_config = self.config.get('lerobot', {})  
            merged_config = {**self.config, **lerobot_config}  
            self.lerobot_formatter = LeRobotFormatter(merged_config)  
            self.episode_counter = self.lerobot_formatter.starting_episode_idx  
            
            # Store current teleop messages for each arm
            self.current_teleop_msgs = {}
            
            # Get arm names from config
            self.arm_names = list(self.config.get('robot', {}).keys())
            
            self.logger.info(f"All components initialized successfully. Arms: {self.arm_names}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
            
    def _start_save_thread(self):
        """Start enhanced background save thread"""
        self.stop_save_thread.clear()
        self.save_thread = threading.Thread(target=self._save_worker, daemon=True)
        self.save_thread.start()
        self.logger.info("Enhanced background save thread started")
        
    def _save_worker(self):
        """Enhanced background worker for saving episodes"""
        while not self.stop_save_thread.is_set():
            try:
                # Get save task with timeout (priority queue returns (priority, episode_data))
                priority, chunk_counter,episode_data = self.save_queue.get(timeout=1.0)
                
                # Update queue size stat
                self.save_stats['queue_size'] = self.save_queue.qsize()
                
                episode_idx = episode_data.episode_index
                self.logger.info(f"Starting to save episode {episode_idx} ({episode_data.frame_count} frames)")
                
                # Create dataset directory structure following LeRobot v3.0
                dataset_path = self._create_dataset_path()
                data_dir = dataset_path

                # Save using LeRobot formatter
                save_start_time = time.time()
                # self.lerobot_formatter.save_episode(
                #     episode_data.frames,
                #     episode_idx,
                #     data_dir,
                #     video_dir
                # )
                self.lerobot_formatter.save_episode(episode_data)

                save_duration = time.time() - save_start_time
                
                self.save_stats['saved'] += 1
                self.logger.info(f"Episode {episode_idx} saved successfully in {save_duration:.2f}s")
                
                frames = episode_data.frames
                for frame in frames:
                    # 显式清空内部的字典，并删除其中的 numpy 数组引用
                    if hasattr(frame, 'images'):
                        for img_name in list(frame.images.keys()):
                            img_array = frame.images.pop(img_name) # 弹出并删除
                            if isinstance(img_array, np.ndarray):
                                del img_array
                        frame.images.clear() # 确保清空
                    
                    if hasattr(frame, 'robot_states'):
                        for state_name in list(frame.robot_states.keys()):
                            state_data = frame.robot_states.pop(state_name) # 弹出并删除
                            del state_data
                        frame.robot_states.clear()
                        
                    if hasattr(frame, 'actions'):
                        for action_name in list(frame.actions.keys()):
                            action_data = frame.actions.pop(action_name) # 弹出并删除
                            del action_data
                        frame.actions.clear()
                frames.clear()
                del frames
                del episode_data
                gc.collect()

                # Mark task done
                self.save_queue.task_done()

                # 🔥 强制释放未使用的内存
                libc.malloc_trim(0)
                
            except queue.Empty:
                continue
            except Exception as e:
                self.save_stats['failed'] += 1
                self.logger.error(f"Error in save worker: {e}")
                if 'episode_data' in locals():
                    del episode_data
                gc.collect()
                
    def _create_dataset_path(self) -> Path:
        """Create dataset directory path"""
        base_dir = Path(self.config['output']['base_dir'])
        dataset_name = self.config['output']['dataset_name']
        return base_dir / dataset_name
        
    def _start_performance_monitor(self):
        """Start performance monitoring thread"""
        def performance_monitor():
            while not self.stop_recording_event.is_set():
                time.sleep(10)  # Report every 10 seconds
                
                if self.is_recording:
                    actual_fps = len(self.actual_fps_tracker) / 10 if self.actual_fps_tracker else 0
                    buffer_usage = len(self.current_episode_frames) / self.max_buffer_size * 100
                    
                    self.logger.info(f"Performance: FPS={actual_fps:.1f}, Buffer={buffer_usage:.1f}%, "
                                   f"Recorded={self.performance_stats['frames_recorded']}, "
                                   f"Dropped={self.performance_stats['frames_dropped']}")
                    
                    # Clear FPS tracker for next interval
                    self.actual_fps_tracker.clear()
        
        monitor_thread = threading.Thread(target=performance_monitor, daemon=True)
        monitor_thread.start()
        
    def _on_teleopt_cmd(self, event_type: str, arm_name: str, msg):
        """Enhanced callback for TeleOptCmd messages with event type and arm name"""
        # Update current teleop message for the arm
        if msg is not None:
            self.current_teleop_msgs[arm_name] = msg
        
        # Handle different event types based on teleopt_subscriber.py states
        if event_type == 'start_recording':
            self.logger.info(f"📹 Received start_recording event from {arm_name}")
            # start_recording会自动处理缓存清理
            self.start_recording()
            
        elif event_type == 'stop_and_save_recording':
            self.logger.info(f"💾 Received stop_and_save event from {arm_name}")  
            # 调用 stop_recording()，它的默认行为就是停止并保存  
            self.stop_recording()   
            
        elif event_type == 'stop_and_discard_recording': # 👈 2. 新增一个专门用于丢弃的事件  
            self.logger.info(f"🗑️ Received stop_and_discard event from {arm_name}")  
            # 调用 discard_current_episode() 方法来处理丢弃逻辑  
            self.discard_current_episode()  
            
        # 备注：下面这个 'save' 事件可以保留，它用于录制过程中的“手动分块保存”，不终止录制  
        elif event_type == 'save':  
            self.logger.info(f"💾 Received manual chunk save event from {arm_name}")  
            self._queue_current_episode_for_save()  
            
        else:  
            # 如果收到旧的 'stop_recording' 事件，打印一个警告，提示逻辑需要更新  
            if event_type == 'stop_recording':  
                 self.logger.warning(f"Received legacy 'stop_recording' event. Logic should be updated to use 'stop_and_save_recording' or 'stop_and_discard_recording'. Defaulting to save.")  
                 self.stop_recording()  
            else:  
                pass  


    def start_recording(self):
        """Start recording with enhanced initialization and cache clearing"""
        with self.recording_lock:
            # 如果正在录制，先停止
            if self.is_recording:
                self.logger.warning("Already recording, stopping current and starting new")
                self._stop_recording_internal()

            # 🔥 在开始新录制前，强制清理相机缓存
            self._force_camera_cleanup()

            # 重要：清空当前缓存数据，确保新录制不受影响
            if self.current_episode_frames:
                self.logger.info(f"Clearing {len(self.current_episode_frames)} frames from previous session")
                self.current_episode_frames.clear()
                
            # Initialize new episode
            self.current_episode_frames = []
            self.current_frame_index = 0
            self.current_episode_start_time = time.time()
            
            # Reset performance tracking
            self.performance_stats = {
                'frames_recorded': 0,
                'frames_dropped': 0,
                'avg_record_time': 0,
                'max_record_time': 0
            }
            
            # Reset timing
            self.last_record_time = time.time()
            
            # Start recording
            self.is_recording = True
            
            # Start recording thread
            self.stop_recording_event.clear()
            self.recording_thread = threading.Thread(target=self._recording_loop, daemon=True)
            self.recording_thread.start()
            
            # 🔥 强制垃圾回收
            gc.collect()
            
            self.logger.info(f"🎬 Started recording episode {self.episode_counter} (cache cleared)")

    def _queue_current_episode_for_save(self):
        """将当前episode数据提交到保存队列，但不停止录制"""
        with self.recording_lock:
            # 检查是否有数据需要保存
            if not self.current_episode_frames:
                self.logger.warning("No data to save")
                return
                
            # 创建episode数据的深拷贝，避免后续修改影响保存
            frames_to_save = self.current_episode_frames
            self.current_episode_frames = []
            
            frame_counts = {}  
            for frame in self.current_episode_frames:  
                for camera_name in frame.images.keys():  
                    if camera_name not in frame_counts:  
                       frame_counts[camera_name] = 0  
                    frame_counts[camera_name] += 1  
            self.logger.info(f"Frame counts before EpisodeData creation: {frame_counts}")  

            episode_data = EpisodeData(
                episode_index=self.episode_counter,
                frames=frames_to_save,
                start_time=self.current_episode_start_time,
                end_time=time.time(),
                metadata={
                    'config': self.original_config,
                    'performance_stats': self.performance_stats,
                    'save_timestamp': datetime.now().isoformat(),
                    'save_trigger': 'manual_save_event'
                }
            )
            
            # 添加到优先队列进行后台保存
            priority = 0  # High priority for manual saves
            self.save_queue.put((priority, episode_data))
            
            # 立即清空当前缓存，释放内存
            self.current_episode_frames.clear()
            self.current_frame_index = 0
            
            # 强制垃圾回收
            gc.collect()

            frame_count = len(frames_to_save)
            duration = episode_data.duration
            
            self.logger.info(f"💾 Episode {self.episode_counter} queued for background save "
                        f"({frame_count} frames, {duration:.2f}s)")
            
            # 重要：递增episode计数器，为下一个episode准备
            self.episode_counter += 1
            
    def stop_recording(self):  
        """Stops the recording and queues any remaining frames for a final save."""  
        if not self.is_recording:  
            self.logger.warning("Recording is not currently active.")  
            return  

        with self.recording_lock:  
            self.is_recording = False  
            self.stop_recording_event.set()  
            
            # 等待录制循环线程结束  
            if self.recording_thread and self.recording_thread.is_alive():  
                self.recording_thread.join(timeout=2)  

            self.logger.info(f"Recording stopped for episode {self.episode_counter}. Queueing final frames...")  

            # --- 核心修改：保存最后剩余的帧 ---  
            # 检查 current_episode_frames 中是否还有未被分块保存的剩余数据  
            if self.current_episode_frames:  
                self.logger.info(f"Found {len(self.current_episode_frames)} remaining frames in buffer. Saving as final chunk.")  
                
                # 使用相同的分块逻辑来保存最后一部分  
                final_chunk_data = EpisodeData(  
                    episode_index=self.episode_counter,  
                    frames=self.current_episode_frames,  
                    start_time=self.current_episode_start_time,  
                    end_time=time.time(),  
                    metadata={'save_trigger': 'final_stop'}  
                )  
                
                # 使用最高优先级（0）放入队列，确保它被优先处理  
                self.save_queue.put((0, self._chunk_counter,final_chunk_data))  
                self._chunk_counter += 1
                
                self.current_episode_frames = [] # 清空 
                self.episode_counter += 1
                 
            else:  
                self.logger.info("No remaining frames in buffer. Final save not needed.") 

            # 增加 episode 计数器，为下一次录制做准备  
            #  记录相机帧数
            self._log_camera_frame_counts()

            self.logger.info(f"All data for episode {self.episode_counter - 1} is queued. Ready for next recording.")  
            
    def _log_camera_frame_counts(self):  
        """记录每个相机的帧计数"""  
        self.logger.info("📸 Camera Frame Count Summary:")  
        for camera_name, counts in self.camera_frame_counts.items():  
            self.logger.info(  
                f"Camera {camera_name}: "  
                f"🖼️ Color Frames: {counts['color']}, "  
                f"📊 Depth Frames: {counts['depth']}, "  
                f"📈 Total Frames: {counts['total']}"  
            )  

    def _stop_recording_internal(self):
        """Internal method to stop recording with detailed logging"""
        if not self.is_recording:
            self.logger.warning("Not currently recording")
            return
            
        # Stop recording
        self.is_recording = False
        self.stop_recording_event.set()
        
        # Wait for recording thread to finish
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2.0)
            
        frame_count = len(self.current_episode_frames)
        duration = time.time() - self.current_episode_start_time if self.current_episode_start_time else 0
        
        # 🔥 新增：强制清理相机缓存
        self._force_camera_cleanup()

        self.logger.info(f"⏹️ Stopped recording episode {self.episode_counter}: "
                        f"{frame_count} frames, {duration:.2f}s")

    def _force_camera_cleanup(self):
        """强制清理相机内存缓存"""
        try:
            if hasattr(self, 'camera_manager') and self.camera_manager:
                for camera_name, camera in self.camera_manager.cameras.items():
                    with camera.frame_lock:
                        # 显式删除引用，并将其设置为 None
                        if camera.latest_frames['color'] is not None:
                            del camera.latest_frames['color']
                            camera.latest_frames['color'] = None
                        if camera.latest_frames['depth'] is not None:
                            del camera.latest_frames['depth']
                            camera.latest_frames['depth'] = None
                        
                        # 🔥 尝试清理显示相关的引用（如果存在）
                        if hasattr(camera, 'label') and camera.label:
                            camera.label.imgtk = None # 解除 Tkinter Image 引用
            
            # 强制垃圾回收
            gc.collect()
            gc.collect()
            gc.collect()
        except Exception as e:
            self.logger.warning(f"Error cleaning camera memory: {e}")

    def _recording_loop(self):  
        """Enhanced main recording loop with adaptive timing and auto-chunking."""  
        self.logger.info("Enhanced recording loop started with auto-chunking")  
        
        # 自动分块的阈值，例如设置为内存缓冲区的75%  
        # 这样可以在缓冲区完全满之前就开始保存，留出余地  
        chunk_threshold = int(self.max_buffer_size * 0.75)  
        self.logger.info(f"Auto-chunking enabled. Threshold set to {chunk_threshold} frames.")  
        
        while not self.stop_recording_event.is_set() and self.is_recording:  
            try:  
                loop_start_time = time.time()  
                
                # 使用 self.recording_interval 来控制帧率  
                if loop_start_time - self.last_record_time >= self.recording_interval:  
                    if self._record_frame():  
                        self.performance_stats['frames_recorded'] += 1  
                        self.actual_fps_tracker.append(time.time())  
                    else:  
                        # _record_frame 返回 False 通常意味着帧被丢弃  
                        self.performance_stats['frames_dropped'] += 1  
                    
                    self.last_record_time = loop_start_time  
                
                # --- 核心修改：检查并触发现场自动分块保存 ---  
                if len(self.current_episode_frames) >= chunk_threshold:  
                    self.logger.info(f"Buffer reached chunk threshold ({len(self.current_episode_frames)} frames). Queuing for background save...")  
                    # 调用新的辅助方法来处理分块  
                    self._queue_current_chunk_for_save()  

                # 自适应休眠，以维持目标帧率  
                loop_duration = time.time() - loop_start_time  
                if loop_duration < self.recording_interval:  
                    sleep_time = self.recording_interval - loop_duration  
                    time.sleep(max(0.001, sleep_time)) # 确保至少休眠一点时间，避免CPU空转  
                    
            except Exception as e:  
                self.logger.error(f"FATAL Error in recording loop: {e}", exc_info=True)  
                # 循环中出现严重错误，最好停止录制  
                self.stop_recording(save=False)  
                
        self.logger.info("Recording loop has gracefully stopped.")  

    def _queue_current_chunk_for_save(self):  
        """  
        Packages the current frame buffer as a 'chunk' and queues it for saving.  
        This method operates under the recording_lock.  
        """  
        with self.recording_lock:  
            if not self.current_episode_frames:  
                # 如果在锁定期间缓冲区被清空，则直接返回  
                return  

            # 1. 转移数据：将当前缓冲区的内容移动到一个新列表  
            frames_to_save = self.current_episode_frames  
            
            # 2. 清空缓冲区：这是关键！重置内存中的缓冲区，为新数据腾出空间  
            self.current_episode_frames = []  
            
            # 3. 打包数据块：创建一个 EpisodeData 对象，它代表一个数据块而非整个片段  
            # episode_index 保持不变，表明所有块都属于同一个逻辑片段  
            chunk_data = EpisodeData(  
                episode_index=self.episode_counter,  
                frames=frames_to_save,  
                start_time=self.current_episode_start_time, # 使用片段的起始时间  
                end_time=time.time(), # 块的结束时间是当前时间  
                metadata={'save_trigger': 'auto_chunk', 'chunk_frame_count': len(frames_to_save)}  
            )  
            
            # 4. 放入队列：将数据块放入保存队列，让后台线程处理  
            # 使用优先级 1，低于手动停止录制时的最终保存（优先级 0）  
            self.save_queue.put((1, self._chunk_counter, chunk_data))  
            self._chunk_counter += 1  
            
            frame_count = len(frames_to_save)  
            self.logger.info(f"Auto-chunk of {frame_count} frames for episode {self.episode_counter} queued. Buffer reset.")  
            
            # 5. 建议垃圾回收：帮助Python更快地回收 `frames_to_save` 列表所占用的内存  
            gc.collect()  
        
    def _record_frame(self) -> bool:  
        """Enhanced frame recording with deep copy and correct exception handling."""

        if len(self.current_episode_frames) >= self.max_buffer_size:  
            self.logger.error("Buffer full, dropping frame")  
            return False  

        if len(self.current_episode_frames) >= self.buffer_warning_threshold:  
            self.logger.warning(f"Buffer usage high: {len(self.current_episode_frames)}/{self.max_buffer_size}")  

        try:  
            timestamp = time.time()  
            
            camera_frames = self.camera_manager.get_latest_frames()  
            if not camera_frames:  
                self.logger.warning("No camera frames available, skipping frame")  
                return False  

            images = {}  
            for camera_name, frame_data_dict in camera_frames.items():  
                if not frame_data_dict:  
                    continue  
                if camera_name not in self.camera_frame_counts:  
                    self.camera_frame_counts[camera_name] = {'color': 0, 'depth': 0, 'total': 0}

                if 'color' in frame_data_dict and frame_data_dict['color'] is not None:  
                    images[camera_name] = frame_data_dict['color'].copy() 
                    self.logger.debug(f"Camera {camera_name}: color frame recorded")
                    self.camera_frame_counts[camera_name]['color'] += 1 
                    self.camera_frame_counts[camera_name]['total'] += 1
                else:
                    self.logger.warning(f"Camera {camera_name}: no color frame available")

                if 'depth' in frame_data_dict and frame_data_dict['depth'] is not None:  
                    depth_key = f"{camera_name}_depth" if not camera_name.endswith('_depth') else camera_name  
                    images[depth_key] = frame_data_dict['depth'].copy()  
                    self.camera_frame_counts[camera_name]['depth'] += 1
                    self.camera_frame_counts[camera_name]['total'] += 1 

            if not images:  
                self.logger.warning("No valid images captured for this frame.")  
                return False  

            self.logger.debug(f"Images captured: {images.keys()}") # 添加日志

            robot_states = self.robot_controller.get_all_states().copy()  
            if not robot_states:  
                self.logger.debug("No robot states available")  

            frame_data = FrameData(  
                timestamp=timestamp,  
                frame_index=self.current_frame_index,  
                episode_index=self.episode_counter,  
                images=images,  
                robot_states=robot_states,  
                task_info={'task': self.config.get('task', 'unknown')},  
                metadata={'actual_timestamp': timestamp}  
            )  
            
            self.current_episode_frames.append(frame_data)  
            self.current_frame_index += 1  

            if self.current_frame_index % 100 == 0:  
                self.logger.debug(f"Recorded {self.current_frame_index} frames for episode {self.episode_counter}")  

        except Exception as e:  
            self.logger.error(f"Error during _record_frame execution: {e}", exc_info=True)  
            if 'images' in locals(): del images  
            if 'robot_states' in locals(): del robot_states  
            if 'camera_frames' in locals(): del camera_frames  
            return False  

        return True  
            

    def _extract_all_camera_images(self, camera_frames: Dict, images: Dict):
        """Extract all available image data (color + depth) from camera frames"""
        
        for camera_name, frame_data in camera_frames.items():
            if not frame_data:
                self.logger.debug(f"No frame data for camera: {camera_name}")
                continue
            
            # Extract color image
            if 'color' in frame_data and frame_data['color'] is not None:
                color_image = frame_data['color']
                
                # Validate color image
                if isinstance(color_image, np.ndarray) and color_image.size > 0:
                    images[f"{camera_name}"] = color_image
                    self.camera_frame_counts[camera_name]['color'] += 1
                    self.camera_frame_counts[camera_name]['total'] += 1
                    

            # Extract depth image (if available)
            if 'depth' in frame_data and frame_data['depth'] is not None:
                depth_image = frame_data['depth']
                
                # Validate depth image
                if isinstance(depth_image, np.ndarray) and depth_image.size > 0:
                    # Use separate key for depth data
                    images[f"{camera_name}_depth"] = depth_image
                    self.camera_frame_counts[camera_name]['depth'] += 1
                    self.camera_frame_counts[camera_name]['total'] += 1
                                
            # Extract timestamp info for validation
            if 'timestamp' in frame_data:
                frame_timestamp = frame_data['timestamp']
                current_time = time.time()
                age = current_time - frame_timestamp
                
                # Warn if frame is too old (>100ms)
                if age > 0.1:
                    self.logger.warning(f"⚠️ {camera_name} frame is {age*1000:.1f}ms old")


    def _extract_action_from_teleop(self, teleop_msg) -> Optional[np.ndarray]:
        """Extract action array from teleoperation message"""
        try:
            action_components = []
            
            # Extract pose (position + orientation)
            if hasattr(teleop_msg, 'target_pose') or hasattr(teleop_msg, 'hand_pose'):
                pose = getattr(teleop_msg, 'target_pose', None) or getattr(teleop_msg, 'hand_pose', None)
                if pose:
                    # Position
                    if hasattr(pose, 'position'):
                        action_components.extend([pose.position.x, pose.position.y, pose.position.z])
                    # Orientation (quaternion)
                    if hasattr(pose, 'orientation'):
                        action_components.extend([
                            pose.orientation.x, pose.orientation.y,
                            pose.orientation.z, pose.orientation.w
                        ])
            
            # Extract gripper command
            if hasattr(teleop_msg, 'gripper_cmd'):
                action_components.append(float(teleop_msg.gripper_cmd))
            else:
                action_components.append(0.0)  # Default gripper value
            
            if action_components:
                return np.array(action_components, dtype=np.float32)
            
        except Exception as e:
            self.logger.debug(f"Error extracting action: {e}")
        
        return None
            
    def save_current_episode(self):
        """Enhanced episode saving - 兼容原有接口，但使用新的队列机制"""
        with self.recording_lock:
            # 如果正在录制，先停止
            if self.is_recording:
                self.logger.info("Stopping recording for save operation")
                self._stop_recording_internal()
                
            # 使用队列保存机制
            self._queue_current_episode_for_save()
            
            # 清空当前缓存
            self.current_episode_frames = []
            self.current_frame_index = 0
            
            self.logger.info("Episode saved via queue mechanism")

    def discard_current_episode(self):
        """Enhanced episode discarding with detailed logging"""
        with self.recording_lock:
            # Stop recording if still active
            if self.is_recording:
                self._stop_recording_internal()
                
            frame_count = len(self.current_episode_frames)
            duration = time.time() - self.current_episode_start_time if self.current_episode_start_time else 0
            
            # Clear buffer
            self.current_episode_frames = []
            self.current_frame_index = 0
            
            self.logger.info(f"🗑️ Discarded episode data ({frame_count} frames, {duration:.2f}s)")
            # 注意：discard不递增episode_counter

    def get_recording_status(self) -> Dict[str, Any]:
        """Enhanced recording status with detailed metrics"""
        with self.recording_lock:
            status = {
                'is_recording': self.is_recording,
                'episode_counter': self.episode_counter,
                'current_frame_count': len(self.current_episode_frames),
                'max_buffer_size': self.max_buffer_size,
                'buffer_usage_percent': len(self.current_episode_frames) / self.max_buffer_size * 100,
                'recording_fps': self.recording_fps,
                'save_queue_size': self.save_queue.qsize(),
                'save_stats': copy.copy(self.save_stats),
                'performance_stats': copy.copy(self.performance_stats)
            }
            
            if self.is_recording:
                status['recording_duration'] = time.time() - self.current_episode_start_time
                status['actual_fps'] = len(self.actual_fps_tracker) / 10 if self.actual_fps_tracker else 0
            
            # 添加下一个episode预览
            status['next_episode_index'] = self.episode_counter
                
            return status
            
    def finalize_dataset(self):
        """Finalize the dataset with all metadata"""
        try:
            dataset_path = self._create_dataset_path()
            
            # Wait for save queue to empty
            self.logger.info("Waiting for all episodes to be saved...")
            self.save_queue.join()
            
            # Finalize dataset using LeRobot formatter
            # self.lerobot_formatter.finalize_dataset(
            #     dataset_path, 
            #     self.episode_counter, 
            #     self.arm_names
            # )
            
            self.logger.info(f"Dataset finalized at {dataset_path}")
            
        except Exception as e:
            self.logger.error(f"Error finalizing dataset: {e}")
            
    def shutdown(self):
        """Enhanced shutdown with proper cleanup sequence"""
        self.logger.info("Shutting down DataRecorder...")
        
        # Stop recording if active
        with self.recording_lock:
            if self.is_recording:
                self.logger.warning("Stopping active recording during shutdown")
                self._stop_recording_internal()
                
        # Stop save thread and wait for completion
        # self.stop_save_thread.set()
        if self.save_thread and self.save_thread.is_alive():
            self.logger.info("Waiting for save thread to complete...")
            self.save_thread.join(timeout=1.0)
            
        # Wait for remaining saves with progress indication
        remaining = self.save_queue.qsize()
        if remaining > 0:
            self.logger.warning(f"Waiting for {remaining} episodes to save...")
            start_time = time.time()
            while self.save_queue.qsize() > 0 and time.time() - start_time < 60:
                time.sleep(1.0)
                current_remaining = self.save_queue.qsize()
                if current_remaining != remaining:
                    self.logger.info(f"Save progress: {remaining - current_remaining}/{remaining} completed")
                    remaining = current_remaining
        
        self.stop_memory_monitor.set()  
        if self.memory_monitor_thread and self.memory_monitor_thread.is_alive():  
            self.memory_monitor_thread.join(timeout=1.0)  
            
        # Finalize dataset
        self.finalize_dataset()
        
        # Shutdown components
        if hasattr(self, 'camera_manager'):
            self.camera_manager.stop_streaming()
            
        if hasattr(self, 'robot_controller'):
            self.robot_controller.disconnect_all()
            
        if hasattr(self, 'teleop_subscriber'):
            self.teleop_subscriber.shutdown()
            
        # Log final statistics
        self.logger.info(f"DataRecorder shutdown complete. Final stats: {self.save_stats}")


def main():
    """Enhanced test function for DataRecorder"""
    config_path = "./recording_config.yaml"
    
    recorder = None
    try:
        # Initialize ROS2
        import rclpy
        rclpy.init()
        
        # Create recorder
        recorder = DataRecorder(config_path)
        
        print("\n" + "="*70)
        print("Enhanced DataRecorder Test")
        print("="*70)
        print("\nFeatures:")
        print("  ✓ Enhanced frame structure with metadata")
        print("  ✓ Performance monitoring and adaptive FPS")
        print("  ✓ Priority-based background saving")
        print("  ✓ Buffer management with warnings")
        print("  ✓ Detailed statistics and logging")
        print("  ✓ LeRobot v3.0 format compatibility")
        print("\nCommands:")
        print("  Press 'q' to quit")
        print("  Press 's' for status")
        print("\nWaiting for teleoperation commands...")
        print("="*70 + "\n")
        
        # Enhanced main loop
        last_status_time = time.time()
        
        while True:
            # Show detailed status every 5 seconds
            current_time = time.time()
            if current_time - last_status_time > 5.0:
                status = recorder.get_recording_status()
                
                if status['is_recording']:
                    print(f"📹 Recording Episode {status['episode_counter']}: "
                          f"Frames={status['current_frame_count']}, "
                          f"Duration={status.get('recording_duration', 0):.1f}s, "
                          f"FPS={status.get('actual_fps', 0):.1f}, "
                          f"Buffer={status['buffer_usage_percent']:.1f}%")
                else:
                    print(f"⏸️ Idle - Episodes: {status['episode_counter']}, "
                          f"Save Queue: {status['save_queue_size']}, "
                          f"Saved/Failed: {status['save_stats']['saved']}/{status['save_stats']['failed']}")
                
                last_status_time = current_time
                
            # Check for user input
            try:
                import select
                import sys
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input().strip().lower()
                    if line == 'q':
                        break
                    elif line == 's':
                        status = recorder.get_recording_status()
                        print("\n" + "="*50)
                        print("Detailed Status:")
                        for key, value in status.items():
                            print(f"  {key}: {value}")
                        print("="*50 + "\n")
            except:
                pass
                
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        if recorder:
            recorder.shutdown()
        
        if 'rclpy' in locals():
            rclpy.shutdown()
            
        print("\nEnhanced test complete")


if __name__ == "__main__":
    main()