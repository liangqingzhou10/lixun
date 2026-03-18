import os
import subprocess
import logging
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
import shutil
from scipy.spatial.transform import Rotation as R

# ANSI escape codes for colors
RED = '\033[91m'
RESET = '\033[0m'

# 自定义日志格式器
class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.WARNING:
            record.msg = RED + record.msg + RESET  # 将 WARNING 消息标红
        return super().format(record)

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # 设置日志级别

# 创建控制台处理器
ch = logging.StreamHandler()

# 设置自定义格式器
formatter = CustomFormatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 添加处理器到日志器
logger.addHandler(ch)

# ---------------------- frame_index.py 功能 ----------------------

def fix_frame_index(parquet_file):
    """修复parquet文件中的帧索引跳变"""
    try:
        table = pq.read_table(parquet_file)
        df = table.to_pandas()

        if df.empty:
            logger.warning(f"DataFrame is empty for file: {parquet_file}. Skipping.")
            return

        if 'frame_index' not in df.columns:
            logger.error(f"'frame_index' column not found in {parquet_file}.")
            return

        df['frame_index'] = df['frame_index'].astype(np.int64)  # 强制转换为 int64
        expected_frame_index = 0
        corrections = []

        for index, row in df.iterrows():
            if row['frame_index'] != expected_frame_index:
                corrections.append((index, expected_frame_index))

            expected_frame_index = (expected_frame_index + 1)

        for index, correct_frame_index in corrections:
            df.loc[index, 'frame_index'] = correct_frame_index

        table = pa.Table.from_pandas(df)
        pq.write_table(table, parquet_file)

        logger.info(f"Successfully fixed frame_index in {parquet_file}")

    except FileNotFoundError:
        logger.error(f"File not found: {parquet_file}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

def quaternion_to_rotation_matrix(quaternion):
    """
    将四元数转换为旋转矩阵。

    Args:
        quaternion: 长度为 4 的四元数 (qx, qy, qz, qw)。

    Returns:
        3x3 旋转矩阵。
    """
    r = R.from_quat(quaternion)
    return r.as_matrix()

def rotation_matrix_to_angle(rotation_matrix):
    """
    将旋转矩阵转换为轴角表示，并返回角度（弧度）。

    Args:
        rotation_matrix: 3x3 旋转矩阵。

    Returns:
        旋转角度（弧度）。
    """
    r = R.from_matrix(rotation_matrix)
    return r.as_rotvec()  # 返回旋转向量，其模长为旋转角度（弧度）

def calculate_joint_and_pose_stats(dataset_path, arm_name):
    """
    遍历 episode 目录中的 parquet 文件，计算 joint_positions 的差值统计量和 pose_quaternion 的旋转差值统计量。

    Args:
        dataset_path: 数据集根目录。
        arm_name: 机械臂名称 (例如 "left" 或 "right")。

    Returns:
        一个字典，包含每个 episode 的关节位置差值和旋转差值统计量。
    """

    episode_stats = {}

    # 获取所有 episode 目录
    episode_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

    if not episode_dirs:
        logger.error(f"No episode directories found in {dataset_path}")
        return None

    for episode_id in episode_dirs:
        episode_path = os.path.join(dataset_path, episode_id)
        parquet_file = os.path.join(episode_path, "data", "episode.parquet")

        if not os.path.exists(parquet_file):
            logger.error(f"Parquet file not found: {parquet_file}")
            continue

        try:
            df = pd.read_parquet(parquet_file)

            # 1. 处理 joint_positions
            joint_positions = np.stack(df['observation.state.' + arm_name + '_arm.joint_positions'].to_numpy())
            if joint_positions.shape[1] != 7:
                logger.error(f"Unexpected joint positions shape: {joint_positions.shape}. Expected (n, 7)")
                continue

            diffs = np.diff(joint_positions, axis=0)
            abs_diffs = np.abs(diffs)
            max_joint_diffs = np.max(abs_diffs, axis=0)

            # 2. 处理 pose_quaternion
            pose_quaternions = np.stack(df['observation.state.' + arm_name + '_arm.pose_quaternion'].to_numpy())
            if pose_quaternions.shape[1] != 7:
                logger.error(f"Unexpected pose quaternions shape: {pose_quaternions.shape}. Expected (n, 7)")
                continue

            # 将 pose_quaternion 分解为位置和四元数
            positions = pose_quaternions[:, :3]
            quaternions = pose_quaternions[:, 3:]

            # 将四元数转换为旋转矩阵
            rotation_matrices = np.array([quaternion_to_rotation_matrix(q) for q in quaternions])

            # 计算相邻旋转矩阵的点积 (R_i+1 * R_i.T)
            rotation_diffs = []
            for i in range(len(rotation_matrices) - 1):
                rotation_diff = rotation_matrices[i+1] @ rotation_matrices[i].T
                rotation_diffs.append(rotation_diff)

            # 将旋转矩阵转换为角度差
            angle_diffs = np.array([rotation_matrix_to_angle(r) for r in rotation_diffs])
            angle_magnitudes = np.linalg.norm(angle_diffs, axis=1)

            # 计算统计量
            max_angle_diff = np.max(angle_magnitudes)
            mean_angle_diff = np.mean(angle_magnitudes)

            # 将所有统计数据存储在 episode_stats 中
            episode_stats[episode_id] = {
                'joint_max': max_joint_diffs.tolist(),
                'pose_max_angle_diff': max_angle_diff,
                'pose_mean_angle_diff': mean_angle_diff,
            }
            logger.info(f"Episode {episode_id}: Joint Max = {max_joint_diffs.tolist()}, Pose Max Angle = {max_angle_diff}, Pose Mean Angle = {mean_angle_diff}")

        except Exception as e:
            logger.error(f"Error processing episode {episode_id}: {e}")

    return episode_stats

def calculate_average_combined_stats(episode_stats):
    """
    计算所有 episode 的关节和姿势统计量的平均值。

    Args:
        episode_stats: 包含每个episode的关节和姿势统计量的字典。

    Returns:
        一个字典，包含平均关节最大差值和平均姿势最大/平均角度差。
    """

    if not episode_stats:
        logger.warning("No episode stats provided.")
        return None

    # 提取所有 episode 的统计量
    all_joint_max_diffs = [stats['joint_max'] for stats in episode_stats.values()]
    all_pose_max_angle_diffs = [stats['pose_max_angle_diff'] for stats in episode_stats.values()]
    all_pose_mean_angle_diffs = [stats['pose_mean_angle_diff'] for stats in episode_stats.values()]

    num_joints = len(all_joint_max_diffs[0])

    # 初始化平均值列表
    average_joint_max_diffs = [0.0] * num_joints

    # 累加关节差值
    for joint_max_diffs in all_joint_max_diffs:
        for i in range(num_joints):
            average_joint_max_diffs[i] += joint_max_diffs[i]

    # 计算关节平均值
    for i in range(num_joints):
        average_joint_max_diffs[i] /= len(episode_stats)

    # 计算姿势平均值
    average_pose_max_angle_diff = np.mean(all_pose_max_angle_diffs)
    average_pose_mean_angle_diff = np.mean(all_pose_mean_angle_diffs)

    return {
        'average_joint_max': average_joint_max_diffs,
        'average_pose_max_angle_diff': average_pose_max_angle_diff,
        'average_pose_mean_angle_diff': average_pose_mean_angle_diff,
    }

def check_data_continuity(parquet_file, arm_name, joint_positions_threshold, pose_quaternion_threshold):  
    """检查数据的连续性，如果超过阈值，则warning并标红，显示是哪一episode，哪一帧"""  
    try:  
        episode_id = os.path.basename(os.path.dirname(os.path.dirname(parquet_file)))  

        table = pq.read_table(parquet_file)  
        df = table.to_pandas()  

        if df.empty:  
            logger.warning(f"DataFrame is empty for file: {parquet_file}. Skipping continuity check.")  
            return  

        # 构建完整的列名前缀  
        column_prefix = f'observation.state.{arm_name}_arm'  

        # 过滤出指定 arm_name 的数据  
        df_arm = df[df[f'{column_prefix}.arm_name'] == f'{arm_name}_arm'].copy()  

        if df_arm.empty:  
            logger.warning(f"No {arm_name} data in {parquet_file}. Skipping continuity check.")  
            return  

        # 确保数据按 frame_index 排序  
        df_arm = df_arm.sort_values(by='frame_index').reset_index(drop=True)  

        # 初始化计数器  
        joint_position_anomalies = 0  
        pose_quaternion_anomalies = 0  
        total_frames = len(df_arm)  # 总帧数  

        # 1. 处理 joint_positions  
        joint_positions = np.stack(df_arm[f'{column_prefix}.joint_positions'].to_numpy())  
        if joint_positions.shape[1] != 7:  
            logger.error(f"Unexpected joint positions shape: {joint_positions.shape}. Expected (n, 7)")  
            return  

        joint_diffs = np.diff(joint_positions, axis=0)  

        for i in range(joint_diffs.shape[0]): # 遍历每一帧  
            for j in range(joint_diffs.shape[1]): # 遍历每个关节  
                if abs(joint_diffs[i, j]) > joint_positions_threshold[j]:  
                    logger.warning(RED + f"Large joint_positions change at frame {i+1} (joint {j}) in episode {episode_id} in {parquet_file} ({arm_name}): {joint_diffs[i, j]}" + RESET)  
                    joint_position_anomalies += 1  # 增加关节位置异常计数  

        # 2. 处理 pose_quaternion  
        pose_quaternions = np.stack(df_arm[f'{column_prefix}.pose_quaternion'].to_numpy())  
        if pose_quaternions.shape[1] != 7:  
            logger.error(f"Unexpected pose quaternions shape: {pose_quaternions.shape}. Expected (n, 7)")  
            return  

        # 将 pose_quaternion 分解为位置和四元数  
        positions = pose_quaternions[:, :3]  
        quaternions = pose_quaternions[:, 3:]  

        # 将四元数转换为旋转矩阵  
        rotation_matrices = np.array([quaternion_to_rotation_matrix(q) for q in quaternions])  

        # 计算相邻旋转矩阵的点积 (R_i+1 * R_i.T)  
        rotation_diffs = []  
        for i in range(len(rotation_matrices) - 1):  
            rotation_diff = rotation_matrices[i+1] @ rotation_matrices[i].T  
            rotation_diffs.append(rotation_diff)  

        # 将旋转矩阵转换为角度差  
        angle_diffs = np.array([rotation_matrix_to_angle(r) for r in rotation_diffs])  
        angle_magnitudes = np.linalg.norm(angle_diffs, axis=1)  

        for i, diff in enumerate(angle_magnitudes):  
            if diff > pose_quaternion_threshold:  
                logger.warning(RED + f"Large pose_quaternion change at frame {i+1} in episode {episode_id} in {parquet_file} ({arm_name}): {diff}" + RESET)  
                pose_quaternion_anomalies += 1  # 增加姿态四元数异常计数  

        # 添加汇总信息  
        logger.info(f"Data continuity check for {parquet_file} ({arm_name}) completed. "  
                    f"Total frames: {total_frames}, Joint position anomalies: {joint_position_anomalies}, "  
                    f"Pose quaternion anomalies: {pose_quaternion_anomalies}")  

    except FileNotFoundError:  
        logger.error(f"File not found: {parquet_file}")  
    except Exception as e:  
        logger.error(f"An error occurred during data continuity check: {e}")  

def process_directory(root_dir, arm_name, average_joint_max, average_pose_max_angle_diff):
    """处理指定目录下所有 episode.parquet 文件，并进行连续性检查"""
    # 设置阈值为平均值的0.5倍
    joint_positions_threshold = [x * 0.5 for x in average_joint_max]
    pose_quaternion_threshold = average_pose_max_angle_diff * 0.5

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'episode.parquet':
                full_path = os.path.join(dirpath, filename)
                fix_frame_index(full_path)
                check_data_continuity(full_path, arm_name, joint_positions_threshold, pose_quaternion_threshold)


# ---------------------- 视频完整性检查 功能 ----------------------

def check_video_integrity(video_dir, ffprobe_path=None):
    """检查视频完整性"""

    if ffprobe_path is None:
        ffprobe_path = "ffprobe"  # 尝试使用环境变量中的 ffprobe

    try:
        # 确保 ffprobe 可用
        subprocess.run([ffprobe_path, "-version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        logger.error(f"ffprobe 未找到，请确认已安装 ffmpeg/ffprobe，并且 {'已配置环境变量' if ffprobe_path == 'ffprobe' else '指定的路径正确'}")
        return False

    checked = 0
    removed = 0
    has_bad = 0
    found_any = 0

    # 直接检查 video_dir 下的视频文件
    logger.info(f"检查目录: {video_dir}")  # 记录检查的目录

    video_files = [f for f in os.listdir(video_dir) if f.lower().endswith((".mp4", ".mov", ".mkv", ".avi", ".m4v", ".webm"))]

    if not video_files:
        logger.warning(f"未发现视频文件: {video_dir}")
        return True

    checked = len(video_files) #  设置检查的数量为视频文件的数量

    for filename in video_files:
        video_path = os.path.join(video_dir, filename)
        found_any = 1
        try:
            # 使用 ffprobe 检测视频流
            subprocess.run(
                [ffprobe_path, "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=codec_name", "-of", "csv=p=0", video_path],
                check=True,
                capture_output=True
            )
            logger.info(f"视频可读: {video_path}")  # 视频可读的日志
        except subprocess.CalledProcessError:
            logger.error(f"视频不可读: {video_path}")
            has_bad = 1
            break

    if has_bad:
        logger.info(f"删除目录: {video_dir}")
        # shutil.rmtree(video_dir)  # 谨慎操作，这里先注释掉
        removed += 1
    else:
        logger.info(f"通过: {video_dir}")

    logger.info(f"完成。检查目录: {checked}，删除目录: {removed}。")
    return True

# ---------------------- 数据集数据目录和内容完整性检查 功能 ----------------------
def check_dataset_structure(dataset_path):
    """
    检查数据集目录结构和关键文件的存在性，遍历所有可能的 "hand" 目录。
    """
    valid = True

    # 获取所有可能的 "hand" 目录
    hand_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d)) and "hand" in d]

    if not hand_dirs:
        logger.error(f"No 'hand' directories found in {dataset_path}")
        return False

    for hand_dir_name in hand_dirs:
        hand_path = os.path.join(dataset_path, hand_dir_name)

        # 获取所有 episode 目录
        episode_dirs = [d for d in os.listdir(hand_path) if os.path.isdir(os.path.join(hand_path, d))]

        if not episode_dirs:
            logger.warning(f"No episode directories found in {hand_path}")
            continue  # 允许没有 episode 目录的 "hand" 目录

        for episode_id in episode_dirs:
            episode_path = os.path.join(hand_path, episode_id)

            expected_files = {
                "data": ["episode.parquet"],
                "info": ["config_snapshot.json", "episode_metadata.json", "episode_tasks.json"],
                "videos": [
                    "left_camera_depth.mp4", "left_camera.mp4", "left_tactile_left_camera.mp4",
                    "left_tactile_right_camera.mp4", "right_camera_depth.mp4", "right_camera.mp4",
                    "right_tactile_left_camera.mp4", "right_tactile_right_camera.mp4"
                ],
            }

            for subdir, expected_file_list in expected_files.items():
                full_path = os.path.join(episode_path, subdir)
                if not os.path.exists(full_path):
                    logger.error(f"Missing directory: {full_path}")
                    valid = False
                    continue

                # 检查是否存在缺少的文件
                for expected_file in expected_file_list:
                    file_path = os.path.join(full_path, expected_file)
                    if not os.path.exists(file_path):
                        logger.error(f"Missing file: {file_path}")
                        valid = False

                # 检查是否存在多余的文件
                actual_files = os.listdir(full_path)
                for actual_file in actual_files:
                    if actual_file not in expected_file_list:
                        logger.warning(f"Unexpected file found: {os.path.join(full_path, actual_file)}")
                        # valid = False  # 你可以选择将 valid 设置为 False，如果存在多余文件就认为结构错误

    if valid:
        logger.info("Dataset structure check passed.")
    else:
        logger.error("Dataset structure check failed.")
    return valid
