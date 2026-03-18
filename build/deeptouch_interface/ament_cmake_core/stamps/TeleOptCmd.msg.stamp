# 位姿数据消息定义
# deeptouch_interface/TeleOptCmd.msg

# 是否随动  true: 随动  false: 不随动
bool is_follow

# 是否校准起始位姿  true: 校准起始位姿  false: 不校准
bool is_calibrate_start_pose

# 是否绝对位姿  true: 绝对位姿  false: 相对位姿
bool is_absolute_pose

# 是否回到初始位置
bool is_initial_pose

# 手部位姿 
geometry_msgs/Pose hand_pose

# 夹爪指令
bool gripper_cmd      #  Gripper 0: open; 1: close

# 开始记录数据
string record_state

# 尺度（手部位姿缩放）
float32 scale

uint8 primary_thumb  # 摇杆按下

# 本次录制的评分（仅 HIL-SERL 使用）：
#  1 = 成功, 255 = 失败, 0 = 未标记
uint8 rating