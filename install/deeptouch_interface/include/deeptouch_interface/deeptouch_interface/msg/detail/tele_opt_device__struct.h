// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from deeptouch_interface:msg/TeleOptDevice.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_H_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'hand_touch'
#include "deeptouch_interface/msg/detail/hand_touch__struct.h"
// Member 'hand_pose'
// Member 'head_pose'
#include "geometry_msgs/msg/detail/pose__struct.h"

/// Struct defined in msg/TeleOptDevice in the package deeptouch_interface.
/**
  * VR完整数据帧消息定义
  * deeptouch_interface/TeleOptDevice.msg
 */
typedef struct deeptouch_interface__msg__TeleOptDevice
{
  /// 时间戳
  float timestamp;
  /// 帧序号
  uint32_t frame_id;
  /// 手柄状态
  deeptouch_interface__msg__HandTouch hand_touch;
  /// 设备位姿
  geometry_msgs__msg__Pose hand_pose;
  /// 头部位姿
  geometry_msgs__msg__Pose head_pose;
} deeptouch_interface__msg__TeleOptDevice;

// Struct for a sequence of deeptouch_interface__msg__TeleOptDevice.
typedef struct deeptouch_interface__msg__TeleOptDevice__Sequence
{
  deeptouch_interface__msg__TeleOptDevice * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} deeptouch_interface__msg__TeleOptDevice__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_H_
