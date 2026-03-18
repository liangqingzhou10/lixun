// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from deeptouch_interface:msg/TeleOptDevice.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__TRAITS_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "deeptouch_interface/msg/detail/tele_opt_device__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'hand_touch'
#include "deeptouch_interface/msg/detail/hand_touch__traits.hpp"
// Member 'hand_pose'
// Member 'head_pose'
#include "geometry_msgs/msg/detail/pose__traits.hpp"

namespace deeptouch_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const TeleOptDevice & msg,
  std::ostream & out)
{
  out << "{";
  // member: timestamp
  {
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << ", ";
  }

  // member: frame_id
  {
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << ", ";
  }

  // member: hand_touch
  {
    out << "hand_touch: ";
    to_flow_style_yaml(msg.hand_touch, out);
    out << ", ";
  }

  // member: hand_pose
  {
    out << "hand_pose: ";
    to_flow_style_yaml(msg.hand_pose, out);
    out << ", ";
  }

  // member: head_pose
  {
    out << "head_pose: ";
    to_flow_style_yaml(msg.head_pose, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TeleOptDevice & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: timestamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "timestamp: ";
    rosidl_generator_traits::value_to_yaml(msg.timestamp, out);
    out << "\n";
  }

  // member: frame_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "frame_id: ";
    rosidl_generator_traits::value_to_yaml(msg.frame_id, out);
    out << "\n";
  }

  // member: hand_touch
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_touch:\n";
    to_block_style_yaml(msg.hand_touch, out, indentation + 2);
  }

  // member: hand_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_pose:\n";
    to_block_style_yaml(msg.hand_pose, out, indentation + 2);
  }

  // member: head_pose
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "head_pose:\n";
    to_block_style_yaml(msg.head_pose, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TeleOptDevice & msg, bool use_flow_style = false)
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
  const deeptouch_interface::msg::TeleOptDevice & msg,
  std::ostream & out, size_t indentation = 0)
{
  deeptouch_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use deeptouch_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const deeptouch_interface::msg::TeleOptDevice & msg)
{
  return deeptouch_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<deeptouch_interface::msg::TeleOptDevice>()
{
  return "deeptouch_interface::msg::TeleOptDevice";
}

template<>
inline const char * name<deeptouch_interface::msg::TeleOptDevice>()
{
  return "deeptouch_interface/msg/TeleOptDevice";
}

template<>
struct has_fixed_size<deeptouch_interface::msg::TeleOptDevice>
  : std::integral_constant<bool, has_fixed_size<deeptouch_interface::msg::HandTouch>::value && has_fixed_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct has_bounded_size<deeptouch_interface::msg::TeleOptDevice>
  : std::integral_constant<bool, has_bounded_size<deeptouch_interface::msg::HandTouch>::value && has_bounded_size<geometry_msgs::msg::Pose>::value> {};

template<>
struct is_message<deeptouch_interface::msg::TeleOptDevice>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__TRAITS_HPP_
