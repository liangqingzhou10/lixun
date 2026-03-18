import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import os

def fix_frame_index(parquet_file):
    """
    Fixes the frame_index jump in a parquet file.

    Args:
        parquet_file (str): Path to the parquet file.
    """

    try:
        # 读取 Parquet 文件到 DataFrame
        table = pq.read_table(parquet_file)
        df = table.to_pandas()

        # 检查 DataFrame 是否为空
        if df.empty:
            print(f"Warning: DataFrame is empty for file: {parquet_file}. Skipping.")
            return

        # 确保 'frame_index' 列存在
        if 'frame_index' not in df.columns:
            print(f"Error: 'frame_index' column not found in {parquet_file}.")
            return

        # 将 'frame_index' 列转换为整数类型，以确保正确比较
        df['frame_index'] = df['frame_index'].astype(int)

        # 初始化 expected_frame_index
        expected_frame_index = 0

        # 记录需要修改的行的索引和正确的 frame_index
        corrections = []

        # 遍历 DataFrame 的每一行
        for index, row in df.iterrows():
            if row['frame_index'] != expected_frame_index:
                corrections.append((index, expected_frame_index))  # 记录需要修改的索引和正确值

            expected_frame_index = (expected_frame_index + 1) # 更新 expected_frame_index

        # 应用修正
        for index, correct_frame_index in corrections:
            df.loc[index, 'frame_index'] = correct_frame_index

        # 将 DataFrame 转换回 PyArrow 表
        table = pa.Table.from_pandas(df)

        # 覆盖保存修正后的数据
        pq.write_table(table, parquet_file)

        print(f"Successfully fixed frame_index in {parquet_file}")

    except FileNotFoundError:
        print(f"Error: File not found: {parquet_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_directory(root_dir):
    """
    Processes all 'episode.parquet' files in the given directory and its subdirectories.

    Args:
        root_dir (str): The root directory to start processing from.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'episode.parquet':
                full_path = os.path.join(dirpath, filename)
                fix_frame_index(full_path)

# 使用示例
if __name__ == "__main__":
    root_directory = '/home/deeptouch/datasets/third_200'  # 替换为您的根目录
    process_directory(root_directory)
