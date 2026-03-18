// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__BUILDER_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace deeptouch_interface
{

namespace msg
{

namespace builder
{

class Init_TeleOptCmd_rating
{
public:
  explicit Init_TeleOptCmd_rating(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  ::deeptouch_interface::msg::TeleOptCmd rating(::deeptouch_interface::msg::TeleOptCmd::_rating_type arg)
  {
    msg_.rating = std::move(arg);
    return std::move(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_primary_thumb
{
public:
  explicit Init_TeleOptCmd_primary_thumb(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_rating primary_thumb(::deeptouch_interface::msg::TeleOptCmd::_primary_thumb_type arg)
  {
    msg_.primary_thumb = std::move(arg);
    return Init_TeleOptCmd_rating(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_scale
{
public:
  explicit Init_TeleOptCmd_scale(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_primary_thumb scale(::deeptouch_interface::msg::TeleOptCmd::_scale_type arg)
  {
    msg_.scale = std::move(arg);
    return Init_TeleOptCmd_primary_thumb(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_record_state
{
public:
  explicit Init_TeleOptCmd_record_state(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_scale record_state(::deeptouch_interface::msg::TeleOptCmd::_record_state_type arg)
  {
    msg_.record_state = std::move(arg);
    return Init_TeleOptCmd_scale(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_gripper_cmd
{
public:
  explicit Init_TeleOptCmd_gripper_cmd(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_record_state gripper_cmd(::deeptouch_interface::msg::TeleOptCmd::_gripper_cmd_type arg)
  {
    msg_.gripper_cmd = std::move(arg);
    return Init_TeleOptCmd_record_state(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_hand_pose
{
public:
  explicit Init_TeleOptCmd_hand_pose(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_gripper_cmd hand_pose(::deeptouch_interface::msg::TeleOptCmd::_hand_pose_type arg)
  {
    msg_.hand_pose = std::move(arg);
    return Init_TeleOptCmd_gripper_cmd(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_is_initial_pose
{
public:
  explicit Init_TeleOptCmd_is_initial_pose(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_hand_pose is_initial_pose(::deeptouch_interface::msg::TeleOptCmd::_is_initial_pose_type arg)
  {
    msg_.is_initial_pose = std::move(arg);
    return Init_TeleOptCmd_hand_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_is_absolute_pose
{
public:
  explicit Init_TeleOptCmd_is_absolute_pose(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_is_initial_pose is_absolute_pose(::deeptouch_interface::msg::TeleOptCmd::_is_absolute_pose_type arg)
  {
    msg_.is_absolute_pose = std::move(arg);
    return Init_TeleOptCmd_is_initial_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_is_calibrate_start_pose
{
public:
  explicit Init_TeleOptCmd_is_calibrate_start_pose(::deeptouch_interface::msg::TeleOptCmd & msg)
  : msg_(msg)
  {}
  Init_TeleOptCmd_is_absolute_pose is_calibrate_start_pose(::deeptouch_interface::msg::TeleOptCmd::_is_calibrate_start_pose_type arg)
  {
    msg_.is_calibrate_start_pose = std::move(arg);
    return Init_TeleOptCmd_is_absolute_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

class Init_TeleOptCmd_is_follow
{
public:
  Init_TeleOptCmd_is_follow()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TeleOptCmd_is_calibrate_start_pose is_follow(::deeptouch_interface::msg::TeleOptCmd::_is_follow_type arg)
  {
    msg_.is_follow = std::move(arg);
    return Init_TeleOptCmd_is_calibrate_start_pose(msg_);
  }

private:
  ::deeptouch_interface::msg::TeleOptCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::deeptouch_interface::msg::TeleOptCmd>()
{
  return deeptouch_interface::msg::builder::Init_TeleOptCmd_is_follow();
}

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__BUILDER_HPP_
