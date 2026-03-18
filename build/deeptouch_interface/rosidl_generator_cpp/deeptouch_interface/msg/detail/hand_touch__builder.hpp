// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__BUILDER_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "deeptouch_interface/msg/detail/hand_touch__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace deeptouch_interface
{

namespace msg
{

namespace builder
{

class Init_HandTouch_thumbstick_y
{
public:
  explicit Init_HandTouch_thumbstick_y(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  ::deeptouch_interface::msg::HandTouch thumbstick_y(::deeptouch_interface::msg::HandTouch::_thumbstick_y_type arg)
  {
    msg_.thumbstick_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_thumbstick_x
{
public:
  explicit Init_HandTouch_thumbstick_x(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_thumbstick_y thumbstick_x(::deeptouch_interface::msg::HandTouch::_thumbstick_x_type arg)
  {
    msg_.thumbstick_x = std::move(arg);
    return Init_HandTouch_thumbstick_y(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_index_trigger
{
public:
  explicit Init_HandTouch_index_trigger(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_thumbstick_x index_trigger(::deeptouch_interface::msg::HandTouch::_index_trigger_type arg)
  {
    msg_.index_trigger = std::move(arg);
    return Init_HandTouch_thumbstick_x(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_hand_trigger
{
public:
  explicit Init_HandTouch_hand_trigger(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_index_trigger hand_trigger(::deeptouch_interface::msg::HandTouch::_hand_trigger_type arg)
  {
    msg_.hand_trigger = std::move(arg);
    return Init_HandTouch_index_trigger(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_primary_thumb
{
public:
  explicit Init_HandTouch_primary_thumb(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_hand_trigger primary_thumb(::deeptouch_interface::msg::HandTouch::_primary_thumb_type arg)
  {
    msg_.primary_thumb = std::move(arg);
    return Init_HandTouch_hand_trigger(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_menu
{
public:
  explicit Init_HandTouch_menu(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_primary_thumb menu(::deeptouch_interface::msg::HandTouch::_menu_type arg)
  {
    msg_.menu = std::move(arg);
    return Init_HandTouch_primary_thumb(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_four
{
public:
  explicit Init_HandTouch_four(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_menu four(::deeptouch_interface::msg::HandTouch::_four_type arg)
  {
    msg_.four = std::move(arg);
    return Init_HandTouch_menu(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_three
{
public:
  explicit Init_HandTouch_three(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_four three(::deeptouch_interface::msg::HandTouch::_three_type arg)
  {
    msg_.three = std::move(arg);
    return Init_HandTouch_four(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_two
{
public:
  explicit Init_HandTouch_two(::deeptouch_interface::msg::HandTouch & msg)
  : msg_(msg)
  {}
  Init_HandTouch_three two(::deeptouch_interface::msg::HandTouch::_two_type arg)
  {
    msg_.two = std::move(arg);
    return Init_HandTouch_three(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

class Init_HandTouch_one
{
public:
  Init_HandTouch_one()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_HandTouch_two one(::deeptouch_interface::msg::HandTouch::_one_type arg)
  {
    msg_.one = std::move(arg);
    return Init_HandTouch_two(msg_);
  }

private:
  ::deeptouch_interface::msg::HandTouch msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::deeptouch_interface::msg::HandTouch>()
{
  return deeptouch_interface::msg::builder::Init_HandTouch_one();
}

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__BUILDER_HPP_
