// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/tele_opt_cmd__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "deeptouch_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.h"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__functions.h"
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

#include "geometry_msgs/msg/detail/pose__functions.h"  // hand_pose
#include "rosidl_runtime_c/string.h"  // record_state
#include "rosidl_runtime_c/string_functions.h"  // record_state

// forward declare type support functions
ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_deeptouch_interface
size_t get_serialized_size_geometry_msgs__msg__Pose(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_deeptouch_interface
size_t max_serialized_size_geometry_msgs__msg__Pose(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_IMPORT_deeptouch_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Pose)();


using _TeleOptCmd__ros_msg_type = deeptouch_interface__msg__TeleOptCmd;

static bool _TeleOptCmd__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _TeleOptCmd__ros_msg_type * ros_message = static_cast<const _TeleOptCmd__ros_msg_type *>(untyped_ros_message);
  // Field name: is_follow
  {
    cdr << (ros_message->is_follow ? true : false);
  }

  // Field name: is_calibrate_start_pose
  {
    cdr << (ros_message->is_calibrate_start_pose ? true : false);
  }

  // Field name: is_absolute_pose
  {
    cdr << (ros_message->is_absolute_pose ? true : false);
  }

  // Field name: is_initial_pose
  {
    cdr << (ros_message->is_initial_pose ? true : false);
  }

  // Field name: hand_pose
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Pose
      )()->data);
    if (!callbacks->cdr_serialize(
        &ros_message->hand_pose, cdr))
    {
      return false;
    }
  }

  // Field name: gripper_cmd
  {
    cdr << (ros_message->gripper_cmd ? true : false);
  }

  // Field name: record_state
  {
    const rosidl_runtime_c__String * str = &ros_message->record_state;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: scale
  {
    cdr << ros_message->scale;
  }

  // Field name: primary_thumb
  {
    cdr << ros_message->primary_thumb;
  }

  // Field name: rating
  {
    cdr << ros_message->rating;
  }

  return true;
}

static bool _TeleOptCmd__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _TeleOptCmd__ros_msg_type * ros_message = static_cast<_TeleOptCmd__ros_msg_type *>(untyped_ros_message);
  // Field name: is_follow
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_follow = tmp ? true : false;
  }

  // Field name: is_calibrate_start_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_calibrate_start_pose = tmp ? true : false;
  }

  // Field name: is_absolute_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_absolute_pose = tmp ? true : false;
  }

  // Field name: is_initial_pose
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->is_initial_pose = tmp ? true : false;
  }

  // Field name: hand_pose
  {
    const message_type_support_callbacks_t * callbacks =
      static_cast<const message_type_support_callbacks_t *>(
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
        rosidl_typesupport_fastrtps_c, geometry_msgs, msg, Pose
      )()->data);
    if (!callbacks->cdr_deserialize(
        cdr, &ros_message->hand_pose))
    {
      return false;
    }
  }

  // Field name: gripper_cmd
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->gripper_cmd = tmp ? true : false;
  }

  // Field name: record_state
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->record_state.data) {
      rosidl_runtime_c__String__init(&ros_message->record_state);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->record_state,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'record_state'\n");
      return false;
    }
  }

  // Field name: scale
  {
    cdr >> ros_message->scale;
  }

  // Field name: primary_thumb
  {
    cdr >> ros_message->primary_thumb;
  }

  // Field name: rating
  {
    cdr >> ros_message->rating;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_deeptouch_interface
size_t get_serialized_size_deeptouch_interface__msg__TeleOptCmd(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _TeleOptCmd__ros_msg_type * ros_message = static_cast<const _TeleOptCmd__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name is_follow
  {
    size_t item_size = sizeof(ros_message->is_follow);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_calibrate_start_pose
  {
    size_t item_size = sizeof(ros_message->is_calibrate_start_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_absolute_pose
  {
    size_t item_size = sizeof(ros_message->is_absolute_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name is_initial_pose
  {
    size_t item_size = sizeof(ros_message->is_initial_pose);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name hand_pose

  current_alignment += get_serialized_size_geometry_msgs__msg__Pose(
    &(ros_message->hand_pose), current_alignment);
  // field.name gripper_cmd
  {
    size_t item_size = sizeof(ros_message->gripper_cmd);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name record_state
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->record_state.size + 1);
  // field.name scale
  {
    size_t item_size = sizeof(ros_message->scale);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name primary_thumb
  {
    size_t item_size = sizeof(ros_message->primary_thumb);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name rating
  {
    size_t item_size = sizeof(ros_message->rating);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _TeleOptCmd__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_deeptouch_interface__msg__TeleOptCmd(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_deeptouch_interface
size_t max_serialized_size_deeptouch_interface__msg__TeleOptCmd(
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

  // member: is_follow
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_calibrate_start_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_absolute_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: is_initial_pose
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: hand_pose
  {
    size_t array_size = 1;


    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_geometry_msgs__msg__Pose(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }
  // member: gripper_cmd
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: record_state
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
  // member: scale
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: primary_thumb
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: rating
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
    using DataType = deeptouch_interface__msg__TeleOptCmd;
    is_plain =
      (
      offsetof(DataType, rating) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _TeleOptCmd__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_deeptouch_interface__msg__TeleOptCmd(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_TeleOptCmd = {
  "deeptouch_interface::msg",
  "TeleOptCmd",
  _TeleOptCmd__cdr_serialize,
  _TeleOptCmd__cdr_deserialize,
  _TeleOptCmd__get_serialized_size,
  _TeleOptCmd__max_serialized_size
};

static rosidl_message_type_support_t _TeleOptCmd__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_TeleOptCmd,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, deeptouch_interface, msg, TeleOptCmd)() {
  return &_TeleOptCmd__type_support;
}

#if defined(__cplusplus)
}
#endif