# ---------------------- 文件完整性检查 功能 ----------------------
def check_file_integrity(dataset_path):
    """
    Checks the integrity of files in the dataset.
    """
    parquet_files = []

    # 获取所有 episode 目录
    episode_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

    if not episode_dirs:
        logger.error(f"No episode directories found in {dataset_path}")
        return False

    for episode_id in episode_dirs:
        episode_path = os.path.join(dataset_path, episode_id)
        if not os.path.exists(episode_path):
            continue
        for root, _, files in os.walk(episode_path):
            for file in files:
                if file.endswith(".parquet"):
                    parquet_files.append(os.path.join(root, file))

    for file in parquet_files:
        try:
            table = pq.read_table(file)
            # You can add more checks here, like schema validation
            logger.info(f"File integrity check passed: {file}")
        except Exception as e:
            logger.error(f"File integrity check failed for {file}: {e}")
            return False

    logger.info("All file integrity checks passed.")
    return True

# ---------------------- 主函数 ----------------------
def validate_data(dataset_path, ffprobe_path=None):
    """
    Validates the data in the given dataset directory.
    """
    logger.info(f"Starting data validation for dataset: {dataset_path}")

    # 获取所有 hand 目录
    hand_dirs = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

    if not hand_dirs:
        logger.error(f"No hand directories found in {dataset_path}")
        return False

    # 计算平均统计量
    all_episode_stats = {}
    for hand_dir_name in hand_dirs:
        if hand_dir_name in ['left_hand', 'right_hand']:
            hand_dir_path = os.path.join(dataset_path, hand_dir_name)
            arm_name = hand_dir_name[:-5]  # left_hand -> left, right_hand -> right
            episode_stats = calculate_joint_and_pose_stats(hand_dir_path, arm_name)
            if episode_stats:
                all_episode_stats[arm_name] = episode_stats
            else:
                logger.warning(f"Could not calculate stats for {hand_dir_name}")

    average_stats = {}
    for arm_name, episode_stats in all_episode_stats.items():
        average_stats[arm_name] = calculate_average_combined_stats(episode_stats)
        if average_stats[arm_name]:
            logger.info(f"Average stats for {arm_name}: {average_stats[arm_name]}")
        else:
            logger.warning(f"Could not calculate average stats for {arm_name}")
            return False

    # 1. 修复帧索引和检查数据连续性
    for hand_dir_name in hand_dirs:
        if hand_dir_name in ['left_hand', 'right_hand']:
            hand_dir_path = os.path.join(dataset_path, hand_dir_name)
            episode_dirs = [d for d in os.listdir(hand_dir_path) if os.path.isdir(os.path.join(hand_dir_path, d))]

            logger.info(f"Processing {hand_dir_name} directory...")
            arm_name = hand_dir_name[:-5]  # left_hand -> left, right_hand -> right
            if arm_name in average_stats and average_stats[arm_name]:
                average_joint_max = average_stats[arm_name]['average_joint_max']
                average_pose_max_angle_diff = average_stats[arm_name]['average_pose_max_angle_diff']
                for episode_id in episode_dirs:
                    data_dir = os.path.join(hand_dir_path, episode_id, "data")
                    if os.path.exists(data_dir):
                        logger.info(f"Fixing frame indices and checking data continuity for {episode_id} ({arm_name})...")
                        process_directory(data_dir, arm_name, average_joint_max, average_pose_max_angle_diff)
                    else:
                        logger.warning(f"Data directory not found: {data_dir}")
            else:
                logger.warning(f"No average stats found for {arm_name}, skipping continuity check.")


    # 2. 检查视频完整性
    logger.info("Checking video integrity...")
    for hand_dir_name in hand_dirs:
        if hand_dir_name in ['left_hand', 'right_hand']:
            hand_dir_path = os.path.join(dataset_path, hand_dir_name)
            episode_dirs = [d for d in os.listdir(hand_dir_path) if os.path.isdir(os.path.join(hand_dir_path, d))]

            for episode_id in episode_dirs:
                video_dir = os.path.join(hand_dir_path, episode_id, "videos")
                if os.path.exists(video_dir):
                    check_video_integrity(video_dir, ffprobe_path)  # process all directory which contain videos
                else:
                    logger.warning(f"Video directory not found: {video_dir}")

    # 3. 检查数据集结构
    logger.info("Checking dataset structure...")
    if not check_dataset_structure(dataset_path):
        logger.error("Dataset structure check failed. Aborting.")
        return False

    # 4. 检查文件完整性
    logger.info("Checking file integrity...")
    if not check_file_integrity(dataset_path):
        logger.error("File integrity check failed. Aborting.")
        return False

    logger.info("Data validation completed.")
    return True

if __name__ == "__main__":
    dataset_root = "/home/deeptouch/datasets/ceshi"
    ffprobe_path = "/usr/bin/ffprobe" # 使用环境变量中的 ffprobe

    validate_data(dataset_root, ffprobe_path)
