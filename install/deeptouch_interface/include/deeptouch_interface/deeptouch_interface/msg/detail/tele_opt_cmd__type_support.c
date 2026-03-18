// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "deeptouch_interface/msg/detail/tele_opt_cmd__rosidl_typesupport_introspection_c.h"
#include "deeptouch_interface/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__functions.h"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.h"


// Include directives for member types
// Member `hand_pose`
#include "geometry_msgs/msg/pose.h"
// Member `hand_pose`
#include "geometry_msgs/msg/detail/pose__rosidl_typesupport_introspection_c.h"
// Member `record_state`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  deeptouch_interface__msg__TeleOptCmd__init(message_memory);
}

void deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_fini_function(void * message_memory)
{
  deeptouch_interface__msg__TeleOptCmd__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_member_array[10] = {
  {
    "is_follow",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, is_follow),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_calibrate_start_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, is_calibrate_start_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_absolute_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, is_absolute_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "is_initial_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, is_initial_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "hand_pose",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, hand_pose),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "gripper_cmd",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, gripper_cmd),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "record_state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, record_state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "scale",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_FLOAT,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, scale),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "primary_thumb",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, primary_thumb),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "rating",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_UINT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(deeptouch_interface__msg__TeleOptCmd, rating),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_members = {
  "deeptouch_interface__msg",  // message namespace
  "TeleOptCmd",  // message name
  10,  // number of fields
  sizeof(deeptouch_interface__msg__TeleOptCmd),
  deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_member_array,  // message members
  deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_init_function,  // function to initialize message memory (memory has to be allocated)
  deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_type_support_handle = {
  0,
  &deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_deeptouch_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, deeptouch_interface, msg, TeleOptCmd)() {
  deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_member_array[4].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, geometry_msgs, msg, Pose)();
  if (!deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_type_support_handle.typesupport_identifier) {
    deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &deeptouch_interface__msg__TeleOptCmd__rosidl_typesupport_introspection_c__TeleOptCmd_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
