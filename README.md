# Lixun VR 数采系统总说明

这个 README 现在作为 `lixun` 项目里和 VR 遥操作、机械臂控制、灵巧手联动、数采录制、HTTP 数据查看相关的统一说明书。

如果你后面只想看一个文档，优先看这个文件即可。

## 项目目标

这个项目主要用于：

- 使用 VR 头显和手柄遥操作双机械臂
- 通过 `rosbridge` 把 VR 控制消息桥接给 `lerobot`
- 在录制数据时同步采集：
  - 相机图像
  - 左右机械臂状态
  - 手柄开合按键信号
  - 左右灵巧手联动状态

## 目前关键功能

- VR 头显和手柄接入
- RosBridge 桥接 VR 控制消息
- Realman 左右机械臂连接与状态读取
- 数据采集与保存
- 左右灵巧手随机械臂一起连接
- 手柄 `gripper_cmd` 按键联动左右灵巧手固定手势

## 推荐使用方式

现在最推荐直接使用项目根目录的一键脚本：

```bash
cd /home/deeptouch/workspace/lixun
bash start_vr_data_collection.sh
```

这个脚本已经固定好正确顺序：

- 先在非 conda 环境下连接 VR
- 再在非 conda 环境下开启手柄功能
- 再在非 conda 环境下连接机械臂和左右灵巧手
- 再在非 conda 环境下启动 `rosbridge`
- 最后在 `lerobot` 环境里启动数采

也就是说：

- `VR / ROS / rosbridge / 机械臂 / 灵巧手` 相关步骤不走 conda
- `lerobot_record_vr.py` 数采命令走 `lerobot` conda 环境

## 一键启动数采系统

执行：

```bash
cd /home/deeptouch/workspace/lixun
bash start_vr_data_collection.sh
```

### 脚本默认参数

默认参数如下：

- 左机械臂 IP：`192.168.0.18`
- 右机械臂 IP：`192.168.0.19`
- 相机序列号：`243722073411`
- 左灵巧手：`/dev/dexhand_left`
- 右灵巧手：`/dev/dexhand_right`
- 数据集 repo_id：`deeptouch/realman_action_test`
- 数据目录：`/home/deeptouch/workspace/lixun/datasets/recordings_action_test1`
- 任务描述：`vr test`
- 采集环境名：`lerobot`
- ROS 发行版：`humble`

### 常见改法

修改保存目录和任务名：

```bash
bash start_vr_data_collection.sh \
  --dataset-root "/home/deeptouch/workspace/lixun/datasets/demo_001" \
  --task "双臂搬运测试"
```

如果你反复执行同一个命令，而原始目录已经存在，脚本会自动换成一个带时间戳的新目录，避免因为目录已存在而启动失败。

如果你要继续写入一个已经存在的数据集目录：

```bash
bash start_vr_data_collection.sh \
  --dataset-root "/home/deeptouch/workspace/lixun/datasets/recordings_action_test1" \
  --resume
```

如果你的 conda 环境名不是 `lerobot`：

```bash
bash start_vr_data_collection.sh --lerobot-env 你的环境名
```

如果采集结束后，你想保留后台服务，不自动停止：

```bash
bash start_vr_data_collection.sh --keep-services
```

### 一键脚本运行前检查

建议先确认：

- VR 已打开 OpenXR 应用
- 头显已经通过 USB 正常连接，`adb devices` 能看到设备
- 左右机械臂 IP 没写错
- 左右灵巧手别名存在：`/dev/dexhand_left`、`/dev/dexhand_right`
- ROS 工作区已经编译完成，`/home/deeptouch/workspace/lixun/lixun/deeptouch/install/setup.bash` 存在

### 一键脚本日志位置

后台服务日志默认写到：

```bash
/home/deeptouch/workspace/lixun/logs/vr_data_collection/
```

如果某一步失败，优先看这里的：

- `vr_teleop.log`
- `dual_arms_and_dexhands.log`
- `rosbridge.log`

## 手动分步启动

如果你不想用一键脚本，也可以手动按下面步骤启动。

## 启动VR

打开VR的 open XR的app

## 连接VR设备
```
cd /home/deeptouch/workspace/lixun/lixun/deeptouch/src/deeptouch_vr/platform-tools
./adb devices
```

## 启动端口转发
PC 端 Python 服务器监听 127.0.0.1:9001（或 0.0.0.0:9001）
```
./adb reverse tcp:9001 tcp:9001 
```

## 链接头显以及手柄功能 
```
cd /home/deeptouch/workspace/lixun/lixun/deeptouch
source /opt/ros/humble/setup.bash 
source install/setup.bash
ros2 launch /home/deeptouch/workspace/lixun/lixun/deeptouch/src/deeptouch_vr/launch/tele_opt_bringup.launch.py
```
- 注意链接到usb2.0，供电不足，会出现使用中> 充电，手柄小于30%及时更换电池

