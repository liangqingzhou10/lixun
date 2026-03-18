// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_H_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'hand_pose'
#include "geometry_msgs/msg/detail/pose__struct.h"
// Member 'record_state'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/TeleOptCmd in the package deeptouch_interface.
/**
  * 位姿数据消息定义
  * deeptouch_interface/TeleOptCmd.msg
 */
typedef struct deeptouch_interface__msg__TeleOptCmd
{
  /// 是否随动  true: 随动  false: 不随动
  bool is_follow;
  /// 是否校准起始位姿  true: 校准起始位姿  false: 不校准
  bool is_calibrate_start_pose;
  /// 是否绝对位姿  true: 绝对位姿  false: 相对位姿
  bool is_absolute_pose;
  /// 是否回到初始位置
  bool is_initial_pose;
  /// 手部位姿
  geometry_msgs__msg__Pose hand_pose;
  /// 夹爪指令
  ///  Gripper 0: open; 1: close
  bool gripper_cmd;
  /// 开始记录数据
  rosidl_runtime_c__String record_state;
  /// 尺度（手部位姿缩放）
  float scale;
  /// 摇杆按下
  uint8_t primary_thumb;
  /// 本次录制的评分（仅 HIL-SERL 使用）：
  ///  1 = 成功, 255 = 失败, 0 = 未标记
  uint8_t rating;
} deeptouch_interface__msg__TeleOptCmd;

// Struct for a sequence of deeptouch_interface__msg__TeleOptCmd.
typedef struct deeptouch_interface__msg__TeleOptCmd__Sequence
{
  deeptouch_interface__msg__TeleOptCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} deeptouch_interface__msg__TeleOptCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_H_
