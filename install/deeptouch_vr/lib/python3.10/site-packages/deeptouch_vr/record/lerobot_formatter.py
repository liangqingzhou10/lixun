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

import os  
import json  
import shutil  
import tempfile  
from pathlib import Path  
from typing import Dict, List, Any, Optional, Union, Tuple  
import logging  
from concurrent.futures import ThreadPoolExecutor, as_completed  
import threading  
import yaml
import numpy as np  
import pandas as pd  
import pyarrow as pa  
import pyarrow.parquet as pq  
import cv2  
import subprocess
import gc
import concurrent.futures


class LeRobotFormatter:  
    """  
    Enhanced LeRobot v3.0 dataset formatter for multi-arm robot data  
    Modified to store each episode in separate folder named by episode_index
    """  
    
    def __init__(self, config: dict):  
        self.config = config  
        self.logger = logging.getLogger(self.__class__.__name__)  
        
        # Enhanced configuration from config  
        self.fps = config.get('lerobot', {}).get('fps', config.get('fps', 30))  
        self.robot_type = config.get('lerobot', {}).get('robot_type', config.get('robot_type', 'RM75-6F-V'))  
        self.use_video = config.get('lerobot', {}).get('use_video', True)  
        self.video_codec = config.get('lerobot', {}).get('video_codec', 'mp4v')  
        
        # 🔥 新增：检查当前目录获取起始episode索引
        self.base_dir = Path(config.get('output', {}).get('base_dir', './datasets'))
        self.dataset_name = config.get('output', {}).get('dataset_name', 'robot_manipulation_v3')
        self.dataset_root = self.base_dir / self.dataset_name
        self.starting_episode_idx = self._get_starting_episode_index()
        self.current_episode_idx = self.starting_episode_idx
        
        # Enhanced file size limits based on LeRobot v3.0 defaults  
        self.data_file_size_mb = config.get('data_file_size_mb', 100)  
        self.video_file_size_mb = config.get('video_file_size_mb', 500)  
        
        # Chunk management (每个episode独立存储，不再使用chunk概念)
        self.chunk_size = config.get('lerobot', {}).get('chunk_size', 1000)  
        
        # Enhanced buffers for accumulating data with thread safety  
        self.episode_buffer = []  
        self.video_buffers = {}  # per camera  
        self.buffer_lock = threading.RLock()  
        
        # Enhanced chunk and file tracking (简化，每episode独立)
        self.current_chunk_idx = 0  
        self.current_file_idx = 0  
        self.current_data_size_mb = 0  
        self.current_video_sizes_mb = {}  # per camera  
        
        # Enhanced episode and frame tracking  
        self.total_episodes = 0  
        self.total_frames = 0  
        
        # Enhanced task management with validation  
        self.tasks = {}  
        self.task_to_index = {}  
        self.next_task_index = 0  
        
        # Enhanced statistics accumulation  
        self.all_stats = []  
        self.field_stats = {}  # Continuous field statistics  
        
        # Enhanced episode metadata tracking for v3.0  
        self.episodes_metadata = []  
        
        # Video processing thread pool  
        camera_count = len(self.config.get('cameras', {})) * 2  
        self.video_executor = ThreadPoolExecutor(max_workers=max(8, camera_count))
        self.video_futures = []
        self.active_video_writers = {}

        self.video_indices = {}  
        self._ep_meta_index = {}  

        # Camera metadata cache  
        self.camera_metadata_cache = {}

        # 添加meta文件更新相关
        self.meta_lock = threading.Lock()  
        self._episode_meta_cache = []  
        self._task_meta_cache = {}  
        self._stats_accumulator = {}  
        
        self.logger.info(f"Enhanced LeRobotFormatter initialized for robot type: {self.robot_type}")  
        self.logger.info(f"Starting from episode index: {self.starting_episode_idx}")

    def _get_starting_episode_index(self) -> int:
        """检查当前目录获取起始episode索引"""
        if not self.dataset_root.exists():
            self.logger.info(f"Dataset directory does not exist, starting from episode 0")
            return 0
        
        max_episode_idx = -1
        episode_dirs = []
        
        try:
            # 扫描所有以数字命名的文件夹
            for item in self.dataset_root.iterdir():
                if item.is_dir() and item.name.isdigit():
                    episode_idx = int(item.name)
                    episode_dirs.append(episode_idx)
                    max_episode_idx = max(max_episode_idx, episode_idx)
            
            if episode_dirs:
                self.logger.info(f"Found existing episodes: {sorted(episode_dirs)}")
                next_idx = max_episode_idx + 1
                self.logger.info(f"Starting from episode {next_idx}")
                return next_idx
            else:
                self.logger.info(f"No existing episodes found, starting from episode 0")
                return 0
                
        except Exception as e:
            self.logger.warning(f"Error scanning existing episodes: {e}, starting from episode 0")
            return 0
        
    def save_episode(self, episode_data: 'EpisodeData'):  
        """  
        🔥 全新版本：处理数据块(chunk)，支持分块追加写入。  
        
        Args:  
            episode_data: 由 DataRecorder 传来的 EpisodeData 对象，包含一个数据块。  
        """  
        frames = episode_data.frames  
        episode_idx = episode_data.episode_index  
        metadata = episode_data.metadata  
        data_dir = self.dataset_root  

        if not frames:  
            self.logger.warning(f"Chunk for episode {episode_idx} has no frames. Skipping.")  
            return  
    
        chunk_frame_count = len(frames)  
        self.logger.info(f"Processing chunk for episode {episode_idx} with {chunk_frame_count} frames. Trigger: {metadata.get('save_trigger')}")  

        try:  
            # --- 1. 准备目录 ---  
            episode_dir = data_dir / str(episode_idx)  
            episode_dir.mkdir(parents=True, exist_ok=True)  
            episode_data_dir = episode_dir / 'data'  
            episode_data_dir.mkdir(exist_ok=True)  
            episode_video_dir = episode_dir / 'videos'  
            episode_video_dir.mkdir(exist_ok=True)  
            
            # --- 2. 处理 Parquet 数据 (追加写入) ---  
            episode_df = self._frames_to_dataframe_enhanced(frames, episode_idx)  
            if not episode_df.empty:  
                parquet_path = episode_data_dir / "episode.parquet"  
                self._save_or_append_parquet(episode_df, parquet_path)  
            del episode_df # 立即释放内存  
            
            # --- 3. 处理视频数据 (流式写入) ---  
            if self.use_video:  
                self._stream_chunk_to_video(frames, episode_idx, episode_video_dir)  
        
            # 立即释放内存  
            del frames  
            gc.collect()  

            # --- 4. 如果是最后一个块，执行收尾工作 ---  
            # 'final_stop' 是我们在 DataRecorder.stop_recording 中设置的触发器  
            if metadata.get('save_trigger') == 'final_stop':  
                self.logger.info(f"Final chunk for episode {episode_idx} received. Finalizing episode...")  
                self.finalize_episode_resources(episode_idx, episode_dir)  

            self.logger.info(f"✓ Successfully processed chunk for episode {episode_idx}.")  

        except Exception as e:  
            self.logger.error(f"Error processing chunk for episode {episode_idx}: {e}", exc_info=True)  
            # 考虑在这里也清理一下资源  
            self.finalize_episode_resources(episode_idx, episode_dir)  

    def _save_or_append_parquet(self, df: pd.DataFrame, path: Path):  
        """将DataFrame保存到Parquet文件，如果文件存在则追加。"""  
        # 使用锁确保对同一个文件的读写操作是线程安全的  
        with self.meta_lock:  
            try:  
                if path.exists():  
                    # --- 追加模式 ---  
                    self.logger.debug(f"Appending {len(df)} rows to existing Parquet file: {path}")  
                    # 使用 pandas 实现简单可靠的追加  
                    # 注意：这会先读入整个旧文件，对于超大episode可能成为瓶颈  
                    existing_df = pd.read_parquet(path)  
                    combined_df = pd.concat([existing_df, df], ignore_index=True)  
                    combined_df.to_parquet(path, engine='pyarrow', compression='snappy', use_dictionary=True)  
                else:  
                    # --- 创建新文件模式 ---  
                    self.logger.debug(f"Creating new Parquet file: {path} with {len(df)} rows.")  
                    schema = self._create_data_schema_v30_enhanced(df)  
                    table = pa.Table.from_pandas(df, schema=schema)  
                    pq.write_table(table, path, compression='snappy', use_dictionary=True)  

            except Exception as e:  
                self.logger.error(f"Failed during Parquet save/append for {path}: {e}", exc_info=True)  
                raise  

    def _stream_chunk_to_video(self, frames: List, episode_idx: int, video_dir: Path): 
        """将数据块中的图像帧流式写入视频文件 (修复深度图崩溃版本)。""" 
        if episode_idx not in self.active_video_writers: 
            self.active_video_writers[episode_idx] = {} 
            self.logger.info(f"Initializing video writers for episode {episode_idx}") 

        writers = self.active_video_writers[episode_idx] 
        frame_counts = {camera_name: 0 for frame in frames for camera_name in frame.images.keys()} 

        import numpy as np
        import cv2

        for frame_idx, frame in enumerate(frames): 
            for camera_name, image in frame.images.items(): 
                # 预先判断是否为深度流
                is_depth_stream = 'depth' in camera_name.lower()

                if camera_name not in writers: 
                    # --- 初始化 VideoWriter ---
                    try: 
                        height, width, *channels = image.shape 
                        # 如果是深度图，通常是单通道，但在保存视频时为了兼容性，我们通常存为3通道BGR
                        # 所以这里 is_color 统一设为 True (除非你确定后台支持纯灰度编码)
                        is_color = True 
                    
                        video_path = video_dir / f"{camera_name}.mp4" 
                        fourcc = cv2.VideoWriter_fourcc(*self.video_codec) 
                    
                        writer = cv2.VideoWriter(str(video_path), fourcc, float(self.fps), (width, height), isColor=is_color) 
                        if not writer.isOpened(): 
                            self.logger.error(f"Failed to open video writer for {video_path}") 
                            writers[camera_name] = None 
                            continue 
                    
                        writers[camera_name] = writer 
                        frame_counts[camera_name] = 0 
                        self.logger.info(f"Opened video stream for {camera_name} at {video_path} with resolution {width}x{height}") 
                    except Exception as e: 
                        self.logger.error(f"Error creating VideoWriter for {camera_name}: {e}", exc_info=True) 
                        writers[camera_name] = None 
                        continue 

                writer = writers.get(camera_name) 
                if writer: 
                    try: 
                        # --- 健壮性检查: Resize ---
                        target_w = int(writer.get(cv2.CAP_PROP_FRAME_WIDTH)) 
                        target_h = int(writer.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
                        
                        if target_w > 0 and target_h > 0: 
                            h, w = image.shape[:2] 
                            if h != target_h or w != target_w: 
                                image = cv2.resize(image, (target_w, target_h), interpolation=cv2.INTER_NEAREST if is_depth_stream else cv2.INTER_AREA) 
                        
                        # ==========================================================
                        # 🔥 核心修复区域：处理深度图数据类型
                        # ==========================================================
                        if is_depth_stream: 
                            # 1. 归一化处理：因为 VideoWriter 只吃 uint8 (0-255)
                            # 原始深度通常是 float(米) 或 uint16(毫米)
                            # 为了可视化和保存，我们将其归一化到 0-255 范围
                            
                            if image.dtype in [np.float32, np.float64]:
                                # 如果是 float，假设范围是 0-10米 (根据实际情况调整 max_val)
                                # 这里简单的做 min-max 归一化以便显示
                                image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
                            elif image.dtype == np.uint16:
                                # 如果是 16位，压缩到 8位
                                image = (image / 256).astype(np.uint8)
                            
                            # 强制转为 uint8，这是 VideoWriter 不崩溃的关键
                            image = image.astype(np.uint8)

                            # 2. 通道处理：将单通道灰度转为 3通道 BGR
                            # 这一步是为了防止某些编解码器对单通道支持不好
                            if len(image.shape) == 2 or (len(image.shape) == 3 and image.shape[2] == 1):
                                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

                        else: 
                            # 彩色图处理
                            if image.dtype != np.uint8: 
                                image = (image * 255).astype(np.uint8) 
                            # 确保是 BGR 格式 (LeRobot通常内部是 RGB，OpenCV需要 BGR)
                            # 这里假设输入的 image 已经是 BGR 或者 RGB，如果不确定颜色是否正确，可能需要 cvtColor
                            # 但首先确保它是 uint8

                        # --- 最终写入 --- 
                        writer.write(image) 
                        frame_counts[camera_name] += 1 

                    except Exception as e: 
                        self.logger.warning( 
                            f"Error writing frame for {camera_name} " 
                            f"(dtype: {image.dtype if 'image' in locals() else 'N/A'}): {e}",  
                            exc_info=True 
                        )

    def finalize_episode_resources(self, episode_idx: int, episode_dir: Path):  
        """关闭与指定 episode 相关的所有资源，如视频写入器，并生成元数据。"""  
        self.logger.info(f"Finalizing resources for episode {episode_idx}...")  

        # --- 1. 关闭视频写入器 ---  
        if episode_idx in self.active_video_writers:  
            writers = self.active_video_writers.pop(episode_idx) # 从活动字典中移除  
            for camera_name, writer in writers.items():  
                if writer:  
                    writer.release()  
                    self.logger.info(f"Closed video stream for {camera_name} in episode {episode_idx}.")  
            self.logger.info(f"All video writers for episode {episode_idx} have been released.")  
        
        # --- 2. （可选但推荐）生成最终的元数据文件 ---  
        try:  
            parquet_path = episode_dir / 'data' / 'episode.parquet'  
            if parquet_path.exists():  
                full_df = pd.read_parquet(parquet_path)  
                # 使用您现有的 _create_episode_metadata 等方法，但需要改造为从DataFrame读取信息  
                # 这里我们用一个简化的版本  
                num_frames = len(full_df)  
                start_time = full_df['timestamp'].min()  
                end_time = full_df['timestamp'].max()  

                # 复用您已有的元数据创建逻辑，但用df中的数据  
                metadata = {  
                    'episode_index': episode_idx,  
                    'length': num_frames,  
                    'start_timestamp': start_time,  
                    'end_timestamp': end_time,  
                    'duration': end_time - start_time,  
                    # ... 其他可以从df中推断的元数据  
                }  

                info_dir = episode_dir / 'info'  
                info_dir.mkdir(exist_ok=True)  
                # 复用您已有的保存逻辑  
                self._save_episode_info(metadata, info_dir, episode_idx)  

        except Exception as e:  
            self.logger.error(f"Error during metadata generation for episode {episode_idx}: {e}")  
            
        # --- 3. 清理内存 ---  
        gc.collect()  

    def _cleanup_memory_caches(self):
        """定期清理内存缓存"""
        try:
            # 确保所有视频任务都已完成并清理 futures
            self.logger.debug(f"Cleaning {len(self.video_futures)} video futures...")
            for future in self.video_futures:
                if not future.done():
                    future.cancel() # 尝试取消未完成的任务
            self.video_futures = [] # 清空列表

            # 清理相机元数据缓存
            self.episodes_metadata.clear()
            self._ep_meta_index.clear()
            self.all_stats.clear()
            self.video_buffers.clear()
            self.camera_metadata_cache.clear()
            
            # 清理视频缓冲区
            # 🔥 3. 清理 video_buffers - 逐个删除引用
            if self.video_buffers:
                self.logger.debug(f"Cleaning {len(self.video_buffers)} video buffers...")
                for camera_name in list(self.video_buffers.keys()):
                    # 尝试清空列表中的 numpy 数组
                    if isinstance(self.video_buffers[camera_name], list):
                        for img_array in self.video_buffers[camera_name]:
                            del img_array # 解除引用
                        self.video_buffers[camera_name].clear()
                    del self.video_buffers[camera_name] # 删除字典条目
                self.video_buffers.clear()

            # 强制垃圾回收
            gc.collect()
            
            self.logger.info("✓ Memory caches cleaned")
            
        except Exception as e:
            self.logger.warning(f"Error cleaning memory caches: {e}")


    def _frames_to_dataframe_enhanced(self, frames: List, episode_idx: int) -> pd.DataFrame:  
        """🔥 修改版本：Enhanced conversion of frames to pandas DataFrame with proper data types
        将所有state信息记录到observation中，保持原始数据类型"""  
        
        rows = []  
        
        for frame_idx, frame in enumerate(frames):  
            try:  

                # if not frame.robot_states:
                #     self.logger.error(f"🔴 ERROR: Frame {frame_idx} has EMPTY robot_states!")
                # else:
                #     # 打印一下看看里面有啥 keys，确认是不是 arm_name 对不上
                #     self.logger.info(f"🟢 Frame {frame_idx} robot_states keys: {list(frame.robot_states.keys())}")

                row = {  
                    'episode_index': int(episode_idx),  
                    'frame_index': int(frame_idx),  
                    'timestamp': float(frame.timestamp),  
                }  
                
                # 🔥 Enhanced robot observations - 将所有state信息记录到observation中
                for arm_name, robot_state in frame.robot_states.items():  
                    if robot_state:  
                        # 🔥 遍历robot_state中的所有字段，记录到observation中
                        for state_key, state_value in robot_state.items():
                            try:
                                observation_key = f'observation.state.{arm_name}.{state_key}'
                                
                                if state_value is None:
                                    continue
                                    
                                # 处理数组类型的状态信息
                                if isinstance(state_value, np.ndarray):
                                    if state_value.size > 0:
                                        row[observation_key] = state_value.astype(np.float32).tolist()
                                        
                                elif isinstance(state_value, (list, tuple)):
                                    if len(state_value) > 0:
                                        try:
                                            # 尝试转换为数值数组
                                            state_array = np.array(state_value, dtype=np.float32)
                                            row[observation_key] = state_array.tolist()
                                        except (ValueError, TypeError):
                                            # 如果无法转换为数值，存储为JSON字符串
                                            row[observation_key] = json.dumps(list(state_value))
                                            
                                elif isinstance(state_value, dict):
                                    # 🔥 特殊处理gripper_info等嵌套字典
                                    if state_key == 'gripper_info':
                                        # 🔥 修改：使用嵌套命名方式 gripper_info.{key}
                                        for gripper_key, gripper_value in state_value.items():
                                            gripper_obs_key = f'observation.state.{arm_name}.gripper_info.{gripper_key}'
                                            
                                            # 🔥 保持原始数据类型
                                            if isinstance(gripper_value, (int, np.integer)):
                                                row[gripper_obs_key] = int(gripper_value)
                                            elif isinstance(gripper_value, (float, np.floating)):
                                                row[gripper_obs_key] = float(gripper_value)
                                            elif isinstance(gripper_value, bool):
                                                row[gripper_obs_key] = bool(gripper_value)
                                            elif isinstance(gripper_value, (list, tuple, np.ndarray)):
                                                try:
                                                    gripper_array = np.array(gripper_value, dtype=np.float32)
                                                    if gripper_array.size > 0:
                                                        row[gripper_obs_key] = gripper_array.tolist()
                                                except (ValueError, TypeError):
                                                    row[gripper_obs_key] = json.dumps(
                                                        gripper_value.tolist() if isinstance(gripper_value, np.ndarray) else list(gripper_value)
                                                    )
                                            else:
                                                row[gripper_obs_key] = str(gripper_value)
                                    else:
                                        # 其他嵌套字典，递归处理
                                        for sub_key, sub_value in state_value.items():
                                            # 🔥 修改：使用点号分隔的嵌套命名
                                            sub_obs_key = f'observation.state.{arm_name}.{state_key}.{sub_key}'
                                            
                                            # 🔥 保持原始数据类型
                                            if isinstance(sub_value, (int, np.integer)):
                                                row[sub_obs_key] = int(sub_value)
                                            elif isinstance(sub_value, (float, np.floating)):
                                                row[sub_obs_key] = float(sub_value)
                                            elif isinstance(sub_value, bool):
                                                row[sub_obs_key] = bool(sub_value)
                                            elif isinstance(sub_value, (list, tuple, np.ndarray)):
                                                try:
                                                    sub_array = np.array(sub_value, dtype=np.float32)
                                                    if sub_array.size > 0:
                                                        row[sub_obs_key] = sub_array.tolist()
                                                except (ValueError, TypeError):
                                                    row[sub_obs_key] = json.dumps(
                                                        sub_value.tolist() if isinstance(sub_value, np.ndarray) else list(sub_value)
                                                    )
                                            else:
                                                row[sub_obs_key] = str(sub_value)
                                                
                                # 🔥 保持原始数据类型 - 不强制转换为float
                                elif isinstance(state_value, (int, np.integer)):
                                    row[observation_key] = int(state_value)
                                    
                                elif isinstance(state_value, (float, np.floating)):
                                    row[observation_key] = float(state_value)
                                    
                                elif isinstance(state_value, bool):
                                    row[observation_key] = bool(state_value)
                                    
                                elif isinstance(state_value, str):
                                    # 对于字符串类型，如IP地址等直接存储
                                    row[observation_key] = str(state_value)
                                    
                                else:
                                    # 其他类型转换为字符串
                                    row[observation_key] = str(state_value)
                                    
                            except Exception as e:
                                self.logger.warning(f"Error processing state {state_key}={state_value} for arm {arm_name} in frame {frame_idx}: {e}")
                                continue
                
                # 这里省略actions处理部分，因为原代码中被注释掉了
                
                # 🔥 Enhanced image handling following v3.0 format  
                if self.use_video:  
                    for camera_name in frame.images.keys():  
                        row[f'observation.images.{camera_name}'] = f"videos/{camera_name}.mp4"  
                else:  
                    # For direct image storage (not recommended for large datasets)  
                    for camera_name, image in frame.images.items():  
                        # Store image metadata instead of raw data  
                        row[f'observation.images.{camera_name}'] = json.dumps({  
                            'shape': list(image.shape),  
                            'dtype': str(image.dtype)  
                        })  
                
                # 🔥 Enhanced task information  
                if frame.task_info and 'task' in frame.task_info:  
                    task_str = frame.task_info['task']  
                    task_idx = self._get_or_create_task_index(task_str)  
                    row['task_index'] = int(task_idx)
                    
                    # 🔥 记录所有task_info字段，保持原始数据类型
                    for task_key, task_value in frame.task_info.items():
                        if task_key != 'task':  # task字段已经通过task_index处理
                            task_obs_key = f'task_info.{task_key}'
                            
                            if isinstance(task_value, (int, np.integer)):
                                row[task_obs_key] = int(task_value)
                            elif isinstance(task_value, (float, np.floating)):
                                row[task_obs_key] = float(task_value)
                            elif isinstance(task_value, bool):
                                row[task_obs_key] = bool(task_value)
                            elif isinstance(task_value, (list, tuple, np.ndarray)):
                                try:
                                    task_array = np.array(task_value, dtype=np.float32)
                                    if task_array.size > 0:
                                        row[task_obs_key] = task_array.tolist()
                                except (ValueError, TypeError):
                                    row[task_obs_key] = json.dumps(
                                        task_value.tolist() if isinstance(task_value, np.ndarray) else list(task_value)
                                    )
                            else:
                                row[task_obs_key] = str(task_value)
                
                # 🔥 修复：Additional metadata - 正确处理数据类型
                if frame.metadata:  
                    for key, value in frame.metadata.items():  
                        if key not in row:  # Don't override existing keys  
                            metadata_key = f'metadata.{key}'
                            # 🔥 根据值的类型决定如何存储，保持原始类型
                            if isinstance(value, (int, np.integer)):
                                row[metadata_key] = int(value)
                            elif isinstance(value, (float, np.floating)):
                                row[metadata_key] = float(value)
                            elif isinstance(value, bool):
                                row[metadata_key] = bool(value)
                            elif isinstance(value, (list, tuple, np.ndarray)):
                                row[metadata_key] = json.dumps(value.tolist() if isinstance(value, np.ndarray) else list(value))
                            elif isinstance(value, dict):
                                row[metadata_key] = json.dumps(value)
                            else:
                                row[metadata_key] = str(value)
                
                rows.append(row)  
                
            except Exception as e:  
                self.logger.warning(f"Error processing frame {frame_idx} in episode {episode_idx}: {e}")  
                continue  
        
        if not rows:  
            self.logger.error(f"No valid rows created for episode {episode_idx}")  
            return pd.DataFrame()  
        
        df = pd.DataFrame(rows)  
        self.logger.debug(f"Created DataFrame for episode {episode_idx}: {len(df)} rows, {len(df.columns)} columns")  
        return df

    def _save_episode_data_direct(self, episode_df: pd.DataFrame, data_dir: Path, episode_idx: int):
        """直接保存episode的数据到指定目录"""
        if episode_df.empty:
            self.logger.warning(f"Empty DataFrame for episode {episode_idx}")
            return
        
        # 保存为parquet格式
        data_path = data_dir / f"episode.parquet"
        
        try:
            # 🔥 修复：创建正确的schema，不强制所有metadata字段为string
            schema = self._create_data_schema_v30_enhanced(episode_df)
            
            # 保存数据
            pq.write_table(  
                pa.Table.from_pandas(episode_df, schema=schema),  
                data_path,  
                compression='snappy',
                use_dictionary=True
            )  
            
            file_size_mb = data_path.stat().st_size / 1024 / 1024
            self.logger.info(f"✓ Saved episode data: {data_path} ({file_size_mb:.1f}MB, {len(episode_df)} frames)")
            
        except Exception as e:
            self.logger.error(f"Error saving episode data for {episode_idx}: {e}")
            raise


    def _create_data_schema_v30_enhanced(self, df: pd.DataFrame) -> pa.Schema:  
        """🔥 修复：Enhanced schema creation with correct type inference for v3.0
        支持更多observation字段类型"""  
        
        schema_fields = []  
        
        for col in df.columns:  
            try:  
                if col in ['episode_index', 'frame_index', 'task_index']:  
                    schema_fields.append(pa.field(col, pa.int64()))  
                elif col == 'timestamp':  
                    schema_fields.append(pa.field(col, pa.float64()))  
                    
                elif col.startswith('observation.state.'):
                    # 🔥 修复：统一处理所有observation.state字段，根据实际数据类型推断
                    if not df[col].empty:
                        sample_value = df[col].iloc[0]
                        
                        # 检查是否为数组类型字段
                        if isinstance(sample_value, list):
                            schema_fields.append(pa.field(col, pa.list_(pa.float32())))
                        # 检查是否为数值类型
                        elif isinstance(sample_value, (int, np.integer)):
                            schema_fields.append(pa.field(col, pa.int64()))
                        elif isinstance(sample_value, (float, np.floating)):
                            schema_fields.append(pa.field(col, pa.float64()))
                        # 检查是否为布尔类型
                        elif isinstance(sample_value, bool):
                            schema_fields.append(pa.field(col, pa.bool_()))
                        # 其他类型作为字符串处理
                        else:
                            schema_fields.append(pa.field(col, pa.string()))
                    else:
                        # 空列的情况，根据列名推断
                        if any(array_field in col for array_field in ['.joint_positions', '.joint_currents', '.joint_temperatures', 
                                                                    '.pose_quaternion', '.pose_euler', '.force_current', 
                                                                    '.zero_force', '.cartesian_pose', '.cartesian_velocity',
                                                                    '.joint_velocities', '.joint_efforts', '.joint_speeds']):
                            schema_fields.append(pa.field(col, pa.list_(pa.float32())))
                        elif any(string_field in col for string_field in ['.arm_ip', '.arm_name']):
                            schema_fields.append(pa.field(col, pa.string()))
                        elif col.endswith('.timestamp'):
                            schema_fields.append(pa.field(col, pa.float64()))  # 🔥 修复：timestamp是float64
                        elif any(int_field in col for int_field in ['.arm_status', '.error_code', 
                                                                '.gripper_info.status_code', '.gripper_info.error', 
                                                                '.gripper_info.mode', '.gripper_info.actpos', 
                                                                '.gripper_info.enable_state', '.gripper_info.status',
                                                                '.gripper_info.gripper_close']):
                            # 🔥 修改：使用gripper_info.xxx的嵌套命名
                            schema_fields.append(pa.field(col, pa.int64()))
                        elif any(float_field in col for float_field in ['.gripper_info.current_force', '.gripper_info.temperature']):
                            # 🔥 修改：使用gripper_info.xxx的嵌套命名
                            schema_fields.append(pa.field(col, pa.float64()))
                        else:
                            schema_fields.append(pa.field(col, pa.float64()))  # 默认为float64
                            
                elif col.startswith('action.'):
                    # Action字段处理
                    if not df[col].empty:
                        sample_value = df[col].iloc[0]
                        if isinstance(sample_value, list):
                            schema_fields.append(pa.field(col, pa.list_(pa.float32())))
                        elif isinstance(sample_value, (int, np.integer)):
                            schema_fields.append(pa.field(col, pa.int64()))
                        elif isinstance(sample_value, (float, np.floating)):
                            schema_fields.append(pa.field(col, pa.float64()))
                        else:
                            schema_fields.append(pa.field(col, pa.string()))
                    else:
                        schema_fields.append(pa.field(col, pa.list_(pa.float32())))  # 默认为数组
                        
                elif 'observation.images.' in col:
                    schema_fields.append(pa.field(col, pa.string()))
                    
                elif col.startswith('task_info.'):
                    # 🔥 处理task_info字段
                    if not df[col].empty:
                        sample_value = df[col].iloc[0]
                        if isinstance(sample_value, list):
                            schema_fields.append(pa.field(col, pa.list_(pa.float32())))
                        elif isinstance(sample_value, (int, np.integer)):
                            schema_fields.append(pa.field(col, pa.int64()))
                        elif isinstance(sample_value, (float, np.floating)):
                            schema_fields.append(pa.field(col, pa.float64()))
                        elif isinstance(sample_value, bool):
                            schema_fields.append(pa.field(col, pa.bool_()))
                        else:
                            schema_fields.append(pa.field(col, pa.string()))
                    else:
                        schema_fields.append(pa.field(col, pa.string()))
                        
                elif col.startswith('metadata.'):
                    # 🔥 修复：根据实际数据类型推断metadata字段的schema
                    if not df[col].empty:
                        sample_value = df[col].iloc[0]
                        if isinstance(sample_value, (int, np.integer)):
                            schema_fields.append(pa.field(col, pa.int64()))
                        elif isinstance(sample_value, (float, np.floating)):
                            schema_fields.append(pa.field(col, pa.float64()))
                        elif isinstance(sample_value, bool):
                            schema_fields.append(pa.field(col, pa.bool_()))
                        else:
                            schema_fields.append(pa.field(col, pa.string()))
                    else:
                        schema_fields.append(pa.field(col, pa.string()))
                else:
                    schema_fields.append(pa.field(col, pa.string()))
                    
            except Exception as e:
                self.logger.warning(f"Error creating schema for column {col}: {e}")
                schema_fields.append(pa.field(col, pa.string()))
                
        return pa.schema(schema_fields)


    def _process_episode_videos_direct(self, frames: List, episode_idx: int, video_dir: Path, episode_metadata: Dict):  
        """  
        🔥 修改版本 (流式写入): 直接处理并保存episode的视频到指定目录，并准确统计帧数。  
        """  
        if not frames:  
            self.logger.warning(f"No frames for episode {episode_idx} to process for video.")  
            return  

        video_writers: Dict[str, cv2.VideoWriter] = {}  
        camera_dims: Dict[str, Tuple[int, int, int]] = {}  
        # 🔥 本地帧计数器，每个writer一个  
        local_frame_counts: Dict[str, int] = {}  
        video_paths: Dict[str, Path] = {}  

        try:  
            # --- 1. 初始化 VideoWriters ---  
            for frame in frames:  
                for camera_name, image in frame.images.items():  
                    if image is not None and camera_name not in camera_dims:  
                        height, width, channels = self._get_consistent_image_dims([img for f in frames if (img := f.images.get(camera_name)) is not None], camera_name)  
                        camera_dims[camera_name] = (height, width, channels)  

            if not camera_dims:  
                self.logger.warning(f"No valid camera images found in episode {episode_idx}.")  
                return  

            for camera_name, (height, width, channels) in camera_dims.items():  
                video_path = video_dir / f"{camera_name}.mp4"  
                video_paths[camera_name] = video_path  
                fourcc = cv2.VideoWriter_fourcc(*self.video_codec)  
                is_color = not camera_name.endswith('_depth')  
                writer = cv2.VideoWriter(str(video_path), fourcc, float(self.fps), (int(width), int(height)), isColor=is_color)  

                if not writer.isOpened():  
                    self.logger.error(f"Failed to open video writer for {video_path}")  
                    continue  
                video_writers[camera_name] = writer  
                # 🔥 初始化本地计数器  
                local_frame_counts[camera_name] = 0  
                self.logger.info(f"Opened video stream for {camera_name} at {video_path}")  

            # --- 2. 流式写入帧 ---  
            for frame_idx, frame in enumerate(frames):  
                for camera_name, image in frame.images.items():  
                    writer = video_writers.get(camera_name)  
                    if writer and image is not None:  
                        try:  
                            target_h, target_w, _ = camera_dims[camera_name]  
                            processed_img = self._process_image_for_video(image, target_w, target_h, camera_name)  
                            writer.write(processed_img)  
                            # 🔥 递增本地计数器  
                            local_frame_counts[camera_name] += 1  
                        except Exception as e:  
                            self.logger.warning(f"Error writing frame {frame_idx} for {camera_name}: {e}")  

            self.logger.info(f"Finished streaming frames to video writers for episode {episode_idx}.")  

        finally:  
            # --- 3. 关闭所有 VideoWriters ---  
            for camera_name, writer in video_writers.items():  
                if writer:  # 确保writer存在  
                    writer.release()  
                    self.logger.info(f"Closed video stream for {camera_name}.")  

        # --- 4. 提交后台验证和元数据更新 ---  
        futures = []  
        for camera_name, video_path in video_paths.items():  
            if video_path.exists() and video_path.stat().st_size > 0:  
                # 🔥 传递本地计数器给验证任务  
                future = self.video_executor.submit(  
                    self._verify_and_get_video_info_task,  
                    video_path,  
                    camera_name,  
                    episode_idx,  
                    local_frame_counts.get(camera_name, 0)  # 使用本地计数器  
                )  
                futures.append(future)  
                self.video_futures.append(future)  # 跟踪 future  

        # 等待验证完成并更新元数据  
        for future in concurrent.futures.as_completed(futures):  
            try:  
                video_info = future.result()  
                if video_info:  
                    cam_name = video_info['camera']  
                    # 更新 episode_metadata (确保线程安全或在单线程中完成)  
                    episode_metadata[f'videos/{cam_name}/path'] = str(video_info['path'].relative_to(video_dir.parent.parent))  
                    episode_metadata[f'videos/{cam_name}/duration'] = video_info['duration']  
                    episode_metadata[f'videos/{cam_name}/frame_count'] = video_info['frame_count']  
                    episode_metadata[f'videos/{cam_name}/codec'] = video_info['codec']  
            except Exception as e:  
                self.logger.error(f"Video verification task failed: {e}")  

    def _verify_and_get_video_info_task(self, video_path: Path, camera_name: str, episode_idx: int, frame_count: int) -> Optional[Dict]:  
        """A task for verifying a video file and returning its metadata."""  
        try:  
            is_depth = camera_name.endswith('_depth')  
            if not self._verify_video_file(video_path, camera_name, is_depth):  
                self.logger.error(f"Video verification failed for {camera_name} in episode {episode_idx}")  
                if video_path.exists():  
                    video_path.unlink()  # 删除无效视频  
                return None  

            video_size_mb = video_path.stat().st_size / 1024 / 1024  
            duration = frame_count / float(self.fps) if self.fps > 0 else 0  

            fmt = "grayscale" if is_depth else "rgb"  
            self.logger.info(f"✓ Verified {fmt} video for {camera_name}: "  
                           f"{frame_count} frames, {video_size_mb:.1f}MB")  

            return {  
                'camera': camera_name,  
                'episode_idx': episode_idx,  
                'duration': duration,  
                'frame_count': frame_count,  # 直接使用传入的 frame_count  
                'codec': self.video_codec,  
                'path': video_path,  
                'size_mb': video_size_mb  
            }  
        except Exception as e:  
            self.logger.error(f"Error in video verification task for {camera_name}: {e}")  
            return None  

    def _save_episode_info(self, episode_metadata: Dict, info_dir: Path, episode_idx: int):  
        """保存episode的信息到info目录"""  
        try:  
            # 1. 保存episode metadata  
            episode_info_path = info_dir / "episode_metadata.json"  
            with open(episode_info_path, 'w', encoding='utf-8') as f:  
                json.dump(episode_metadata, f, indent=2, default=str)  

            # 2. 读取 recording_config.yaml 文件并保存 task_saying 描述  
            try:
                recording_config_path = Path('/workspace/deeptouch/src/deeptouch_vr/deeptouch_vr/record/config/recording_config.yaml')  
                if not recording_config_path.exists():  
                    self.logger.warning(f"配置文件未找到: {recording_config_path}")  
                else:  
    # 正常处理配置文件  
                     with open(recording_config_path, 'r', encoding='utf-8') as f:  
                         recording_config = yaml.safe_load(f)  
                task_saying_description = recording_config.get('tasks')  

                if task_saying_description:  
                    task_json_path = info_dir / "episode_tasks.json"  
                    try:  
                        with open(task_json_path, 'w', encoding='utf-8') as f:  
                            json.dump({'tasks': [ 
                                task_saying_description
                                ]}, f, indent=2, ensure_ascii=False)  
                        self.logger.info(f"✓ Saved episode_tasks.json to {task_json_path}")  
                    except Exception as e:  
                        self.logger.error(f"Error saving episode_tasks.json: {e}")  
                else:  
                    self.logger.info("No tasks specified in recording_config.yaml")  

            except Exception as e:  
                self.logger.error(f"Error loading recording_config.yaml: {e}", exc_info=True)  

            # 3. 保存episode任务信息  
            episode_tasks = episode_metadata.get('tasks', [])  
            if episode_tasks:  
                tasks_path = info_dir / "episode_tasks.json"  
                with open(tasks_path, 'w', encoding='utf-8') as f:  
                    json.dump({'tasks': episode_tasks}, f, indent=2)  

            # 4. 保存episode配置快照  
            config_path = info_dir / "config_snapshot.json"  

            safe_cameras_config = self._sanitize_config_for_json(self.config.get('cameras', {}))  
            safe_robot_config = self._sanitize_config_for_json(self.config.get('robot', {}))  

            config_snapshot = {  
                'fps': self.fps,  
                'robot_type': self.robot_type,  
                'cameras': safe_cameras_config,  
                'robot': safe_robot_config,  
                'episode_index': episode_idx,  
                'timestamp': pd.Timestamp.now().isoformat()  
            }  
            with open(config_path, 'w', encoding='utf-8') as f:  
                # 使用 default=str 作为最后的保障  
                json.dump(config_snapshot, f, indent=2, default=str)  

            self.logger.info(f"✓ Saved episode info to {info_dir}")  

        except Exception as e:  
            self.logger.error(f"Error saving episode info for {episode_idx}: {e}")  

    def _sanitize_config_for_json(self, config_part: Any) -> Any:  
        """递归清理配置，移除不可序列化的对象。"""  
        if isinstance(config_part, dict):  
            # 对于字典，递归处理它的值  
            return {key: self._sanitize_config_for_json(value) for key, value in config_part.items()}  
        elif isinstance(config_part, list):  
            # 对于列表，递归处理它的元素  
            return [self._sanitize_config_for_json(item) for item in config_part]  
        elif isinstance(config_part, (int, float, str, bool, type(None))):  
            # 基本的可序列化类型，直接返回  
            return config_part  
        else:  
            # 对于所有其他类型（对象、实例等），将其转换为字符串表示  
            return str(config_part)  


    def _create_episode_metadata(self, frames: List, episode_idx: int) -> Dict:  
        """Create comprehensive episode metadata following v3.0 format"""  
        if not frames:  
            return {}  
        
        metadata = {  
            'episode_index': episode_idx,  
            'length': len(frames),  
            'start_timestamp': frames[0].timestamp,  
            'end_timestamp': frames[-1].timestamp,  
            'duration': frames[-1].timestamp - frames[0].timestamp,  
            'avg_fps': len(frames) / (frames[-1].timestamp - frames[0].timestamp) if len(frames) > 1 else 0,
            'created_at': pd.Timestamp.now().isoformat(),
            'storage_format': 'single_episode_folder'
        }  
        
        # Add camera information  
        camera_names = set()  
        for frame in frames:  
            camera_names.update(frame.images.keys())  
        metadata['camera_names'] = sorted(list(camera_names))  
        
        # Add arm information  
        arm_names = set()  
        for frame in frames:  
            arm_names.update(frame.robot_states.keys())  
            arm_names.update(frame.actions.keys())  
        metadata['arm_names'] = sorted(list(arm_names))  
        
        # Add task information  
        tasks = set()  
        for frame in frames:  
            if frame.task_info and 'task' in frame.task_info:  
                tasks.add(frame.task_info['task'])  
        metadata['tasks'] = sorted(list(tasks))  
        
        return metadata

    # 继续添加其他必要的函数...
    def _validate_and_clean_frames(self, frames: List, episode_idx: int) -> List:
        """根据配置验证和清理帧数据，支持RGB和depth数据"""
        validated_frames = []
        camera_config = self.config.get('cameras', {})
        
        # 根据配置确定预期的相机流
        expected_cameras = set()
        for camera_name, config in camera_config.items():
            if config.get('rgb_stream', False):
                expected_cameras.add(camera_name)
            if config.get('depth_stream', False):
                expected_cameras.add(f"{camera_name}_depth")     
                
        all_cameras_found = set()
        
        for i, frame in enumerate(frames):
            try:
                # Basic frame validation
                if not hasattr(frame, 'timestamp') or frame.timestamp <= 0:
                    self.logger.warning(f"Episode {episode_idx}, frame {i}: Invalid timestamp")
                    continue
                
                frame_cameras = set(frame.images.keys())
                all_cameras_found.update(frame_cameras)
                
                # 根据配置处理图像
                valid_images = {}
                for camera_name, image in frame.images.items():
                    if image is not None and isinstance(image, np.ndarray) and image.size > 0:
                        
                        if len(image.shape) < 2:
                            self.logger.warning(f"Episode {episode_idx}, frame {i}: Invalid shape for {camera_name}: {image.shape}")
                            continue
                        
                        base_camera_name = camera_name.replace('_depth', '')
                        is_depth_stream = camera_name.endswith('_depth')
                        
                        camera_cfg = camera_config.get(base_camera_name, {})
                        
                        if is_depth_stream:
                            if not camera_cfg.get('depth_stream', False):
                                continue
                            
                            # 处理深度图像格式
                            if len(image.shape) == 2:
                                valid_images[camera_name] = image
                            elif len(image.shape) == 3 and image.shape[2] == 1:
                                valid_images[camera_name] = image[:, :, 0]
                            elif len(image.shape) == 3 and image.shape[2] == 3:
                                depth_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                                valid_images[camera_name] = depth_gray
                            else:
                                self.logger.warning(f"Episode {episode_idx}, frame {i}: Invalid depth format for {camera_name}, shape: {image.shape}")
                                
                        else:
                            if not camera_cfg.get('rgb_stream', False):
                                continue
                            
                            # 处理RGB图像格式
                            if len(image.shape) == 3 and image.shape[2] == 3:
                                valid_images[camera_name] = image
                            elif len(image.shape) == 3 and image.shape[2] == 1:
                                rgb_image = cv2.cvtColor(image[:, :, 0], cv2.COLOR_GRAY2BGR)
                                valid_images[camera_name] = rgb_image
                            elif len(image.shape) == 2:
                                rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
                                valid_images[camera_name] = rgb_image
                            else:
                                self.logger.warning(f"Episode {episode_idx}, frame {i}: Invalid RGB format for {camera_name}, shape: {image.shape}")
                
                frame.images = valid_images
                
                # Validate robot states
                valid_states = {}
                for arm_name, state in frame.robot_states.items():
                    if state and isinstance(state, dict):
                        valid_states[arm_name] = state
                frame.robot_states = valid_states
                
                # Validate actions
                valid_actions = {}
                for arm_name, action in frame.actions.items():
                    if action is not None:
                        if isinstance(action, np.ndarray):
                            valid_actions[arm_name] = action
                        elif isinstance(action, (list, tuple)):
                            valid_actions[arm_name] = np.array(action, dtype=np.float32)
                frame.actions = valid_actions
                
                validated_frames.append(frame)
                
            except Exception as e:
                self.logger.warning(f"Error validating frame {i} in episode {episode_idx}: {e}")
                continue
        
        # 检查缺失的相机
        camera_stats = {}
        for frame in validated_frames:
            for camera_name in frame.images.keys():
                if camera_name not in camera_stats:
                    camera_stats[camera_name] = 0
                camera_stats[camera_name] += 1
                
        missing_cameras = expected_cameras - set(camera_stats.keys())
        if missing_cameras:
            self.logger.error(f"Episode {episode_idx}: Missing expected cameras: {sorted(missing_cameras)}")
                
        return validated_frames

    def _get_consistent_image_dims(self, images: List[np.ndarray], camera_name: str) -> Tuple[int, int, int]:
        """获取一致的图像尺寸，正确处理depth和RGB图像"""
        if camera_name in self.camera_metadata_cache:
            cache = self.camera_metadata_cache[camera_name]
            return cache['height'], cache['width'], cache['channels']
        
        # 统计图像尺寸
        dims_count = {}
        is_depth = camera_name.endswith('_depth')
        
        for img in images:
            if img is not None and len(img.shape) >= 2:
                height, width = img.shape[:2]
                
                if is_depth:
                    channels = 1  # 记录原始通道数
                else:
                    channels = img.shape[2] if len(img.shape) == 3 else 3
                
                dim = (height, width, channels)
                dims_count[dim] = dims_count.get(dim, 0) + 1
        
        if dims_count:
            # 使用最常见的尺寸
            height, width, channels = max(dims_count.keys(), key=dims_count.get)
            
            # 缓存结果
            self.camera_metadata_cache[camera_name] = {
                'height': height,
                'width': width,
                'channels': channels,
                'is_depth': is_depth
            }
            
            return height, width, channels
        
        # 默认值
        if is_depth:
            return 480, 640, 1  # depth默认单通道
        else:
            return 480, 640, 3  # RGB默认三通道

    def _process_image_for_video(self, img: np.ndarray, target_width: int, target_height: int, 
                           camera_name: str) -> np.ndarray:
        """处理图像用于视频编码，修正RGB/BGR和depth归一化问题"""
        try:
            # 调整尺寸
            if img.shape[:2] != (target_height, target_width):
                img = cv2.resize(img, (target_width, target_height))
            
            # 判断是否为depth图像
            is_depth = camera_name.endswith('_depth')
            
            if is_depth:
                # 处理depth图像 - 输出单通道灰度图
                if len(img.shape) == 3 and img.shape[2] == 1:
                    depth_gray = img[:, :, 0]
                elif len(img.shape) == 2:
                    depth_gray = img
                else:
                    if len(img.shape) == 3:
                        depth_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    else:
                        self.logger.warning(f"Unexpected depth image shape: {img.shape}")
                        depth_gray = np.zeros((target_height, target_width), dtype=np.uint8)
                
                # 修正depth值归一化处理
                if depth_gray.dtype != np.uint8:
                    if depth_gray.dtype in [np.float32, np.float64]:
                        valid_mask = (depth_gray > 0) & (depth_gray < np.inf) & (~np.isnan(depth_gray))
                        
                        if np.any(valid_mask):
                            valid_depths = depth_gray[valid_mask]
                            
                            if depth_gray.max() <= 1.0:
                                depth_normalized = depth_gray * 255
                            elif depth_gray.max() <= 10.0:
                                max_depth = min(np.percentile(valid_depths, 99), 5.0)
                                depth_normalized = np.clip(depth_gray / max_depth * 255, 0, 255)
                            else:
                                depth_99th = np.percentile(valid_depths, 99)
                                depth_normalized = np.clip(depth_gray / depth_99th * 255, 0, 255)
                            
                            depth_normalized[~valid_mask] = 0
                        else:
                            depth_normalized = np.zeros_like(depth_gray)
                        
                        depth_gray = depth_normalized.astype(np.uint8)
                    else:
                        if depth_gray.max() > 255:
                            depth_normalized = np.clip(depth_gray / depth_gray.max() * 255, 0, 255)
                            depth_gray = depth_normalized.astype(np.uint8)
                        else:
                            depth_gray = depth_gray.astype(np.uint8)
                
                return depth_gray
                
            else:
                # 处理RGB图像 - 输出3通道BGR
                if len(img.shape) == 3 and img.shape[2] == 3:
                    if img.dtype != np.uint8:
                        if img.dtype in [np.float32, np.float64]:
                            if img.max() <= 1.0:
                                img = (img * 255).astype(np.uint8)
                            else:
                                img = np.clip(img, 0, 255).astype(np.uint8)
                        else:
                            img = img.astype(np.uint8)
                    
                    img_bgr = img  # 假设输入已经是BGR格式
                    return img_bgr
                else:
                    self.logger.warning(f"Unexpected RGB image format: {img.shape}")
                    return np.zeros((target_height, target_width, 3), dtype=np.uint8)
            
        except Exception as e:
            self.logger.warning(f"Error processing image for {camera_name}: {e}")
            # 返回适当的后备图像
            if camera_name.endswith('_depth'):
                return np.zeros((target_height, target_width), dtype=np.uint8)
            else:
                return np.zeros((target_height, target_width, 3), dtype=np.uint8)

    def _verify_video_file(self, video_path: Path, camera_name: str, is_depth: bool) -> bool:
        """验证生成的视频文件是否可读"""
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                self.logger.warning(f"Cannot open video file: {video_path}")
                return False
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if frame_count == 0:
                self.logger.warning(f"Video has no frames: {video_path}")
                cap.release()
                return False
            
            frames_to_check = min(3, frame_count)
            valid_frames = 0
            
            for i in range(frames_to_check):
                ret, frame = cap.read()
                if ret and frame is not None:
                    valid_frames += 1
                else:
                    break
            
            cap.release()
            success_rate = valid_frames / frames_to_check if frames_to_check > 0 else 0
            return success_rate >= 0.8
            
        except Exception as e:
            self.logger.warning(f"Error verifying video {video_path}: {e}")
            return False

    def _get_or_create_task_index(self, task_str: str) -> int:
        """Get or create task index for given task string"""
        if task_str not in self.task_to_index:
            self.task_to_index[task_str] = self.next_task_index
            self.tasks[self.next_task_index] = task_str
            self.next_task_index += 1
        return self.task_to_index[task_str]

    def _update_episode_stats_enhanced(self, frames: List, episode_idx: int):
        """Update episode statistics for v3.0 format"""
        # Extract numeric data for statistics
        numeric_data = {}
        
        for frame in frames:
            # Robot state statistics
            for arm_name, state in frame.robot_states.items():
                if state:
                    if 'joint_positions' in state:
                        key = f"observation.state.{arm_name}.joint_positions"
                        if key not in numeric_data:
                            numeric_data[key] = []
                        numeric_data[key].extend(state['joint_positions'])
            
            # Action statistics
            for arm_name, action in frame.actions.items():
                if action is not None:
                    key = f"action.{arm_name}"
                    if key not in numeric_data:
                        numeric_data[key] = []
                    numeric_data[key].extend(action.tolist())
        
        # Compute statistics
        episode_stats = {'episode_index': episode_idx}
        for key, values in numeric_data.items():
            if values:
                values_array = np.array(values)
                episode_stats[key] = {
                    'mean': float(np.mean(values_array)),
                    'std': float(np.std(values_array)),
                    'min': float(np.min(values_array)),
                    'max': float(np.max(values_array))
                }
        
        self.all_stats.append(episode_stats)

    def _update_tasks_enhanced(self, frames: List, episode_idx: int):
        """Update task information for v3.0 format"""
        for frame in frames:
            if frame.task_info and 'task' in frame.task_info:
                task_str = frame.task_info['task']
                self._get_or_create_task_index(task_str)

    def finalize_dataset(self, dataset_path: Path = None, total_episodes: int = None, arm_names: List[str] = None):
        """
        完成数据集处理 - 创建全局汇总信息
        
        Args:
            dataset_path: 数据集路径，如果为None则使用默认路径
            total_episodes: 总episode数，如果为None则使用内部计数
            arm_names: 机械臂名称列表，如果为None则自动推断
        """
        try:
            if dataset_path is None:
                dataset_path = self.dataset_root
                
            if total_episodes is None:
                total_episodes = self.total_episodes
                
            if arm_names is None:
                # 自动推断arm names
                arm_names = set()
                for ep in self.episodes_metadata:
                    arm_names.update(ep.get('arm_names', []))
                arm_names = sorted(list(arm_names))
            
            self.logger.info("Finalizing dataset...")
            
            # 1. 等待所有视频处理完成
            if hasattr(self, 'video_executor'):
                self.video_executor.shutdown(wait=True)
            
            # 2. 创建全局汇总信息
            self._create_global_summary(dataset_path, total_episodes, arm_names)
            
            # 3. 创建dataset index
            self._create_dataset_index(dataset_path)
            
            # 4. 验证数据集完整性
            self._validate_dataset_structure(dataset_path)
            
            self.logger.info(f"✓ Dataset finalized successfully at {dataset_path}")
            self.logger.info(f"✓ Total episodes: {total_episodes}, Total frames: {self.total_frames}")
            
        except Exception as e:
            self.logger.error(f"Error finalizing dataset: {e}", exc_info=True)
            raise

    def _create_global_summary(self, dataset_path: Path, total_episodes: int, arm_names: List[str]):
        """创建全局数据集汇总信息"""
        try:
            summary_dir = dataset_path / 'summary'
            summary_dir.mkdir(exist_ok=True)
            
            # 1. 全局信息
            global_info = {
                'dataset_name': self.dataset_name,
                'codebase_version': 'v3.0_single_episode',
                'robot_type': self.robot_type,
                'total_episodes': int(total_episodes),
                'total_frames': int(self.total_frames),
                'total_tasks': len(self.tasks),
                'fps': int(self.fps),
                'storage_format': 'single_episode_folder',
                'created_at': pd.Timestamp.now().isoformat(),
                'arms': arm_names,
                'cameras': list(self.config.get('cameras', {}).keys()),
                'episode_range': {
                    'start': self.starting_episode_idx,
                    'end': self.current_episode_idx - 1,
                    'count': self.current_episode_idx - self.starting_episode_idx
                }
            }
            
            # 保存全局信息
            with open(summary_dir / 'dataset_info.json', 'w') as f:
                json.dump(global_info, f, indent=2)
            
            # 2. Episodes汇总
            episodes_summary = []
            for ep_meta in self.episodes_metadata:
                summary_item = {
                    'episode_index': ep_meta['episode_index'],
                    'length': ep_meta['length'],
                    'duration': ep_meta.get('duration', 0.0),
                    'camera_names': ep_meta.get('camera_names', []),
                    'arm_names': ep_meta.get('arm_names', []),
                    'tasks': ep_meta.get('tasks', []),
                    'folder_path': str(ep_meta['episode_index'])
                }
                episodes_summary.append(summary_item)
            
            # 保存episodes汇总
            episodes_df = pd.DataFrame(episodes_summary)
            episodes_df.to_parquet(summary_dir / 'episodes_summary.parquet', index=False)
            episodes_df.to_csv(summary_dir / 'episodes_summary.csv', index=False)
            
            # 3. Tasks汇总  
            if self.tasks:
                tasks_summary = [{'task_index': idx, 'task': task} 
                               for idx, task in self.tasks.items()]
                tasks_df = pd.DataFrame(tasks_summary)
                tasks_df.to_parquet(summary_dir / 'tasks_summary.parquet', index=False)
                tasks_df.to_csv(summary_dir / 'tasks_summary.csv', index=False)
            
            # 4. 统计汇总
            if self.all_stats:
                self._create_stats_summary(summary_dir)
            
            self.logger.info(f"✓ Created global summary in {summary_dir}")
            
        except Exception as e:
            self.logger.error(f"Error creating global summary: {e}")
            raise

    def _create_dataset_index(self, dataset_path: Path):
        """创建数据集索引文件，方便快速访问"""
        try:
            # 创建episode索引
            episode_index = {}
            for ep_meta in self.episodes_metadata:
                ep_idx = ep_meta['episode_index']
                episode_index[ep_idx] = {
                    'folder': str(ep_idx),
                    'data_file': f"{ep_idx}/data/episode_{ep_idx:06d}.parquet",
                    'info_file': f"{ep_idx}/info/episode_metadata.json",
                    'length': ep_meta['length'],
                    'duration': ep_meta.get('duration', 0.0),
                    'cameras': ep_meta.get('camera_names', []),
                    'videos': {cam: f"{ep_idx}/videos/{cam}_episode_{ep_idx:06d}.mp4" 
                             for cam in ep_meta.get('camera_names', [])}
                }
            
            # 保存索引
            index_path = dataset_path / 'dataset_index.json'
            with open(index_path, 'w') as f:
                json.dump(episode_index, f, indent=2)
            
            self.logger.info(f"✓ Created dataset index: {index_path}")
            
        except Exception as e:
            self.logger.error(f"Error creating dataset index: {e}")

    def _validate_dataset_structure(self, dataset_path: Path):
        """验证数据集结构完整性"""
        missing_items = []
        
        # 检查每个episode的文件
        for ep_meta in self.episodes_metadata:
            ep_idx = ep_meta['episode_index']
            episode_dir = dataset_path / str(ep_idx)
            
            # 检查目录
            if not episode_dir.exists():
                missing_items.append(f"Episode {ep_idx}: missing episode directory")
                continue
            
            # 检查数据文件
            data_file = episode_dir / 'data' / f'episode_{ep_idx:06d}.parquet'
            if not data_file.exists():
                missing_items.append(f"Episode {ep_idx}: missing data file")
            
            # 检查info文件
            info_file = episode_dir / 'info' / 'episode_metadata.json'
            if not info_file.exists():
                missing_items.append(f"Episode {ep_idx}: missing metadata file")
            
            # 检查视频文件（如果启用）
            if self.use_video:
                for camera_name in ep_meta.get('camera_names', []):
                    video_file = episode_dir / 'videos' / f'{camera_name}_episode_{ep_idx:06d}.mp4'
                    if not video_file.exists():
                        missing_items.append(f"Episode {ep_idx}: missing video for {camera_name}")
        
        # 检查汇总文件
        summary_files = [
            'summary/dataset_info.json',
            'summary/episodes_summary.parquet', 
            'dataset_index.json'
        ]
        
        for summary_file in summary_files:
            file_path = dataset_path / summary_file
            if not file_path.exists():
                missing_items.append(f"Missing summary file: {summary_file}")
        
        if missing_items:
            self.logger.error(f"Dataset validation failed. Missing items:")
            for item in missing_items:
                self.logger.error(f"  - {item}")
        else:
            self.logger.info("✓ Dataset validation passed - all files present")

    def _create_stats_summary(self, summary_dir: Path):
        """创建统计信息汇总"""
        try:
            # 聚合所有episodes的统计
            field_stats = {}
            for episode_stat in self.all_stats:
                for field, stats in episode_stat.items():
                    if field != 'episode_index' and isinstance(stats, dict):
                        if field not in field_stats:
                            field_stats[field] = {'values': []}
                        if 'mean' in stats:
                            field_stats[field]['values'].append(stats['mean'])
            
            # 计算全局统计
            global_stats = []
            for field, data in field_stats.items():
                if data['values']:
                    values = np.array(data['values'])
                    global_stats.append({
                        'field': field,
                        'mean': float(np.mean(values)),
                        'std': float(np.std(values)),
                        'min': float(np.min(values)),
                        'max': float(np.max(values)),
                        'count': len(values)
                    })
            
            if global_stats:
                # 保存为parquet和JSON
                stats_df = pd.DataFrame(global_stats)
                stats_df.to_parquet(summary_dir / 'global_stats.parquet', index=False)
                
                # 同时保存为可读的JSON
                with open(summary_dir / 'global_stats.json', 'w') as f:
                    json.dump(global_stats, f, indent=2)
                
                self.logger.info(f"✓ Created global statistics summary ({len(global_stats)} fields)")
                
        except Exception as e:
            self.logger.error(f"Error creating stats summary: {e}")