## 启动Realman机械臂控制节点
```
cd /home/deeptouch/workspace/lixun/lixun/deeptouch
source /opt/ros/humble/setup.bash 
source install/setup.bash
ros2 launch deeptouch_arm_controller dual_arms_control_node.launch.py
```
- 这条命令现在会同时启动：
  - 左机械臂控制节点
  - 右机械臂控制节点
  - 左右灵巧手桥接节点
- 也就是说，你执行这一条命令时，就会同时去连接机械臂和左右两只灵巧手。
- 默认固定接口为：
  - 左手：`/dev/dexhand_left`
  - 右手：`/dev/dexhand_right`
- 当收到 `gripper_cmd=true` 时，对应侧灵巧手执行：
  - `set_joint_angles([75, 70, 60, 0, 0, 0], duration=0.5)`
- 当收到 `gripper_cmd=false` 时，对应侧灵巧手张开：
  - `set_joint_angles([0, 0, 0, 0, 0, 0], duration=0.5)`
- 注意ROS相关修改后需要重新编译
    ```
    # 构建ROS包
    colcon build
    ```

# root终端进行ros桥接：
cd /home/deeptouch/workspace/lixun/lixun/deeptouch
source /opt/ros/humble/setup.bash 
source install/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml delay_between_messages:=0.0

# 以下为roslibpy实例代码（勿删）
#连接到刚才启动的 rosbridge
client = roslibpy.Ros(host='localhost', port=9090)
client.run()
import roslibpy
import time
#连接到本地的 rosbridge (端口 9090)
client = roslibpy.Ros(host='localhost', port=9090)
def on_connect():
    print("✅ [成功] LeRobot 环境已连接到 ROS 2 系统！")
def on_disconnect():

    print("❌ [断开] 连接丢失")
client.on_ready(on_connect)

client.on_close(on_disconnect)

client.run()

## 启动数采命令
在lerobot 环境下运行：

python /home/deeptouch/workspace/lixun/lixun/lerobot/scripts/lerobot_record_vr.py \
  --robot.type=realman_robot \
  --robot.use_ros_controller=true \
  --robot.left_ip="192.168.0.18" \
  --robot.right_ip="192.168.0.19" \
  --robot.cameras='{
    "cam0": {"type": "intelrealsense", "serial_number_or_name": "243722073411", "width": 640, "height": 480, "fps": 30}
  }' \
  --teleop.type=ros_vr_teleop \
  --teleop.rosbridge_host="localhost" \
  --teleop.left_topic="/teleoperation/left_cmd" \
  --teleop.right_topic="/teleoperation/right_cmd" \
  --teleop.use_dex_hands=true \
  --teleop.left_hand_port="/dev/dexhand_left" \
  --teleop.right_hand_port="/dev/dexhand_right" \
  --teleop.hand_baudrate=115200 \
  --dataset.repo_id="deeptouch/realman_action_test" \
  --dataset.root="/home/deeptouch/workspace/lixun/datasets/recordings_action_test1" \
  --dataset.fps=10 \
  --dataset.single_task="vr test" \
  --dataset.video=true \
  --play_sounds=False

## HTTP 可获取内容说明

如果你想通过浏览器、前端页面或者接口调试工具直接查看数据集内容和实时相机画面，可以启动：

```bash
conda run -n lerobot python /home/deeptouch/workspace/lixun/http_dataset_server.py \
  --host 0.0.0.0 \
  --port 8000 \
  --dataset-root /home/deeptouch/workspace/lixun/datasets/recordings_action_test1 \
  --camera-config '{"cam0":{"type":"intelrealsense","serial_number_or_name":"243722073411","width":640,"height":480,"fps":30}}'
```

说明：

- `--dataset-root`：要查看的数据集目录。
- `--camera-config`：实时相机配置，不传也能看数据集元数据，但不能看实时相机画面。
- 这个服务已经带了 `CORS` 头，前端页面可以直接跨域访问。

### 1. 服务根地址

访问：

```text
http://localhost:8000/
```

可以拿到：

- 服务名称
- 当前支持的所有接口列表

### 2. 健康检查

访问：

```text
http://localhost:8000/health
```

返回内容：

- `ok`
- `status`

正常时一般会返回：

```json
{"ok": true, "status": "running"}
```

### 3. 数据集总览

访问：

```text
http://localhost:8000/api/summary
```

返回内容里重点有：

