// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/tele_opt_cmd__rosidl_typesupport_fastrtps_cpp.hpp"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.hpp"

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
namespace geometry_msgs
{
namespace msg
{
namespace typesupport_fastrtps_cpp
{
bool cdr_serialize(
  const geometry_msgs::msg::Pose &,
  eprosima::fastcdr::Cdr &);
bool cdr_deserialize(
  eprosima::fastcdr::Cdr &,
  geometry_msgs::msg::Pose &);
size_t get_serialized_size(
  const geometry_msgs::msg::Pose &,
  size_t current_alignment);
size_t
max_serialized_size_Pose(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);
}  // namespace typesupport_fastrtps_cpp
}  // namespace msg
}  // namespace geometry_msgs


namespace deeptouch_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
cdr_serialize(
  const deeptouch_interface::msg::TeleOptCmd & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: is_follow
  cdr << (ros_message.is_follow ? true : false);
  // Member: is_calibrate_start_pose
  cdr << (ros_message.is_calibrate_start_pose ? true : false);
  // Member: is_absolute_pose
  cdr << (ros_message.is_absolute_pose ? true : false);
  // Member: is_initial_pose
  cdr << (ros_message.is_initial_pose ? true : false);
  // Member: hand_pose
  geometry_msgs::msg::typesupport_fastrtps_cpp::cdr_serialize(
    ros_message.hand_pose,
    cdr);
  // Member: gripper_cmd
  cdr << (ros_message.gripper_cmd ? true : false);
  // Member: record_state
  cdr << ros_message.record_state;
  // Member: scale
  cdr << ros_message.scale;
  // Member: primary_thumb
  cdr << ros_message.primary_thumb;
  // Member: rating
  cdr << ros_message.rating;
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  deeptouch_interface::msg::TeleOptCmd & ros_message)
{
  // Member: is_follow
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.is_follow = tmp ? true : false;
  }

  // Member: is_calibrate_start_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.is_calibrate_start_pose = tmp ? true : false;
  }

  // Member: is_absolute_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.is_absolute_pose = tmp ? true : false;
  }

  // Member: is_initial_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.is_initial_pose = tmp ? true : false;
  }

  // Member: hand_pose
  geometry_msgs::msg::typesupport_fastrtps_cpp::cdr_deserialize(
    cdr, ros_message.hand_pose);

  // Member: gripper_cmd
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.gripper_cmd = tmp ? true : false;
  }

  // Member: record_state
  cdr >> ros_message.record_state;

  // Member: scale
  cdr >> ros_message.scale;

  // Member: primary_thumb
  cdr >> ros_message.primary_thumb;

  // Member: rating
  cdr >> ros_message.rating;

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
get_serialized_size(
  const deeptouch_interface::msg::TeleOptCmd & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: is_follow
  {
    size_t item_size = sizeof(ros_message.is_follow);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: is_calibrate_start_pose
  {
    size_t item_size = sizeof(ros_message.is_calibrate_start_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: is_absolute_pose
  {
    size_t item_size = sizeof(ros_message.is_absolute_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: is_initial_pose
  {
    size_t item_size = sizeof(ros_message.is_initial_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: hand_pose

  current_alignment +=
    geometry_msgs::msg::typesupport_fastrtps_cpp::get_serialized_size(
    ros_message.hand_pose, current_alignment);
  // Member: gripper_cmd
  {
    size_t item_size = sizeof(ros_message.gripper_cmd);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: record_state
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message.record_state.size() + 1);
  // Member: scale
  {
    size_t item_size = sizeof(ros_message.scale);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: primary_thumb
  {
    size_t item_size = sizeof(ros_message.primary_thumb);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: rating
  {
    size_t item_size = sizeof(ros_message.rating);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_deeptouch_interface
max_serialized_size_TeleOptCmd(
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


  // Member: is_follow
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: is_calibrate_start_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: is_absolute_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: is_initial_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: hand_pose
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size =
        geometry_msgs::msg::typesupport_fastrtps_cpp::max_serialized_size_Pose(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Member: gripper_cmd
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: record_state
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  // Member: scale
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: primary_thumb
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: rating
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = deeptouch_interface::msg::TeleOptCmd;
    is_plain =
      (
      offsetof(DataType, rating) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _TeleOptCmd__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const deeptouch_interface::msg::TeleOptCmd *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _TeleOptCmd__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<deeptouch_interface::msg::TeleOptCmd *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _TeleOptCmd__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const deeptouch_interface::msg::TeleOptCmd *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _TeleOptCmd__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_TeleOptCmd(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _TeleOptCmd__callbacks = {
  "deeptouch_interface::msg",
  "TeleOptCmd",
  _TeleOptCmd__cdr_serialize,
  _TeleOptCmd__cdr_deserialize,
  _TeleOptCmd__get_serialized_size,
  _TeleOptCmd__max_serialized_size
};

static rosidl_message_type_support_t _TeleOptCmd__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_TeleOptCmd__callbacks,
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
get_message_type_support_handle<deeptouch_interface::msg::TeleOptCmd>()
{
  return &deeptouch_interface::msg::typesupport_fastrtps_cpp::_TeleOptCmd__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, deeptouch_interface, msg, TeleOptCmd)() {
  return &deeptouch_interface::msg::typesupport_fastrtps_cpp::_TeleOptCmd__handle;
}

#ifdef __cplusplus
}
#endif
