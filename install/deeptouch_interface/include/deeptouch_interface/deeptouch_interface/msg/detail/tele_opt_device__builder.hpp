// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from deeptouch_interface:msg/TeleOptDevice.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__BUILDER_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "deeptouch_interface/msg/detail/tele_opt_device__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace deeptouch_interface
{

namespace msg
{

namespace builder
{

class Init_TeleOptDevice_head_pose
{
public:
  explicit Init_TeleOptDevice_head_pose(::deeptouch_interface::msg::TeleOptDevice & msg)
  : msg_(msg)
  {}
  ::deeptouch_interface::msg::TeleOptDevice head_pose(::deeptouch_interface::msg::TeleOptDevice::_head_pose_type arg)
  {
    msg_.head_pose = std::move(arg);
    return std::move(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptDevice msg_;
};

class Init_TeleOptDevice_hand_pose
{
public:
  explicit Init_TeleOptDevice_hand_pose(::deeptouch_interface::msg::TeleOptDevice & msg)
  : msg_(msg)
  {}
  Init_TeleOptDevice_head_pose hand_pose(::deeptouch_interface::msg::TeleOptDevice::_hand_pose_type arg)
  {
    msg_.hand_pose = std::move(arg);
    return Init_TeleOptDevice_head_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptDevice msg_;
};

class Init_TeleOptDevice_hand_touch
{
public:
  explicit Init_TeleOptDevice_hand_touch(::deeptouch_interface::msg::TeleOptDevice & msg)
  : msg_(msg)
  {}
  Init_TeleOptDevice_hand_pose hand_touch(::deeptouch_interface::msg::TeleOptDevice::_hand_touch_type arg)
  {
    msg_.hand_touch = std::move(arg);
    return Init_TeleOptDevice_hand_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptDevice msg_;
};

class Init_TeleOptDevice_frame_id
{
public:
  explicit Init_TeleOptDevice_frame_id(::deeptouch_interface::msg::TeleOptDevice & msg)
  : msg_(msg)
  {}
  Init_TeleOptDevice_hand_touch frame_id(::deeptouch_interface::msg::TeleOptDevice::_frame_id_type arg)
  {
    msg_.frame_id = std::move(arg);
    return Init_TeleOptDevice_hand_touch(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptDevice msg_;
};

class Init_TeleOptDevice_timestamp
{
public:
  Init_TeleOptDevice_timestamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TeleOptDevice_frame_id timestamp(::deeptouch_interface::msg::TeleOptDevice::_timestamp_type arg)
  {
    msg_.timestamp = std::move(arg);
    return Init_TeleOptDevice_frame_id(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptDevice msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::deeptouch_interface::msg::TeleOptDevice>()
{
  return deeptouch_interface::msg::builder::Init_TeleOptDevice_timestamp();
}

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__BUILDER_HPP_