- `dataset_root`：当前数据集目录
- `robot_type`：机器人类型
- `fps`：数据集帧率
- `total_episodes`：总 episode 数量
- `total_frames`：总帧数
- `camera_features`：数据集里有哪些图像流
- `observation_state_names`：状态向量字段名
- `action_names`：动作向量字段名
- `dex_hand_fields`：灵巧手开合信号字段
- `dex_hand_note`：当前保存的是开合信号，不是 6 个关节角
- `episode_metadata_count`：episode 元数据条数

适合用来快速确认：

- 数据集有没有录到内容
- 相机字段名是否正确
- 动作和状态字段是否符合预期

### 4. 查看 episode 列表

访问：

```text
http://localhost:8000/api/episodes?limit=20&offset=0
```

参数说明：

- `limit`：一次返回多少条
- `offset`：从第几条开始

返回内容：

- `total`：总 episode 数
- `items`：episode 列表

`items` 里返回的是 `meta/episodes` 里的原始字段，通常用于：

- 列出所有 episode
- 做分页
- 让前端先选一个 episode，再去查帧

### 5. 查看某个 episode 的帧数据

访问：

```text
http://localhost:8000/api/frames?episode_index=0&limit=50&offset=0
```

参数说明：

- `episode_index`：必填，要查看哪一个 episode
- `limit`：一次取多少帧
- `offset`：从第几帧开始

返回内容：

- `episode_index`
- `total`
- `items`

每一条 `items` 里重点字段有：

- `episode_index`
- `frame_index`
- `timestamp`
- `dataset_index`
- `task_index`
- `task`
- `robot.left_arm`
- `robot.right_arm`
- `dex_hand.left_hand.close_signal`
- `dex_hand.left_hand.state`
- `dex_hand.right_hand.close_signal`
- `dex_hand.right_hand.state`
- `raw_action`
- `raw_observation_state`

这里特别注意：

- `dex_hand.left_hand.state` / `dex_hand.right_hand.state` 会被整理成 `open` 或 `closed`
- `close_signal` 本质上还是记录值：
  - `0.0` 约等于张开
  - `1.0` 约等于闭合
- `raw_action` 是原始动作向量
- `raw_observation_state` 是原始机器人状态向量

这个接口最适合做：

- 回放时序数据
- 检查某一段动作是否录对
- 检查灵巧手开合信号是否同步写入

### 6. 查看最新一帧

访问：

```text
http://localhost:8000/api/latest-frame
```

或者指定某个 episode：

```text
http://localhost:8000/api/latest-frame?episode_index=0
```

返回内容：

- `item`

这个 `item` 的结构和 `/api/frames` 里的单条帧数据基本一致。

适合用来做：

- 前端轮询最新状态
- 调试当前最近一次采集结果

### 7. 查看实时相机状态

访问：

```text
http://localhost:8000/api/live/status
```

返回内容：

- `configured`：是否传入了 `--camera-config`
- `started`：实时相机是否已成功启动
- `error`：启动失败时的报错信息
- `cameras`：当前可用相机名列表

如果你看到：

- `configured=false`

说明你启动 HTTP 服务时没有传相机配置，所以实时画面接口不能用。

### 8. 获取一张实时相机 JPEG 图片

访问：

```text
http://localhost:8000/api/live/frame?camera=cam0
```

参数说明：

- `camera`：必填，相机名，比如 `cam0`

返回类型：

- 不是 JSON
- 直接返回 `image/jpeg`

适合用来做：

- 浏览器直接看单张图
- 前端定时刷新图片
- 调试相机是否真的出图

### 9. 获取实时相机视频流

访问：

```text
http://localhost:8000/api/live/stream?camera=cam0&fps=10
```

参数说明：

- `camera`：必填，相机名
- `fps`：可选，推流频率，默认 `10`

返回类型：

- 不是 JSON
- 返回 `multipart/x-mixed-replace`
- 本质上是 MJPEG 流

适合用来做：

- 浏览器实时预览
- 前端视频监看页面

### 10. 常见报错含义

如果接口返回：

- `Missing required query parameter: episode_index`
  - 说明你请求 `/api/frames` 时没传 `episode_index`
- `Missing required query parameter: camera`
  - 说明你请求实时相机接口时没传 `camera`
- `Unknown camera: cam0`
  - 说明 `camera` 名字不在 `--camera-config` 里
- `Live camera is not configured.`
  - 说明启动 HTTP 服务时没有传 `--camera-config`
- `Dataset info not found`
  - 说明 `--dataset-root` 不是一个有效的 LeRobot 数据集目录

### 11. 最常用访问示例

浏览器直接打开：

```text
http://localhost:8000/api/summary
http://localhost:8000/api/episodes?limit=10&offset=0
http://localhost:8000/api/frames?episode_index=0&limit=20&offset=0
http://localhost:8000/api/latest-frame
http://localhost:8000/api/live/status
http://localhost:8000/api/live/frame?camera=cam0
http://localhost:8000/api/live/stream?camera=cam0&fps=10
```

