#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULE_SRC="${SCRIPT_DIR}/99-dexhand.rules"
RULE_DST="/etc/udev/rules.d/99-dexhand.rules"

if [[ ! -f "${RULE_SRC}" ]]; then
  echo "Rule file not found: ${RULE_SRC}"
  exit 1
fi

echo "Installing udev rule to ${RULE_DST}"
sudo cp "${RULE_SRC}" "${RULE_DST}"
sudo udevadm control --reload-rules
sudo udevadm trigger /dev/ttyUSB0 || true
sudo udevadm trigger /dev/ttyUSB1 || true

echo "Done."
echo "Check results with:"
echo "  ls -l /dev/dexhand_left /dev/dexhand_right"
