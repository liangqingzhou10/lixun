// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/hand_touch__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "deeptouch_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "deeptouch_interface/msg/detail/hand_touch__struct.h"
#include "deeptouch_interface/msg/detail/hand_touch__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _HandTouch__ros_msg_type = deeptouch_interface__msg__HandTouch;

static bool _HandTouch__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _HandTouch__ros_msg_type * ros_message = static_cast<const _HandTouch__ros_msg_type *>(untyped_ros_message);
  // Field name: one
  {
    cdr << ros_message->one;
  }

  // Field name: two
  {
    cdr << ros_message->two;
  }

  // Field name: three
  {
    cdr << ros_message->three;
  }

  // Field name: four
  {
    cdr << ros_message->four;
  }

  // Field name: menu
  {
    cdr << ros_message->menu;
  }

  // Field name: primary_thumb
  {
    cdr << ros_message->primary_thumb;
  }

  // Field name: hand_trigger
  {
    cdr << ros_message->hand_trigger;
  }

  // Field name: index_trigger
  {
    cdr << ros_message->index_trigger;
  }

  // Field name: thumbstick_x
  {
    cdr << ros_message->thumbstick_x;
  }

  // Field name: thumbstick_y
  {
    cdr << ros_message->thumbstick_y;
  }

  return true;
}

static bool _HandTouch__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _HandTouch__ros_msg_type * ros_message = static_cast<_HandTouch__ros_msg_type *>(untyped_ros_message);
  // Field name: one
  {
    cdr >> ros_message->one;
  }

  // Field name: two
  {
    cdr >> ros_message->two;
  }

  // Field name: three
  {
    cdr >> ros_message->three;
  }

  // Field name: four
  {
    cdr >> ros_message->four;
  }

  // Field name: menu
  {
    cdr >> ros_message->menu;
  }

  // Field name: primary_thumb
  {
    cdr >> ros_message->primary_thumb;
  }

  // Field name: hand_trigger
  {
    cdr >> ros_message->hand_trigger;
  }

  // Field name: index_trigger
  {
    cdr >> ros_message->index_trigger;
  }

  // Field name: thumbstick_x
  {
    cdr >> ros_message->thumbstick_x;
  }

  // Field name: thumbstick_y
  {
    cdr >> ros_message->thumbstick_y;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_deeptouch_interface
size_t get_serialized_size_deeptouch_interface__msg__HandTouch(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _HandTouch__ros_msg_type * ros_message = static_cast<const _HandTouch__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name one
  {
    size_t item_size = sizeof(ros_message->one);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name two
  {
    size_t item_size = sizeof(ros_message->two);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name three
  {
    size_t item_size = sizeof(ros_message->three);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name four
  {
    size_t item_size = sizeof(ros_message->four);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name menu
  {
    size_t item_size = sizeof(ros_message->menu);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name primary_thumb
  {
    size_t item_size = sizeof(ros_message->primary_thumb);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name hand_trigger
  {
    size_t item_size = sizeof(ros_message->hand_trigger);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name index_trigger
  {
    size_t item_size = sizeof(ros_message->index_trigger);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name thumbstick_x
  {
    size_t item_size = sizeof(ros_message->thumbstick_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name thumbstick_y
  {
    size_t item_size = sizeof(ros_message->thumbstick_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _HandTouch__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_deeptouch_interface__msg__HandTouch(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_deeptouch_interface
size_t max_serialized_size_deeptouch_interface__msg__HandTouch(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: one
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: two
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: three
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: four
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: menu
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: primary_thumb
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: hand_trigger
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: index_trigger
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: thumbstick_x
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: thumbstick_y
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = deeptouch_interface__msg__HandTouch;
    is_plain =
      (
      offsetof(DataType, thumbstick_y) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _HandTouch__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_deeptouch_interface__msg__HandTouch(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_HandTouch = {
  "deeptouch_interface::msg",
  "HandTouch",
  _HandTouch__cdr_serialize,
  _HandTouch__cdr_deserialize,
  _HandTouch__get_serialized_size,
  _HandTouch__max_serialized_size
};

static rosidl_message_type_support_t _HandTouch__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_HandTouch,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, deeptouch_interface, msg, HandTouch)() {
  return &_HandTouch__type_support;
}

#if defined(__cplusplus)
}
#endif
