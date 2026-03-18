// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__TRAITS_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'hand_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace deeptouch_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const TeleOptCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_follow
  {
    out << "is_follow: ";
    rosidl_generator_traits::value_to_yaml(msg.is_follow, out);
    out << ", ";
  }

  // member: is_calibrate_start_pose
  {
    out << "is_calibrate_start_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_calibrate_start_pose, out);
    out << ", ";
  }

  // member: is_absolute_pose
  {
    out << "is_absolute_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_absolute_pose, out);
    out << ", ";
  }

  // member: is_initial_pose
  {
    out << "is_initial_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_initial_pose, out);
    out << ", ";
  }

  // member: hand_pose
  {
    out << "hand_pose: ";
    to_flow_style_yaml(msg.hand_pose, out);
    out << ", ";
  }

  // member: gripper_cmd
  {
    out << "gripper_cmd: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_cmd, out);
    out << ", ";
  }

  // member: record_state
  {
    out << "record_state: ";
    rosidl_generator_traits::value_to_yaml(msg.record_state, out);
    out << ", ";
  }

  // member: scale
  {
    out << "scale: ";
    rosidl_generator_traits::value_to_yaml(msg.scale, out);
    out << ", ";
  }

  // member: primary_thumb
  {
    out << "primary_thumb: ";
    rosidl_generator_traits::value_to_yaml(msg.primary_thumb, out);
    out << ", ";
  }

  // member: rating
  {
    out << "rating: ";
    rosidl_generator_traits::value_to_yaml(msg.rating, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TeleOptCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_follow
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_follow: ";
    rosidl_generator_traits::value_to_yaml(msg.is_follow, out);
    out << "\n";
  }

  // member: is_calibrate_start_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_calibrate_start_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_calibrate_start_pose, out);
    out << "\n";
  }

  // member: is_absolute_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_absolute_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_absolute_pose, out);
    out << "\n";
  }

  // member: is_initial_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_initial_pose: ";
    rosidl_generator_traits::value_to_yaml(msg.is_initial_pose, out);
    out << "\n";
  }

  // member: hand_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_pose:\n";
    to_block_style_yaml(msg.hand_pose, out, indentation + 2);
  }

  // member: gripper_cmd
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "gripper_cmd: ";
    rosidl_generator_traits::value_to_yaml(msg.gripper_cmd, out);
    out << "\n";
  }

  // member: record_state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "record_state: ";
    rosidl_generator_traits::value_to_yaml(msg.record_state, out);
    out << "\n";
  }

  // member: scale
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "scale: ";
    rosidl_generator_traits::value_to_yaml(msg.scale, out);
    out << "\n";
  }

  // member: primary_thumb
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "primary_thumb: ";
    rosidl_generator_traits::value_to_yaml(msg.primary_thumb, out);
    out << "\n";
  }

  // member: rating
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rating: ";
    rosidl_generator_traits::value_to_yaml(msg.rating, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TeleOptCmd & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace deeptouch_interface

namespace rosidl_generator_traits
{

[[deprecated("use deeptouch_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const deeptouch_interface::msg::TeleOptCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  deeptouch_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use deeptouch_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const deeptouch_interface::msg::TeleOptCmd & msg)
{
  return deeptouch_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<deeptouch_interface::msg::TeleOptCmd>()
{
  return "deeptouch_interface::msg::TeleOptCmd";
}

template<>
inline const char * name<deeptouch_interface::msg::TeleOptCmd>()
{
  return "deeptouch_interface/msg/TeleOptCmd";
}

template<>
struct has_fixed_size<deeptouch_interface::msg::TeleOptCmd>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<deeptouch_interface::msg::TeleOptCmd>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<deeptouch_interface::msg::TeleOptCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__TRAITS_HPP_
