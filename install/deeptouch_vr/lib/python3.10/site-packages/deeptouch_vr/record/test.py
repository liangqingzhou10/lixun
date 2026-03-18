import subprocess  
import json  
import os  
import glob  

def get_video_frame_count(video_path):  
    """  
    使用 ffprobe 获取视频文件的帧数。  

    Args:  
      video_path: 视频文件的路径。  

    Returns:  
      视频的帧数，如果出错则返回 None。  
    """  
    try:  
        ffprobe_path = "/usr/bin/ffprobe"  # 替换为你的 ffprobe 可执行文件的完整路径  
        command = [  
            ffprobe_path,  
            "-v", "error",  
            "-select_streams", "v:0",  
            "-show_entries", "stream=nb_frames",  
            "-of", "default=nokey=1:noprint_wrappers=1",  
            video_path  
        ]  
        result = subprocess.run(command, capture_output=True, text=True, check=True)  
        frame_count = int(result.stdout.strip())  
        return frame_count  
    except subprocess.CalledProcessError as e:  
        print(f"Error running ffprobe: {e}")  
        return None  
    except ValueError:  
        print("Could not parse frame count from ffprobe output.")  
        return None  

def main():  
    video_folder = "/home/deeptouch/datasets/eighth_150/left_hand/1/videos"  # 替换为你的视频文件夹路径  
    video_files = glob.glob(os.path.join(video_folder, "*.mp4"))  # 可以根据需要修改文件扩展名  

    if not video_files:  
        print(f"在 {video_folder} 中没有找到视频文件。")  
        return  

    for video_file in video_files:  
        frame_count = get_video_frame_count(video_file)  
        if frame_count is not None:  
            print(f"{video_file}: {frame_count} 帧")  
        else:  
            print(f"无法获取 {video_file} 的帧数")  

if __name__ == "__main__":  
    main()  