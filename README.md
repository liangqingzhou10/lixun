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
- 提供对齐前端标准的回放 HTTP 接口（支持图表与视频切片同步）
- 提供遥操作后台启停与实时 WebSocket 状态推送服务

## 目前关键功能

- VR 头显和手柄接入
- RosBridge 桥接 VR 控制消息
- Realman 左右机械臂连接与状态读取
- 数据采集与保存
- 左右灵巧手随机械臂一起连接
- 手柄 `gripper_cmd` 按键联动左右灵巧手固定手势
- 标准化 RESTful V1 API 数据读取与 MP4 回放
- 通过 HTTP POST/WebSocket 直接管理遥操作后台进程

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
```bash
cd /home/deeptouch/workspace/lixun/lixun/deeptouch/src/deeptouch_vr/platform-tools
./adb devices
```

## 启动端口转发
PC 端 Python 服务器监听 127.0.0.1:9001（或 0.0.0.0:9001）
```bash
./adb reverse tcp:9001 tcp:9001 
```

## 链接头显以及手柄功能 
```bash
cd /home/deeptouch/workspace/lixun/lixun/deeptouch
source /opt/ros/humble/setup.bash 
source install/setup.bash
ros2 launch /home/deeptouch/workspace/lixun/lixun/deeptouch/src/deeptouch_vr/launch/tele_opt_bringup.launch.py
```
- 注意链接到usb2.0，供电不足，会出现使用中> 充电，手柄小于30%及时更换电池

## 启动Realman机械臂控制节点
```bash
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
    ```bash
    # 构建ROS包
    colcon build
    ```

## root终端进行ros桥接：
```bash
cd /home/deeptouch/workspace/lixun/lixun/deeptouch
source /opt/ros/humble/setup.bash 
source install/setup.bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml delay_between_messages:=0.0
```

## 启动数采命令
在lerobot 环境下运行：

```bash
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
```

## HTTP 接口与服务集成说明 (V2.0 更新)

本项目的 HTTP 服务已经升级，全面对齐了前端的数据交互接口设计（PDF 规范）。不仅可以读取数据集元数据和实时相机画面，还集成了 **前端 ECharts 图表回放数据流**、**MP4 切片视频支持** 和 **遥操作后台进程管理**。

启动服务：

```bash
conda run -n lerobot python /home/deeptouch/workspace/lixun/http_dataset_server.py \
  --host 0.0.0.0 \
  --port 8000 \
  --dataset-root /home/deeptouch/workspace/lixun/datasets/recordings_action_test1 \
  --camera-config '{"cam0":{"type":"intelrealsense","serial_number_or_name":"243722073411","width":640,"height":480,"fps":30}}'
```

### 一、 V1 回放标准前端接口 (RESTful)

专为前端网页 `DataReplayView` 设计的完整载荷接口。

#### 1. 获取所有数据集列表
- **URL**: `GET /api/v1/datasets`
- **说明**: 返回数据集摘要，包含总集数、文件体积、版本号及每个 Episode 的摘要信息。

#### 2. 获取单集回放数据 (EpisodeData)
- **URL**: `GET /api/v1/datasets/:org/:dataset/episodes/:episodeId`
- **说明**: 返回整个 Episode 的完整数据。
- **关键返回内容**:
  - `flatChartData`: 已经展开的扁平化字典数组（包含 `timestamp`, `obs_state_xxx`, `action_xxx`, `task_index`），可直接喂给 ECharts 渲染。
  - `videosInfo`: 视频信息列表，包含 `segmentStart` 和 `url`。
  - `tasks`: 任务步骤名称数组，用于驱动前端侧边栏任务状态。

#### 3. 获取 MP4 视频流 (支持 Range 切片)
- **URL**: `GET /api/v1/datasets/:org/:dataset/episodes/:episodeId/videos/:camera`
- **说明**: 直接返回该集对应的 `.mp4` 视频。支持 HTTP `Range: bytes=X-Y` 请求，前端 `<video>` 标签可以直接 seek 拖动进度条。

### 二、 遥操作控制与状态接口 (Teleop)

专为遥操作页面（开始采集、停止采集、状态监控）设计的接口。

#### 1. 启动遥操作
- **URL**: `POST /api/teleop/start`
- **请求体**: `{"goal_id": "goal_123456", "command": "start"}`
- **说明**: 调用后台 Bash 脚本（`start_teleop.sh`）拉起 VR 和数采进程。

#### 2. 停止遥操作
- **URL**: `POST /api/teleop/stop`
- **请求体**: `{}`
- **说明**: 终止正在运行的遥操相关后台进程。

#### 3. 订阅遥操采集状态 (原生 WebSocket)
- **URL**: `ws://localhost:8000/api/teleop/feedback`
- **说明**: 前端建立 WebSocket 连接后，服务端会以 `1Hz` 频率推送当前状态。
- **返回内容**: 
  ```json
  { "status": 1, "duration": 42, "frame_count": 420 }
  // status: 0=空闲, 1=采集中, -1=异常
  ```

#### 4. 获取实时视频列表
- **URL**: `GET /api/teleop/cameras`
- **说明**: 返回当前可用的实时摄像头列表。包含推流直链 `stream_url` (MJPEG 格式) 和 单帧快照 `snapshot_url`。

### 三、 实时监控与调试基础接口 (旧版兼容)

如果仅作为调试用途，你依然可以使用以下接口：

- `GET /health`：健康检查。
- `GET /api/summary`：数据集基础统计与字段结构字典。
- `GET /api/episodes`：列出原始 episode 属性。
- `GET /api/frames?episode_index=0`：按帧分页查询未经扁平化处理的原始嵌套数据（含手柄夹爪信号）。
- `GET /api/live/stream?camera=cam0`：直接获取 MJPEG 实时推流。
- `GET /api/live/frame?camera=cam0`：获取单张 JPEG 截图。

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
- **确保你在 `http_dataset_server.py` 中将 `START_SCRIPT` 和 `STOP_SCRIPT` 替换为了你真实的遥操作 shell 脚本路径**。

## 关键代码位置

- 一键启动脚本：`start_vr_data_collection.sh`
- HTTP 数据服务与后台控制：`http_dataset_server.py`
- 灵巧手底层控制：`lixun/deeptouch/src/deeptouch_vr/hand.py`
- VR 遥操作接入：`lixun/lerobot/teleoperators/ros_vr/ros_bridge_teleop.py`
- VR 数采脚本：`lixun/lerobot/scripts/lerobot_record_vr.py`
- 本说明文件：`README.md`

## 当前实现结论

当前项目已经实现：

- VR 手柄控制双机械臂
- `gripper_cmd` 驱动灵巧手执行固定张开/闭合动作
- 录制数据时写入夹爪开合信号
- **完全对齐前端规范的 HTTP 回放服务，直接支撑浏览器 ECharts 和 Video 标签渲染**
- **原生 WebSocket 服务端状态推送与 POST 遥操启停指令下发**
- 通过一键脚本按正确环境顺序拉起整套系统

## 后续可以继续优化

- 增加按键去抖，避免频繁点击时重复动作
- 增加灵巧手连接失败时的界面提示
- 增加左右手独立角度配置，方便不同手势切换