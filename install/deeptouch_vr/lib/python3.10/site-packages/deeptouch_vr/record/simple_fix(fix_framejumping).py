import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os
import numpy as np
import logging

# ==========================================
# 1. 配置日志 (Logging Configuration)
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("repair_dataset.log", mode='w'), # 日志写入文件
        logging.StreamHandler()                              # 日志输出到控制台
    ]
)

logger = logging.getLogger(__name__)

def process_parquet_file(parquet_file):
    """
    修复 Parquet 文件：
    1. 修复 frame_index 跳跃问题。
    2. 修正夹爪数据：当 mode 为 3 时，将 gripper_close 设为 1。
    """
    try:
        # 读取文件
        table = pq.read_table(parquet_file)
        df = table.to_pandas()

        if df.empty:
            logger.warning(f"SKIP: DataFrame is empty -> {parquet_file}")
            return

        # 标记数据是否发生了改变
        data_changed = False
        fix_details = [] # 用于收集该文件的修复摘要

        # ==========================================
        # 任务 A: 修复 frame_index
        # ==========================================
        if 'frame_index' in df.columns:
            correct_indices = np.arange(len(df), dtype=int)
            current_indices = df['frame_index'].to_numpy()
            
            # 检查是否完全匹配
            if not np.array_equal(current_indices, correct_indices):
                df['frame_index'] = correct_indices
                data_changed = True
                fix_details.append("Frame Index Reset")

        # ==========================================
        # 任务 B: 修正 Left Arm Gripper 数据
        # ==========================================
        col_mode = 'observation.state.left_arm.gripper_info.mode'
        col_close = 'observation.state.left_arm.gripper_info.gripper_close'

        if col_mode in df.columns and col_close in df.columns:
            # 1. 找到 mode == 3 的行
            mode_is_3 = df[col_mode] == 3
            
            # 2. 找到当前值不是 1 的行 (避免重复修改)
            value_not_1 = df[col_close] != 1
            
            # 3. 组合条件
            mask_to_fix = mode_is_3 & value_not_1
            
            count = mask_to_fix.sum()
            
            if count > 0:
                # 向量化赋值
                df.loc[mask_to_fix, col_close] = 1
                data_changed = True
                fix_details.append(f"Gripper Fixed ({count} rows)")
        else:
            logger.debug(f"MISSING COLUMNS: Gripper columns not found in {parquet_file}")

        # ==========================================
        # 保存逻辑
        # ==========================================
        if data_changed:
            # 写入文件
            table = pa.Table.from_pandas(df, preserve_index=False)
            pq.write_table(table, parquet_file)
            
            # 汇总日志信息
            actions_str = ", ".join(fix_details)
            logger.info(f"FIXED: {parquet_file} | Actions: [{actions_str}]")
        else:
            # 如果没变化，通常不输出INFO以免刷屏，或者使用DEBUG级别
            # logger.info(f"CLEAN: {parquet_file} (No changes needed)")
            pass

    except FileNotFoundError:
        logger.error(f"ERROR: File not found -> {parquet_file}")
    except Exception as e:
        logger.error(f"ERROR: Processing {parquet_file} -> {str(e)}")

def process_directory(root_dir):
    """
    递归遍历目录处理 episode.parquet
    """
    logger.info(f"Starting scan in: {root_dir}")
    
    processed_count = 0
    fixed_file_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'episode.parquet':
                full_path = os.path.join(dirpath, filename)
                
                # 我们稍微修改下逻辑，以便统计修复了多少个文件
                # 但为了保持函数纯洁性，这里主要负责遍历
                process_parquet_file(full_path)
                processed_count += 1
                
                if processed_count % 100 == 0:
                    logger.info(f"Progress: Scanned {processed_count} files...")

    logger.info(f"Job Complete. Total files scanned: {processed_count}")

if __name__ == "__main__":
    root_directory = '/home/deeptouch/datasets/eighth_150' 
    process_directory(root_directory)