如果你要给前端对接，推荐优先使用：

- `/api/summary`：先拿字段结构
- `/api/episodes`：拿 episode 列表
- `/api/frames`：拿帧级别数据
- `/api/latest-frame`：拿最新一帧
- `/api/live/frame` 或 `/api/live/stream`：拿实时图像

## 夹爪信号记录说明（已修复）

- 采集动作中的 `left_arm_gripper` / `right_arm_gripper` 现在使用：
  - 直接读取手柄消息 `TeleOptCmd.gripper_cmd`（`true=闭合`, `false=张开`）。
- 记录值语义：`0.0=张开`，`1.0=闭合`。
- 如果你发现夹爪值一直不变，优先检查：
  - ROS/VR 控制节点是否真的发布了 `gripper_cmd`；
  - 当前录制订阅的话题是否与控制话题一致（`left_topic/right_topic`）。

## 灵巧手联动（替代夹爪）

现在 `ros_vr_teleop` 已支持：
- 在连接机械臂时，同时连接左右灵巧手；
- 监听 `TeleOptCmd.gripper_cmd`，按键按下时执行固定弯曲角度；
- 左右手使用固定串口配置，防止插拔后端口变化导致连接失败。

默认控制逻辑：
- `gripper_cmd=true`：执行 `set_joint_angles([75, 70, 60, 0, 0, 0], duration=0.5)`；
- `gripper_cmd=false`：执行张开手势 `[0, 0, 0, 0, 0, 0]`。

对应配置项（`RosBridgeTeleopConfig`）：
- `teleop.use_dex_hands=true`
- `teleop.left_hand_port="/dev/dexhand_left"`
- `teleop.right_hand_port="/dev/dexhand_right"`
- `teleop.hand_baudrate=115200`
- `teleop.hand_close_angles="[75,70,60,0,0,0]"`
- `teleop.hand_open_angles="[0,0,0,0,0,0]"`
- `teleop.hand_move_duration=0.5`

### 固定左右手接口（强烈建议）

建议通过 `udev` 给左右灵巧手做固定别名，例如：
- 左手：`/dev/dexhand_left`
- 右手：`/dev/dexhand_right`

这样即使 USB 重新插拔，程序也能稳定连接到正确手。

### 安装 udev 固定规则

项目根目录已经提供：
- `99-dexhand.rules`
- `install_dexhand_udev.sh`

当前这台机器实测后的正确左右手映射是：
- `1-1` -> 右手
- `1-2` -> 左手

执行：

```bash
cd /home/deeptouch/workspace/lixun
bash install_dexhand_udev.sh
```

安装后检查：

```bash
ls -l /dev/dexhand_left /dev/dexhand_right
```

如果你暂时还没有配置 `udev` 固定别名，也可以先直接写死当前串口，例如：
- 左手：`--teleop.left_hand_port="/dev/ttyUSB0"`
- 右手：`--teleop.right_hand_port="/dev/ttyUSB1"`

但这种方式在重新插拔后很可能会变化，所以更推荐固定成：
- `/dev/dexhand_left`
- `/dev/dexhand_right`

## 启动时需要重点关注

- 先确保 ROS、RosBridge、VR 话题发布正常
- 再确认左右机械臂 IP 正确
- 最后确认左右灵巧手串口固定名存在
- 如果一键脚本提示已有旧进程在运行，要先停止旧进程再重新启动
- 如果 `/dev/dexhand_left` 或 `/dev/dexhand_right` 不存在，优先检查 `udev` 规则是否已安装生效

## 关键代码位置

- 一键启动脚本：`start_vr_data_collection.sh`
- HTTP 数据服务：`http_dataset_server.py`
- 灵巧手底层控制：`lixun/deeptouch/src/deeptouch_vr/hand.py`
- VR 遥操作接入：`lixun/lerobot/teleoperators/ros_vr/ros_bridge_teleop.py`
- VR 数采脚本：`lixun/lerobot/scripts/lerobot_record_vr.py`
- 本说明文件：`lixun/lerobot/teleoperators/ros_vr/README.md`

## 当前实现结论

当前项目已经实现：

- VR 手柄控制双机械臂
- `gripper_cmd` 驱动灵巧手执行固定张开/闭合动作
- 录制数据时写入夹爪开合信号
- 通过 HTTP 接口读取数据集内容和实时相机画面
- 通过一键脚本按正确环境顺序拉起整套系统

## 后续可以继续优化

- 增加按键去抖，避免频繁点击时重复动作
- 增加灵巧手连接失败时的界面提示
- 增加左右手独立角度配置，方便不同手势切换
- 增加停止脚本或图形化启动面板，进一步降低使用门槛