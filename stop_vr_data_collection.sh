#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$SCRIPT_DIR"
ROS_WS="$WORKSPACE_ROOT/lixun/deeptouch"
ADB_BIN="$ROS_WS/src/deeptouch_vr/platform-tools/adb"
WAIT_SECONDS="${WAIT_SECONDS:-5}"
FORCE_KILL="${FORCE_KILL:-1}"
REMOVE_ADB_REVERSE="${REMOVE_ADB_REVERSE:-1}"

PATTERNS=(
  "lerobot_record_vr.py"
  "rosbridge_websocket_launch.xml"
  "rosbridge_websocket"
  "dual_arms_control_node.launch.py"
  "tele_opt_bringup.launch.py"
  "tele_opt_cmd_publish.py"
  "tele_opt_device_publish.py"
)

usage() {
  cat <<EOF
用法：
  bash stop_vr_data_collection.sh [参数]

常用参数：
  --wait-seconds N        发送 TERM 后等待秒数，默认：$WAIT_SECONDS
  --no-force             不进行强制 kill -9
  --keep-adb-reverse     不移除 adb reverse tcp:9001
  -h, --help             查看帮助

示例：
  bash stop_vr_data_collection.sh
  bash stop_vr_data_collection.sh --wait-seconds 8
EOF
}

print_step() {
  echo
  echo "============================================================"
  echo "$1"
  echo "============================================================"
}

collect_pids() {
  local pattern="$1"
  pgrep -f "$pattern" 2>/dev/null || true
}

show_matches() {
  local pattern="$1"
  pgrep -af "$pattern" 2>/dev/null || true
}

terminate_pattern() {
  local pattern="$1"
  local label="$2"
  local pids

  pids="$(collect_pids "$pattern")"
  if [[ -z "$pids" ]]; then
    echo "[跳过] 未发现 $label"
    return 0
  fi

  echo "[处理] 正在停止 $label"
  show_matches "$pattern"
  while IFS= read -r pid; do
    [[ -z "$pid" ]] && continue
    kill "$pid" >/dev/null 2>&1 || true
  done <<< "$pids"
}

force_kill_pattern() {
  local pattern="$1"
  local label="$2"
  local pids

  pids="$(collect_pids "$pattern")"
  if [[ -z "$pids" ]]; then
    return 0
  fi

  echo "[强制] $label 仍未退出，执行 kill -9"
  show_matches "$pattern"
  while IFS= read -r pid; do
    [[ -z "$pid" ]] && continue
    kill -9 "$pid" >/dev/null 2>&1 || true
  done <<< "$pids"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --wait-seconds)
      WAIT_SECONDS="$2"
      shift 2
      ;;
    --no-force)
      FORCE_KILL=0
      shift
      ;;
    --keep-adb-reverse)
      REMOVE_ADB_REVERSE=0
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

print_step "第 1 步：停止数采和 ROS 相关进程"
terminate_pattern "lerobot_record_vr.py" "数采脚本"
terminate_pattern "rosbridge_websocket_launch.xml" "rosbridge launch"
terminate_pattern "rosbridge_websocket" "rosbridge websocket"
terminate_pattern "dual_arms_control_node.launch.py" "机械臂/灵巧手控制节点"
terminate_pattern "tele_opt_bringup.launch.py" "VR 启动节点"
terminate_pattern "tele_opt_cmd_publish.py" "VR 命令发布节点"
terminate_pattern "tele_opt_device_publish.py" "VR 设备发布节点"

if [[ "$WAIT_SECONDS" =~ ^[0-9]+$ ]] && (( WAIT_SECONDS > 0 )); then
  echo "[等待] 给进程 ${WAIT_SECONDS}s 自行退出..."
  sleep "$WAIT_SECONDS"
fi

if [[ "$FORCE_KILL" == "1" ]]; then
  print_step "第 2 步：清理残留进程"
  force_kill_pattern "lerobot_record_vr.py" "数采脚本"
  force_kill_pattern "rosbridge_websocket_launch.xml" "rosbridge launch"
  force_kill_pattern "rosbridge_websocket" "rosbridge websocket"
  force_kill_pattern "dual_arms_control_node.launch.py" "机械臂/灵巧手控制节点"
  force_kill_pattern "tele_opt_bringup.launch.py" "VR 启动节点"
  force_kill_pattern "tele_opt_cmd_publish.py" "VR 命令发布节点"
  force_kill_pattern "tele_opt_device_publish.py" "VR 设备发布节点"
fi

if [[ "$REMOVE_ADB_REVERSE" == "1" && -x "$ADB_BIN" ]]; then
  print_step "第 3 步：移除 ADB 端口转发"
  "$ADB_BIN" reverse --remove tcp:9001 >/dev/null 2>&1 || true
  echo "[完成] 已尝试移除 adb reverse tcp:9001"
fi

print_step "第 4 步：检查剩余进程"
remaining=0
for pattern in "${PATTERNS[@]}"; do
  if pgrep -af "$pattern" >/dev/null 2>&1; then
    remaining=1
    show_matches "$pattern"
  fi
done

if [[ "$remaining" == "0" ]]; then
  echo "[成功] 数采相关进程已全部停止。"
else
  echo "[提示] 仍有残留进程，请根据上面输出继续手动处理。"
fi
