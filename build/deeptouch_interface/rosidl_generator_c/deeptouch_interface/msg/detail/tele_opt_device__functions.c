// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from deeptouch_interface:msg/TeleOptDevice.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/tele_opt_device__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `hand_touch`
#include "deeptouch_interface/msg/detail/hand_touch__functions.h"
// Member `hand_pose`
// Member `head_pose`
#include "geometry_msgs/msg/detail/pose__functions.h"

bool
deeptouch_interface__msg__TeleOptDevice__init(deeptouch_interface__msg__TeleOptDevice * msg)
{
  if (!msg) {
    return false;
  }
  // timestamp
  // frame_id
  // hand_touch
  if (!deeptouch_interface__msg__HandTouch__init(&msg->hand_touch)) {
    deeptouch_interface__msg__TeleOptDevice__fini(msg);
    return false;
  }
  // hand_pose
  if (!geometry_msgs__msg__Pose__init(&msg->hand_pose)) {
    deeptouch_interface__msg__TeleOptDevice__fini(msg);
    return false;
  }
  // head_pose
  if (!geometry_msgs__msg__Pose__init(&msg->head_pose)) {
    deeptouch_interface__msg__TeleOptDevice__fini(msg);
    return false;
  }
  return true;
}

void
deeptouch_interface__msg__TeleOptDevice__fini(deeptouch_interface__msg__TeleOptDevice * msg)
{
  if (!msg) {
    return;
  }
  // timestamp
  // frame_id
  // hand_touch
  deeptouch_interface__msg__HandTouch__fini(&msg->hand_touch);
  // hand_pose
  geometry_msgs__msg__Pose__fini(&msg->hand_pose);
  // head_pose
  geometry_msgs__msg__Pose__fini(&msg->head_pose);
}

bool
deeptouch_interface__msg__TeleOptDevice__are_equal(const deeptouch_interface__msg__TeleOptDevice * lhs, const deeptouch_interface__msg__TeleOptDevice * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // timestamp
  if (lhs->timestamp != rhs->timestamp) {
    return false;
  }
  // frame_id
  if (lhs->frame_id != rhs->frame_id) {
    return false;
  }
  // hand_touch
  if (!deeptouch_interface__msg__HandTouch__are_equal(
      &(lhs->hand_touch), &(rhs->hand_touch)))
  {
    return false;
  }
  // hand_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->hand_pose), &(rhs->hand_pose)))
  {
    return false;
  }
  // head_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->head_pose), &(rhs->head_pose)))
  {
    return false;
  }
  return true;
}

bool
deeptouch_interface__msg__TeleOptDevice__copy(
  const deeptouch_interface__msg__TeleOptDevice * input,
  deeptouch_interface__msg__TeleOptDevice * output)
{
  if (!input || !output) {
    return false;
  }
  // timestamp
  output->timestamp = input->timestamp;
  // frame_id
  output->frame_id = input->frame_id;
  // hand_touch
  if (!deeptouch_interface__msg__HandTouch__copy(
      &(input->hand_touch), &(output->hand_touch)))
  {
    return false;
  }
  // hand_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->hand_pose), &(output->hand_pose)))
  {
    return false;
  }
  // head_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->head_pose), &(output->head_pose)))
  {
    return false;
  }
  return true;
}

deeptouch_interface__msg__TeleOptDevice *
deeptouch_interface__msg__TeleOptDevice__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptDevice * msg = (deeptouch_interface__msg__TeleOptDevice *)allocator.allocate(sizeof(deeptouch_interface__msg__TeleOptDevice), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(deeptouch_interface__msg__TeleOptDevice));
  bool success = deeptouch_interface__msg__TeleOptDevice__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
deeptouch_interface__msg__TeleOptDevice__destroy(deeptouch_interface__msg__TeleOptDevice * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    deeptouch_interface__msg__TeleOptDevice__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
deeptouch_interface__msg__TeleOptDevice__Sequence__init(deeptouch_interface__msg__TeleOptDevice__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptDevice * data = NULL;

  if (size) {
    data = (deeptouch_interface__msg__TeleOptDevice *)allocator.zero_allocate(size, sizeof(deeptouch_interface__msg__TeleOptDevice), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = deeptouch_interface__msg__TeleOptDevice__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        deeptouch_interface__msg__TeleOptDevice__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
deeptouch_interface__msg__TeleOptDevice__Sequence__fini(deeptouch_interface__msg__TeleOptDevice__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      deeptouch_interface__msg__TeleOptDevice__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

deeptouch_interface__msg__TeleOptDevice__Sequence *
deeptouch_interface__msg__TeleOptDevice__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptDevice__Sequence * array = (deeptouch_interface__msg__TeleOptDevice__Sequence *)allocator.allocate(sizeof(deeptouch_interface__msg__TeleOptDevice__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = deeptouch_interface__msg__TeleOptDevice__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
deeptouch_interface__msg__TeleOptDevice__Sequence__destroy(deeptouch_interface__msg__TeleOptDevice__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    deeptouch_interface__msg__TeleOptDevice__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
deeptouch_interface__msg__TeleOptDevice__Sequence__are_equal(const deeptouch_interface__msg__TeleOptDevice__Sequence * lhs, const deeptouch_interface__msg__TeleOptDevice__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!deeptouch_interface__msg__TeleOptDevice__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
deeptouch_interface__msg__TeleOptDevice__Sequence__copy(
  const deeptouch_interface__msg__TeleOptDevice__Sequence * input,
  deeptouch_interface__msg__TeleOptDevice__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(deeptouch_interface__msg__TeleOptDevice);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    deeptouch_interface__msg__TeleOptDevice * data =
      (deeptouch_interface__msg__TeleOptDevice *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!deeptouch_interface__msg__TeleOptDevice__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          deeptouch_interface__msg__TeleOptDevice__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!deeptouch_interface__msg__TeleOptDevice__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
