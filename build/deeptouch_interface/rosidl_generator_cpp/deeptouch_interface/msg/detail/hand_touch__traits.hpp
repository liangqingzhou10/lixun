// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__TRAITS_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "deeptouch_interface/msg/detail/hand_touch__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace deeptouch_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const HandTouch & msg,
  std::ostream & out)
{
  out << "{";
  // member: one
  {
    out << "one: ";
    rosidl_generator_traits::value_to_yaml(msg.one, out);
    out << ", ";
  }

  // member: two
  {
    out << "two: ";
    rosidl_generator_traits::value_to_yaml(msg.two, out);
    out << ", ";
  }

  // member: three
  {
    out << "three: ";
    rosidl_generator_traits::value_to_yaml(msg.three, out);
    out << ", ";
  }

  // member: four
  {
    out << "four: ";
    rosidl_generator_traits::value_to_yaml(msg.four, out);
    out << ", ";
  }

  // member: menu
  {
    out << "menu: ";
    rosidl_generator_traits::value_to_yaml(msg.menu, out);
    out << ", ";
  }

  // member: primary_thumb
  {
    out << "primary_thumb: ";
    rosidl_generator_traits::value_to_yaml(msg.primary_thumb, out);
    out << ", ";
  }

  // member: hand_trigger
  {
    out << "hand_trigger: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_trigger, out);
    out << ", ";
  }

  // member: index_trigger
  {
    out << "index_trigger: ";
    rosidl_generator_traits::value_to_yaml(msg.index_trigger, out);
    out << ", ";
  }

  // member: thumbstick_x
  {
    out << "thumbstick_x: ";
    rosidl_generator_traits::value_to_yaml(msg.thumbstick_x, out);
    out << ", ";
  }

  // member: thumbstick_y
  {
    out << "thumbstick_y: ";
    rosidl_generator_traits::value_to_yaml(msg.thumbstick_y, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const HandTouch & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: one
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "one: ";
    rosidl_generator_traits::value_to_yaml(msg.one, out);
    out << "\n";
  }

  // member: two
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "two: ";
    rosidl_generator_traits::value_to_yaml(msg.two, out);
    out << "\n";
  }

  // member: three
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "three: ";
    rosidl_generator_traits::value_to_yaml(msg.three, out);
    out << "\n";
  }

  // member: four
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "four: ";
    rosidl_generator_traits::value_to_yaml(msg.four, out);
    out << "\n";
  }

  // member: menu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "menu: ";
    rosidl_generator_traits::value_to_yaml(msg.menu, out);
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

  // member: hand_trigger
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hand_trigger: ";
    rosidl_generator_traits::value_to_yaml(msg.hand_trigger, out);
    out << "\n";
  }

  // member: index_trigger
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "index_trigger: ";
    rosidl_generator_traits::value_to_yaml(msg.index_trigger, out);
    out << "\n";
  }

  // member: thumbstick_x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "thumbstick_x: ";
    rosidl_generator_traits::value_to_yaml(msg.thumbstick_x, out);
    out << "\n";
  }

  // member: thumbstick_y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "thumbstick_y: ";
    rosidl_generator_traits::value_to_yaml(msg.thumbstick_y, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const HandTouch & msg, bool use_flow_style = false)
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
  const deeptouch_interface::msg::HandTouch & msg,
  std::ostream & out, size_t indentation = 0)
{
  deeptouch_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use deeptouch_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const deeptouch_interface::msg::HandTouch & msg)
{
  return deeptouch_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<deeptouch_interface::msg::HandTouch>()
{
  return "deeptouch_interface::msg::HandTouch";
}

template<>
inline const char * name<deeptouch_interface::msg::HandTouch>()
{
  return "deeptouch_interface/msg/HandTouch";
}

template<>
struct has_fixed_size<deeptouch_interface::msg::HandTouch>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<deeptouch_interface::msg::HandTouch>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<deeptouch_interface::msg::HandTouch>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__TRAITS_HPP_
