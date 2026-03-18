#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$SCRIPT_DIR"
ROS_WS="$WORKSPACE_ROOT/lixun/deeptouch"
ADB_BIN="$ROS_WS/src/deeptouch_vr/platform-tools/adb"
RECORD_SCRIPT="$WORKSPACE_ROOT/lixun/lerobot/scripts/lerobot_record_vr.py"
LOG_DIR="$WORKSPACE_ROOT/logs/vr_data_collection"

LEROBOT_ENV_NAME="${LEROBOT_ENV_NAME:-lerobot}"
LEFT_IP="${LEFT_IP:-192.168.0.18}"
RIGHT_IP="${RIGHT_IP:-192.168.0.19}"
CAMERA_SERIAL="${CAMERA_SERIAL:-243722073411}"
DATASET_REPO_ID="${DATASET_REPO_ID:-deeptouch/realman_action_test}"
DATASET_ROOT="${DATASET_ROOT:-$WORKSPACE_ROOT/datasets/recordings_action_test1}"
DATASET_FPS="${DATASET_FPS:-10}"
DATASET_TASK="${DATASET_TASK:-vr test}"
LEFT_TOPIC="${LEFT_TOPIC:-/teleoperation/left_cmd}"
RIGHT_TOPIC="${RIGHT_TOPIC:-/teleoperation/right_cmd}"
LEFT_HAND_PORT="${LEFT_HAND_PORT:-/dev/dexhand_left}"
RIGHT_HAND_PORT="${RIGHT_HAND_PORT:-/dev/dexhand_right}"
HAND_BAUDRATE="${HAND_BAUDRATE:-115200}"
ROSBRIDGE_HOST="${ROSBRIDGE_HOST:-localhost}"
ROS_DISTRO="${ROS_DISTRO:-humble}"
KEEP_SERVICES="${KEEP_SERVICES:-0}"
RESUME_RECORDING="${RESUME_RECORDING:-0}"

PIDS=()

usage() {
  cat <<EOF
用法：
  bash start_vr_data_collection.sh [参数]

常用参数：
  --left-ip IP                左机械臂 IP，默认：$LEFT_IP
  --right-ip IP               右机械臂 IP，默认：$RIGHT_IP
  --camera-serial SERIAL      相机序列号，默认：$CAMERA_SERIAL
  --dataset-repo-id ID        数据集 repo_id，默认：$DATASET_REPO_ID
  --dataset-root PATH         数据保存目录，默认：$DATASET_ROOT
  --dataset-fps FPS           采集帧率，默认：$DATASET_FPS
  --task TEXT                 任务描述，默认：$DATASET_TASK
  --lerobot-env NAME          conda 环境名，默认：$LEROBOT_ENV_NAME
  --left-hand-port PATH       左灵巧手串口，默认：$LEFT_HAND_PORT
  --right-hand-port PATH      右灵巧手串口，默认：$RIGHT_HAND_PORT
  --ros-distro NAME           ROS 发行版，默认：$ROS_DISTRO
  --resume                    继续写入已存在的数据集目录
  --keep-services             采集结束后不自动停止 ROS 相关进程
  -h, --help                  查看帮助

示例：
  bash start_vr_data_collection.sh \\
    --dataset-root "$WORKSPACE_ROOT/datasets/demo_001" \\
    --task "双臂搬运测试"
EOF
}

print_step() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

require_file() {
  local path="$1"
  if [[ ! -e "$path" ]]; then
    echo "[错误] 文件不存在：$path" >&2
    exit 1
  fi
}

require_command() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    echo "[错误] 缺少命令：$name" >&2
    exit 1
  fi
}

strip_conda_path() {
  local old_path="$1"
  local new_path=""
  local part=""
  local old_ifs="$IFS"
  IFS=':'
  for part in $old_path; do
    case "$part" in
      *conda*|*miniconda*|*anaconda*)
        continue
        ;;
    esac
    if [[ -z "$new_path" ]]; then
      new_path="$part"
    else
      new_path="$new_path:$part"
    fi
  done
  IFS="$old_ifs"
  printf '%s\n' "$new_path"
}

ensure_not_running() {
  local pattern="$1"
  local label="$2"
  if pgrep -af "$pattern" >/dev/null 2>&1; then
    echo "[错误] 检测到已有 $label 正在运行，请先停止旧进程再启动。" >&2
    pgrep -af "$pattern" || true
    exit 1
  fi
}

