// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'hand_pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__deeptouch_interface__msg__TeleOptCmd __attribute__((deprecated))
#else
# define DEPRECATED__deeptouch_interface__msg__TeleOptCmd __declspec(deprecated)
#endif

namespace deeptouch_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TeleOptCmd_
{
  using Type = TeleOptCmd_<ContainerAllocator>;

  explicit TeleOptCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : hand_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_follow = false;
      this->is_calibrate_start_pose = false;
      this->is_absolute_pose = false;
      this->is_initial_pose = false;
      this->gripper_cmd = false;
      this->record_state = "";
      this->scale = 0.0f;
      this->primary_thumb = 0;
      this->rating = 0;
    }
  }

  explicit TeleOptCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : hand_pose(_alloc, _init),
    record_state(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_follow = false;
      this->is_calibrate_start_pose = false;
      this->is_absolute_pose = false;
      this->is_initial_pose = false;
      this->gripper_cmd = false;
      this->record_state = "";
      this->scale = 0.0f;
      this->primary_thumb = 0;
      this->rating = 0;
    }
  }

  // field types and members
  using _is_follow_type =
    bool;
  _is_follow_type is_follow;
  using _is_calibrate_start_pose_type =
    bool;
  _is_calibrate_start_pose_type is_calibrate_start_pose;
  using _is_absolute_pose_type =
    bool;
  _is_absolute_pose_type is_absolute_pose;
  using _is_initial_pose_type =
    bool;
  _is_initial_pose_type is_initial_pose;
  using _hand_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _hand_pose_type hand_pose;
  using _gripper_cmd_type =
    bool;
  _gripper_cmd_type gripper_cmd;
  using _record_state_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _record_state_type record_state;
  using _scale_type =
    float;
  _scale_type scale;
  using _primary_thumb_type =
    uint8_t;
  _primary_thumb_type primary_thumb;
  using _rating_type =
    uint8_t;
  _rating_type rating;

  // setters for named parameter idiom
  Type & set__is_follow(
    const bool & _arg)
  {
    this->is_follow = _arg;
    return *this;
  }
  Type & set__is_calibrate_start_pose(
    const bool & _arg)
  {
    this->is_calibrate_start_pose = _arg;
    return *this;
  }
  Type & set__is_absolute_pose(
    const bool & _arg)
  {
    this->is_absolute_pose = _arg;
    return *this;
  }
  Type & set__is_initial_pose(
    const bool & _arg)
  {
    this->is_initial_pose = _arg;
    return *this;
  }
  Type & set__hand_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->hand_pose = _arg;
    return *this;
  }
  Type & set__gripper_cmd(
    const bool & _arg)
  {
    this->gripper_cmd = _arg;
    return *this;
  }
  Type & set__record_state(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->record_state = _arg;
    return *this;
  }
  Type & set__scale(
    const float & _arg)
  {
    this->scale = _arg;
    return *this;
  }
  Type & set__primary_thumb(
    const uint8_t & _arg)
  {
    this->primary_thumb = _arg;
    return *this;
  }
  Type & set__rating(
    const uint8_t & _arg)
  {
    this->rating = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__deeptouch_interface__msg__TeleOptCmd
    std::shared_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__deeptouch_interface__msg__TeleOptCmd
    std::shared_ptr<deeptouch_interface::msg::TeleOptCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TeleOptCmd_ & other) const
  {
    if (this->is_follow != other.is_follow) {
      return false;
    }
    if (this->is_calibrate_start_pose != other.is_calibrate_start_pose) {
      return false;
    }
    if (this->is_absolute_pose != other.is_absolute_pose) {
      return false;
    }
    if (this->is_initial_pose != other.is_initial_pose) {
      return false;
    }
    if (this->hand_pose != other.hand_pose) {
      return false;
    }
    if (this->gripper_cmd != other.gripper_cmd) {
      return false;
    }
    if (this->record_state != other.record_state) {
      return false;
    }
    if (this->scale != other.scale) {
      return false;
    }
    if (this->primary_thumb != other.primary_thumb) {
      return false;
    }
    if (this->rating != other.rating) {
      return false;
    }
    return true;
  }
  bool operator!=(const TeleOptCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TeleOptCmd_

// alias to use template instance with default allocator
using TeleOptCmd =
  deeptouch_interface::msg::TeleOptCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_CMD__STRUCT_HPP_
