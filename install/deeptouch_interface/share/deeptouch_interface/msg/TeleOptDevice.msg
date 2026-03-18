# VR完整数据帧消息定义
# deeptouch_interface/TeleOptDevice.msg

# 时间戳
float32 timestamp
uint32 frame_id      # 帧序号

# 手柄状态
deeptouch_interface/HandTouch hand_touch

# 设备位姿
geometry_msgs/Pose hand_pose

# 头部位姿
geometry_msgs/Pose head_pose

