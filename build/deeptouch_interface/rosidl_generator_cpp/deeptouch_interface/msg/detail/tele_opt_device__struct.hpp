// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from deeptouch_interface:msg/TeleOptDevice.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'hand_touch'
#include "deeptouch_interface/msg/detail/hand_touch__struct.hpp"
// Member 'hand_pose'
// Member 'head_pose'
#include "geometry_msgs/msg/detail/pose__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__deeptouch_interface__msg__TeleOptDevice __attribute__((deprecated))
#else
# define DEPRECATED__deeptouch_interface__msg__TeleOptDevice __declspec(deprecated)
#endif

namespace deeptouch_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TeleOptDevice_
{
  using Type = TeleOptDevice_<ContainerAllocator>;

  explicit TeleOptDevice_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : hand_touch(_init),
    hand_pose(_init),
    head_pose(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timestamp = 0.0f;
      this->frame_id = 0ul;
    }
  }

  explicit TeleOptDevice_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : hand_touch(_alloc, _init),
    hand_pose(_alloc, _init),
    head_pose(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->timestamp = 0.0f;
      this->frame_id = 0ul;
    }
  }

  // field types and members
  using _timestamp_type =
    float;
  _timestamp_type timestamp;
  using _frame_id_type =
    uint32_t;
  _frame_id_type frame_id;
  using _hand_touch_type =
    deeptouch_interface::msg::HandTouch_<ContainerAllocator>;
  _hand_touch_type hand_touch;
  using _hand_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _hand_pose_type hand_pose;
  using _head_pose_type =
    geometry_msgs::msg::Pose_<ContainerAllocator>;
  _head_pose_type head_pose;

  // setters for named parameter idiom
  Type & set__timestamp(
    const float & _arg)
  {
    this->timestamp = _arg;
    return *this;
  }
  Type & set__frame_id(
    const uint32_t & _arg)
  {
    this->frame_id = _arg;
    return *this;
  }
  Type & set__hand_touch(
    const deeptouch_interface::msg::HandTouch_<ContainerAllocator> & _arg)
  {
    this->hand_touch = _arg;
    return *this;
  }
  Type & set__hand_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->hand_pose = _arg;
    return *this;
  }
  Type & set__head_pose(
    const geometry_msgs::msg::Pose_<ContainerAllocator> & _arg)
  {
    this->head_pose = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> *;
  using ConstRawPtr =
    const deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__deeptouch_interface__msg__TeleOptDevice
    std::shared_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__deeptouch_interface__msg__TeleOptDevice
    std::shared_ptr<deeptouch_interface::msg::TeleOptDevice_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TeleOptDevice_ & other) const
  {
    if (this->timestamp != other.timestamp) {
      return false;
    }
    if (this->frame_id != other.frame_id) {
      return false;
    }
    if (this->hand_touch != other.hand_touch) {
      return false;
    }
    if (this->hand_pose != other.hand_pose) {
      return false;
    }
    if (this->head_pose != other.head_pose) {
      return false;
    }
    return true;
  }
  bool operator!=(const TeleOptDevice_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TeleOptDevice_

// alias to use template instance with default allocator
using TeleOptDevice =
  deeptouch_interface::msg::TeleOptDevice_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__TELE_OPT_DEVICE__STRUCT_HPP_
