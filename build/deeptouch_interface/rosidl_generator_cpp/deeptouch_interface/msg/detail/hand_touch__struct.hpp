// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice

#ifndef DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_HPP_
#define DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__deeptouch_interface__msg__HandTouch __attribute__((deprecated))
#else
# define DEPRECATED__deeptouch_interface__msg__HandTouch __declspec(deprecated)
#endif

namespace deeptouch_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HandTouch_
{
  using Type = HandTouch_<ContainerAllocator>;

  explicit HandTouch_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->one = 0;
      this->two = 0;
      this->three = 0;
      this->four = 0;
      this->menu = 0;
      this->primary_thumb = 0;
      this->hand_trigger = 0.0f;
      this->index_trigger = 0.0f;
      this->thumbstick_x = 0.0f;
      this->thumbstick_y = 0.0f;
    }
  }

  explicit HandTouch_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->one = 0;
      this->two = 0;
      this->three = 0;
      this->four = 0;
      this->menu = 0;
      this->primary_thumb = 0;
      this->hand_trigger = 0.0f;
      this->index_trigger = 0.0f;
      this->thumbstick_x = 0.0f;
      this->thumbstick_y = 0.0f;
    }
  }

  // field types and members
  using _one_type =
    uint8_t;
  _one_type one;
  using _two_type =
    uint8_t;
  _two_type two;
  using _three_type =
    uint8_t;
  _three_type three;
  using _four_type =
    uint8_t;
  _four_type four;
  using _menu_type =
    uint8_t;
  _menu_type menu;
  using _primary_thumb_type =
    uint8_t;
  _primary_thumb_type primary_thumb;
  using _hand_trigger_type =
    float;
  _hand_trigger_type hand_trigger;
  using _index_trigger_type =
    float;
  _index_trigger_type index_trigger;
  using _thumbstick_x_type =
    float;
  _thumbstick_x_type thumbstick_x;
  using _thumbstick_y_type =
    float;
  _thumbstick_y_type thumbstick_y;

  // setters for named parameter idiom
  Type & set__one(
    const uint8_t & _arg)
  {
    this->one = _arg;
    return *this;
  }
  Type & set__two(
    const uint8_t & _arg)
  {
    this->two = _arg;
    return *this;
  }
  Type & set__three(
    const uint8_t & _arg)
  {
    this->three = _arg;
    return *this;
  }
  Type & set__four(
    const uint8_t & _arg)
  {
    this->four = _arg;
    return *this;
  }
  Type & set__menu(
    const uint8_t & _arg)
  {
    this->menu = _arg;
    return *this;
  }
  Type & set__primary_thumb(
    const uint8_t & _arg)
  {
    this->primary_thumb = _arg;
    return *this;
  }
  Type & set__hand_trigger(
    const float & _arg)
  {
    this->hand_trigger = _arg;
    return *this;
  }
  Type & set__index_trigger(
    const float & _arg)
  {
    this->index_trigger = _arg;
    return *this;
  }
  Type & set__thumbstick_x(
    const float & _arg)
  {
    this->thumbstick_x = _arg;
    return *this;
  }
  Type & set__thumbstick_y(
    const float & _arg)
  {
    this->thumbstick_y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    deeptouch_interface::msg::HandTouch_<ContainerAllocator> *;
  using ConstRawPtr =
    const deeptouch_interface::msg::HandTouch_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::HandTouch_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      deeptouch_interface::msg::HandTouch_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__deeptouch_interface__msg__HandTouch
    std::shared_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__deeptouch_interface__msg__HandTouch
    std::shared_ptr<deeptouch_interface::msg::HandTouch_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HandTouch_ & other) const
  {
    if (this->one != other.one) {
      return false;
    }
    if (this->two != other.two) {
      return false;
    }
    if (this->three != other.three) {
      return false;
    }
    if (this->four != other.four) {
      return false;
    }
    if (this->menu != other.menu) {
      return false;
    }
    if (this->primary_thumb != other.primary_thumb) {
      return false;
    }
    if (this->hand_trigger != other.hand_trigger) {
      return false;
    }
    if (this->index_trigger != other.index_trigger) {
      return false;
    }
    if (this->thumbstick_x != other.thumbstick_x) {
      return false;
    }
    if (this->thumbstick_y != other.thumbstick_y) {
      return false;
    }
    return true;
  }
  bool operator!=(const HandTouch_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HandTouch_

// alias to use template instance with default allocator
using HandTouch =
  deeptouch_interface::msg::HandTouch_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace deeptouch_interface

#endif  // DEEPTOUCH_INTERFACE__MSG__DETAIL__HAND_TOUCH__STRUCT_HPP_
