// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_H_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/HandTouch in the package deeptouch_interface.
/**
  * 手柄状态消息定义
  * deeptouch_interface/HandTouch.msg
 */
typedef struct deeptouch_interface__msg__HandTouch
{
  /// 按键状态 (0或1)
  /// 左手：X按钮，右手：A按钮
  uint8_t one;
  /// 左手：Y按钮，右手：B按钮
  uint8_t two;
  /// 预留按键3
  uint8_t three;
  /// 预留按键4
  uint8_t four;
  /// Menu按钮
  uint8_t menu;
  /// 摇杆按下
  uint8_t primary_thumb;
  /// 模拟量输入 (0.0-1.0)
  /// 握持扳机值
  float hand_trigger;
  /// 食指扳机值
  float index_trigger;
  /// 摇杆输入 (-1.0到1.0)
  /// 摇杆X轴值
  float thumbstick_x;
  /// 摇杆Y轴值
  float thumbstick_y;
} deeptouch_interface__msg__HandTouch;

// Struct for a sequence of deeptouch_interface__msg__HandTouch.
typedef struct deeptouch_interface__msg__HandTouch__Sequence
{
  deeptouch_interface__msg__HandTouch * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} deeptouch_interface__msg__HandTouch__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_H_
