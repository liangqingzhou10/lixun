// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/tele_opt_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `hand_pose`
#include "geometry_msgs/msg/detail/pose__functions.h"
// Member `record_state`
#include "rosidl_runtime_c/string_functions.h"

bool
deeptouch_interface__msg__TeleOptCmd__init(deeptouch_interface__msg__TeleOptCmd * msg)
{
  if (!msg) {
    return false;
  }
  // is_follow
  // is_calibrate_start_pose
  // is_absolute_pose
  // is_initial_pose
  // hand_pose
  if (!geometry_msgs__msg__Pose__init(&msg->hand_pose)) {
    deeptouch_interface__msg__TeleOptCmd__fini(msg);
    return false;
  }
  // gripper_cmd
  // record_state
  if (!rosidl_runtime_c__String__init(&msg->record_state)) {
    deeptouch_interface__msg__TeleOptCmd__fini(msg);
    return false;
  }
  // scale
  // primary_thumb
  // rating
  return true;
}

void
deeptouch_interface__msg__TeleOptCmd__fini(deeptouch_interface__msg__TeleOptCmd * msg)
{
  if (!msg) {
    return;
  }
  // is_follow
  // is_calibrate_start_pose
  // is_absolute_pose
  // is_initial_pose
  // hand_pose
  geometry_msgs__msg__Pose__fini(&msg->hand_pose);
  // gripper_cmd
  // record_state
  rosidl_runtime_c__String__fini(&msg->record_state);
  // scale
  // primary_thumb
  // rating
}

bool
deeptouch_interface__msg__TeleOptCmd__are_equal(const deeptouch_interface__msg__TeleOptCmd * lhs, const deeptouch_interface__msg__TeleOptCmd * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // is_follow
  if (lhs->is_follow != rhs->is_follow) {
    return false;
  }
  // is_calibrate_start_pose
  if (lhs->is_calibrate_start_pose != rhs->is_calibrate_start_pose) {
    return false;
  }
  // is_absolute_pose
  if (lhs->is_absolute_pose != rhs->is_absolute_pose) {
    return false;
  }
  // is_initial_pose
  if (lhs->is_initial_pose != rhs->is_initial_pose) {
    return false;
  }
  // hand_pose
  if (!geometry_msgs__msg__Pose__are_equal(
      &(lhs->hand_pose), &(rhs->hand_pose)))
  {
    return false;
  }
  // gripper_cmd
  if (lhs->gripper_cmd != rhs->gripper_cmd) {
    return false;
  }
  // record_state
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->record_state), &(rhs->record_state)))
  {
    return false;
  }
  // scale
  if (lhs->scale != rhs->scale) {
    return false;
  }
  // primary_thumb
  if (lhs->primary_thumb != rhs->primary_thumb) {
    return false;
  }
  // rating
  if (lhs->rating != rhs->rating) {
    return false;
  }
  return true;
}

bool
deeptouch_interface__msg__TeleOptCmd__copy(
  const deeptouch_interface__msg__TeleOptCmd * input,
  deeptouch_interface__msg__TeleOptCmd * output)
{
  if (!input || !output) {
    return false;
  }
  // is_follow
  output->is_follow = input->is_follow;
  // is_calibrate_start_pose
  output->is_calibrate_start_pose = input->is_calibrate_start_pose;
  // is_absolute_pose
  output->is_absolute_pose = input->is_absolute_pose;
  // is_initial_pose
  output->is_initial_pose = input->is_initial_pose;
  // hand_pose
  if (!geometry_msgs__msg__Pose__copy(
      &(input->hand_pose), &(output->hand_pose)))
  {
    return false;
  }
  // gripper_cmd
  output->gripper_cmd = input->gripper_cmd;
  // record_state
  if (!rosidl_runtime_c__String__copy(
      &(input->record_state), &(output->record_state)))
  {
    return false;
  }
  // scale
  output->scale = input->scale;
  // primary_thumb
  output->primary_thumb = input->primary_thumb;
  // rating
  output->rating = input->rating;
  return true;
}

deeptouch_interface__msg__TeleOptCmd *
deeptouch_interface__msg__TeleOptCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptCmd * msg = (deeptouch_interface__msg__TeleOptCmd *)allocator.allocate(sizeof(deeptouch_interface__msg__TeleOptCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(deeptouch_interface__msg__TeleOptCmd));
  bool success = deeptouch_interface__msg__TeleOptCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
deeptouch_interface__msg__TeleOptCmd__destroy(deeptouch_interface__msg__TeleOptCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    deeptouch_interface__msg__TeleOptCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
deeptouch_interface__msg__TeleOptCmd__Sequence__init(deeptouch_interface__msg__TeleOptCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptCmd * data = NULL;

  if (size) {
    data = (deeptouch_interface__msg__TeleOptCmd *)allocator.zero_allocate(size, sizeof(deeptouch_interface__msg__TeleOptCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = deeptouch_interface__msg__TeleOptCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        deeptouch_interface__msg__TeleOptCmd__fini(&data[i - 1]);
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
deeptouch_interface__msg__TeleOptCmd__Sequence__fini(deeptouch_interface__msg__TeleOptCmd__Sequence * array)
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
      deeptouch_interface__msg__TeleOptCmd__fini(&array->data[i]);
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

deeptouch_interface__msg__TeleOptCmd__Sequence *
deeptouch_interface__msg__TeleOptCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__TeleOptCmd__Sequence * array = (deeptouch_interface__msg__TeleOptCmd__Sequence *)allocator.allocate(sizeof(deeptouch_interface__msg__TeleOptCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = deeptouch_interface__msg__TeleOptCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
deeptouch_interface__msg__TeleOptCmd__Sequence__destroy(deeptouch_interface__msg__TeleOptCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    deeptouch_interface__msg__TeleOptCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
deeptouch_interface__msg__TeleOptCmd__Sequence__are_equal(const deeptouch_interface__msg__TeleOptCmd__Sequence * lhs, const deeptouch_interface__msg__TeleOptCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!deeptouch_interface__msg__TeleOptCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
deeptouch_interface__msg__TeleOptCmd__Sequence__copy(
  const deeptouch_interface__msg__TeleOptCmd__Sequence * input,
  deeptouch_interface__msg__TeleOptCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(deeptouch_interface__msg__TeleOptCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    deeptouch_interface__msg__TeleOptCmd * data =
      (deeptouch_interface__msg__TeleOptCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!deeptouch_interface__msg__TeleOptCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          deeptouch_interface__msg__TeleOptCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!deeptouch_interface__msg__TeleOptCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