wait_for_port() {
  local host="$1"
  local port="$2"
  local timeout_s="$3"
  local start_ts
  start_ts="$(date +%s)"

  while true; do
    if python3 - "$host" "$port" <<'PY'
import socket
import sys

host = sys.argv[1]
port = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(1.0)
try:
    sock.connect((host, port))
except OSError:
    sys.exit(1)
else:
    sys.exit(0)
finally:
    sock.close()
PY
    then
      return 0
    fi

    if (( "$(date +%s)" - start_ts >= timeout_s )); then
      return 1
    fi
    sleep 1
  done
}

start_plain_service() {
  local name="$1"
  local command="$2"
  local log_file="$LOG_DIR/${name}.log"
  local clean_path

  clean_path="$(strip_conda_path "${PATH:-/usr/bin:/bin}")"

  print_step "启动：$name"
  echo "[日志] $log_file"

  env \
    -u CONDA_DEFAULT_ENV \
    -u CONDA_PREFIX \
    -u CONDA_PROMPT_MODIFIER \
    -u CONDA_EXE \
    -u CONDA_PYTHON_EXE \
    -u CONDA_SHLVL \
    -u _CE_CONDA \
    -u _CE_M \
    HOME="$HOME" \
    USER="${USER:-deeptouch}" \
    SHELL="${SHELL:-/bin/bash}" \
    TERM="${TERM:-xterm-256color}" \
    PATH="$clean_path" \
    bash -lc "$command" >"$log_file" 2>&1 &

  local pid=$!
  PIDS+=("$pid")
  sleep 2

  if ! kill -0 "$pid" >/dev/null 2>&1; then
    echo "[错误] $name 启动失败，请查看日志：$log_file" >&2
    exit 1
  fi
}

cleanup() {
  if [[ "$KEEP_SERVICES" == "1" ]]; then
    echo
    echo "[提示] 已按要求保留后台 ROS 服务，不自动停止。"
    return
  fi

  if [[ "${#PIDS[@]}" -eq 0 ]]; then
    return
  fi

  echo
  echo "[清理] 正在停止本次脚本拉起的后台服务..."
  for pid in "${PIDS[@]}"; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
    fi
  done
}

prepare_dataset_root() {
  local requested_root="$1"
  local requested_parent
  local requested_name
  local final_root="$requested_root"

  requested_parent="$(dirname "$requested_root")"
  requested_name="$(basename "$requested_root")"
  mkdir -p "$requested_parent"

  if [[ "$RESUME_RECORDING" == "1" ]]; then
    if [[ ! -d "$requested_root" ]]; then
      echo "[错误] --resume 模式要求目录已存在：$requested_root" >&2
      exit 1
    fi
    printf '%s\n' "$requested_root"
    return 0
  fi

  if [[ -e "$requested_root" ]]; then
    final_root="${requested_parent}/${requested_name}_$(date +%Y%m%d_%H%M%S)"
    echo "[提示] 原始数据目录已存在，自动切换到新目录：$final_root" >&2
  fi

  printf '%s\n' "$final_root"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --left-ip)
      LEFT_IP="$2"
      shift 2
      ;;
    --right-ip)
      RIGHT_IP="$2"
      shift 2
      ;;
    --camera-serial)
      CAMERA_SERIAL="$2"
      shift 2
      ;;
    --dataset-repo-id)
      DATASET_REPO_ID="$2"
      shift 2
      ;;
    --dataset-root)
      DATASET_ROOT="$2"
      shift 2
      ;;
    --dataset-fps)
      DATASET_FPS="$2"
      shift 2
      ;;
    --task)
      DATASET_TASK="$2"
      shift 2
      ;;
    --lerobot-env)
      LEROBOT_ENV_NAME="$2"
      shift 2
      ;;
    --left-hand-port)
      LEFT_HAND_PORT="$2"
      shift 2
      ;;
    --right-hand-port)
      RIGHT_HAND_PORT="$2"
      shift 2
      ;;
    --ros-distro)
      ROS_DISTRO="$2"
      shift 2
      ;;
    --resume)
      RESUME_RECORDING=1
      shift
      ;;
    --keep-services)
      KEEP_SERVICES=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[错误] 不支持的参数：$1" >&2
      usage
      exit 1
      ;;
  esac
done

mkdir -p "$LOG_DIR"

require_command bash
require_command python3
require_command conda
require_file "$ADB_BIN"
require_file "$ROS_WS/install/setup.bash"
require_file "$RECORD_SCRIPT"

