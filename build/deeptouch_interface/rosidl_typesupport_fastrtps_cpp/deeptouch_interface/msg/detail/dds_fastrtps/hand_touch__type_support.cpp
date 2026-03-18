// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/hand_touch__rosidl_typesupport_fastrtps_cpp.hpp"
#include "deeptouch_interface/msg/detail/hand_touch__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace deeptouch_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
cdr_serialize(
  const deeptouch_interface::msg::HandTouch & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: one
  cdr << ros_message.one;
  // Member: two
  cdr << ros_message.two;
  // Member: three
  cdr << ros_message.three;
  // Member: four
  cdr << ros_message.four;
  // Member: menu
  cdr << ros_message.menu;
  // Member: primary_thumb
  cdr << ros_message.primary_thumb;
  // Member: hand_trigger
  cdr << ros_message.hand_trigger;
  // Member: index_trigger
  cdr << ros_message.index_trigger;
  // Member: thumbstick_x
  cdr << ros_message.thumbstick_x;
  // Member: thumbstick_y
  cdr << ros_message.thumbstick_y;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  deeptouch_interface::msg::HandTouch & ros_message)
{
  // Member: one
  cdr >> ros_message.one;

  // Member: two
  cdr >> ros_message.two;

  // Member: three
  cdr >> ros_message.three;

  // Member: four
  cdr >> ros_message.four;

  // Member: menu
  cdr >> ros_message.menu;

  // Member: primary_thumb
  cdr >> ros_message.primary_thumb;

  // Member: hand_trigger
  cdr >> ros_message.hand_trigger;

  // Member: index_trigger
  cdr >> ros_message.index_trigger;

  // Member: thumbstick_x
  cdr >> ros_message.thumbstick_x;

  // Member: thumbstick_y
  cdr >> ros_message.thumbstick_y;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
get_serialized_size(
  const deeptouch_interface::msg::HandTouch & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: one
  {
    size_t item_size = sizeof(ros_message.one);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: two
  {
    size_t item_size = sizeof(ros_message.two);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: three
  {
    size_t item_size = sizeof(ros_message.three);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: four
  {
    size_t item_size = sizeof(ros_message.four);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: menu
  {
    size_t item_size = sizeof(ros_message.menu);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: primary_thumb
  {
    size_t item_size = sizeof(ros_message.primary_thumb);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: hand_trigger
  {
    size_t item_size = sizeof(ros_message.hand_trigger);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: index_trigger
  {
    size_t item_size = sizeof(ros_message.index_trigger);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: thumbstick_x
  {
    size_t item_size = sizeof(ros_message.thumbstick_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: thumbstick_y
  {
    size_t item_size = sizeof(ros_message.thumbstick_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
max_serialized_size_HandTouch(
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


  // Member: one
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: two
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: three
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: four
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: menu
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: primary_thumb
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: hand_trigger
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: index_trigger
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: thumbstick_x
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: thumbstick_y
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
    using DataType = deeptouch_interface::msg::HandTouch;
    is_plain =
      (
      offsetof(DataType, thumbstick_y) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _HandTouch__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const deeptouch_interface::msg::HandTouch *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _HandTouch__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<deeptouch_interface::msg::HandTouch *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _HandTouch__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const deeptouch_interface::msg::HandTouch *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _HandTouch__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_HandTouch(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _HandTouch__callbacks = {
  "deeptouch_interface::msg",
  "HandTouch",
  _HandTouch__cdr_serialize,
  _HandTouch__cdr_deserialize,
  _HandTouch__get_serialized_size,
  _HandTouch__max_serialized_size
};

static rosidl_message_type_support_t _HandTouch__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_HandTouch__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace deeptouch_interface

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_deeptouch_interface
const rosidl_message_type_support_t *
get_message_type_support_handle<deeptouch_interface::msg::HandTouch>()
{
  return &deeptouch_interface::msg::typesupport_fastrtps_cpp::_HandTouch__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, deeptouch_interface, msg, HandTouch)() {
  return &deeptouch_interface::msg::typesupport_fastrtps_cpp::_HandTouch__handle;
}

#ifdef __cplusplus
}
#endif