DATASET_ROOT="$(prepare_dataset_root "$DATASET_ROOT")"

ensure_not_running "tele_opt_bringup.launch.py" "VR 手柄节点"
ensure_not_running "dual_arms_control_node.launch.py" "机械臂/灵巧手控制节点"
ensure_not_running "rosbridge_websocket_launch.xml" "rosbridge"
ensure_not_running "lerobot_record_vr.py" "数采脚本"

if [[ ! -e "$LEFT_HAND_PORT" ]]; then
  echo "[警告] 左灵巧手串口不存在：$LEFT_HAND_PORT"
fi

if [[ ! -e "$RIGHT_HAND_PORT" ]]; then
  echo "[警告] 右灵巧手串口不存在：$RIGHT_HAND_PORT"
fi

trap cleanup EXIT INT TERM

print_step "第 1 步：检查 VR 设备连接"
ADB_OUTPUT="$("$ADB_BIN" devices)"
echo "$ADB_OUTPUT"
if ! printf '%s\n' "$ADB_OUTPUT" | awk 'NR > 1 && $2 == "device" { found = 1 } END { exit(found ? 0 : 1) }'; then
  echo "[错误] 没有检测到可用的 VR 设备，请先连接头显并打开 OpenXR 应用。" >&2
  exit 1
fi

print_step "第 2 步：配置 ADB 端口转发"
"$ADB_BIN" reverse tcp:9001 tcp:9001

ROS_ENV_CMD="source /opt/ros/$ROS_DISTRO/setup.bash && source \"$ROS_WS/install/setup.bash\""

start_plain_service \
  "vr_teleop" \
  "$ROS_ENV_CMD && ros2 launch \"$ROS_WS/src/deeptouch_vr/launch/tele_opt_bringup.launch.py\""

start_plain_service \
  "dual_arms_and_dexhands" \
  "$ROS_ENV_CMD && ros2 launch deeptouch_arm_controller dual_arms_control_node.launch.py"

start_plain_service \
  "rosbridge" \
  "$ROS_ENV_CMD && ros2 launch rosbridge_server rosbridge_websocket_launch.xml delay_between_messages:=0.0"

print_step "第 3 步：等待 rosbridge 就绪"
if ! wait_for_port "$ROSBRIDGE_HOST" 9090 20; then
  echo "[错误] rosbridge 20 秒内没有启动成功，请查看日志：$LOG_DIR/rosbridge.log" >&2
  exit 1
fi
echo "[成功] rosbridge 已就绪：$ROSBRIDGE_HOST:9090"

CAMERA_CONFIG=$(cat <<EOF
{
  "cam0": {
    "type": "intelrealsense",
    "serial_number_or_name": "$CAMERA_SERIAL",
    "width": 640,
    "height": 480,
    "fps": 30
  }
}
EOF
)

print_step "第 4 步：在 conda 环境 $LEROBOT_ENV_NAME 中启动数采"
echo "[提示] 录制结束后按 Ctrl+C，脚本会自动停止本次拉起的 ROS 服务。"
echo "[提示] 本次数据目录：$DATASET_ROOT"

record_cmd=(
  conda run -n "$LEROBOT_ENV_NAME" --no-capture-output
  python "$RECORD_SCRIPT"
  --robot.type=realman_robot
  --robot.use_ros_controller=true
  --robot.left_ip="$LEFT_IP"
  --robot.right_ip="$RIGHT_IP"
  --robot.cameras="$CAMERA_CONFIG"
  --teleop.type=ros_vr_teleop
  --teleop.rosbridge_host="$ROSBRIDGE_HOST"
  --teleop.left_topic="$LEFT_TOPIC"
  --teleop.right_topic="$RIGHT_TOPIC"
  --teleop.use_dex_hands=true
  --teleop.left_hand_port="$LEFT_HAND_PORT"
  --teleop.right_hand_port="$RIGHT_HAND_PORT"
  --teleop.hand_baudrate="$HAND_BAUDRATE"
  --dataset.repo_id="$DATASET_REPO_ID"
  --dataset.root="$DATASET_ROOT"
  --dataset.fps="$DATASET_FPS"
  --dataset.single_task="$DATASET_TASK"
  --dataset.video=true
  --play_sounds=False
)

if [[ "$RESUME_RECORDING" == "1" ]]; then
  record_cmd+=(--resume=true)
fi

"${record_cmd[@]}"
