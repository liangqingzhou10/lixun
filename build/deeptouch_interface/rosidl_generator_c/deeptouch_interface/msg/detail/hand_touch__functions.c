// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice
#include "deeptouch_interface/msg/detail/hand_touch__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
deeptouch_interface__msg__HandTouch__init(deeptouch_interface__msg__HandTouch * msg)
{
  if (!msg) {
    return false;
  }
  // one
  // two
  // three
  // four
  // menu
  // primary_thumb
  // hand_trigger
  // index_trigger
  // thumbstick_x
  // thumbstick_y
  return true;
}

void
deeptouch_interface__msg__HandTouch__fini(deeptouch_interface__msg__HandTouch * msg)
{
  if (!msg) {
    return;
  }
  // one
  // two
  // three
  // four
  // menu
  // primary_thumb
  // hand_trigger
  // index_trigger
  // thumbstick_x
  // thumbstick_y
}

bool
deeptouch_interface__msg__HandTouch__are_equal(const deeptouch_interface__msg__HandTouch * lhs, const deeptouch_interface__msg__HandTouch * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // one
  if (lhs->one != rhs->one) {
    return false;
  }
  // two
  if (lhs->two != rhs->two) {
    return false;
  }
  // three
  if (lhs->three != rhs->three) {
    return false;
  }
  // four
  if (lhs->four != rhs->four) {
    return false;
  }
  // menu
  if (lhs->menu != rhs->menu) {
    return false;
  }
  // primary_thumb
  if (lhs->primary_thumb != rhs->primary_thumb) {
    return false;
  }
  // hand_trigger
  if (lhs->hand_trigger != rhs->hand_trigger) {
    return false;
  }
  // index_trigger
  if (lhs->index_trigger != rhs->index_trigger) {
    return false;
  }
  // thumbstick_x
  if (lhs->thumbstick_x != rhs->thumbstick_x) {
    return false;
  }
  // thumbstick_y
  if (lhs->thumbstick_y != rhs->thumbstick_y) {
    return false;
  }
  return true;
}

bool
deeptouch_interface__msg__HandTouch__copy(
  const deeptouch_interface__msg__HandTouch * input,
  deeptouch_interface__msg__HandTouch * output)
{
  if (!input || !output) {
    return false;
  }
  // one
  output->one = input->one;
  // two
  output->two = input->two;
  // three
  output->three = input->three;
  // four
  output->four = input->four;
  // menu
  output->menu = input->menu;
  // primary_thumb
  output->primary_thumb = input->primary_thumb;
  // hand_trigger
  output->hand_trigger = input->hand_trigger;
  // index_trigger
  output->index_trigger = input->index_trigger;
  // thumbstick_x
  output->thumbstick_x = input->thumbstick_x;
  // thumbstick_y
  output->thumbstick_y = input->thumbstick_y;
  return true;
}

deeptouch_interface__msg__HandTouch *
deeptouch_interface__msg__HandTouch__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__HandTouch * msg = (deeptouch_interface__msg__HandTouch *)allocator.allocate(sizeof(deeptouch_interface__msg__HandTouch), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(deeptouch_interface__msg__HandTouch));
  bool success = deeptouch_interface__msg__HandTouch__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
deeptouch_interface__msg__HandTouch__destroy(deeptouch_interface__msg__HandTouch * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    deeptouch_interface__msg__HandTouch__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
deeptouch_interface__msg__HandTouch__Sequence__init(deeptouch_interface__msg__HandTouch__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__HandTouch * data = NULL;

  if (size) {
    data = (deeptouch_interface__msg__HandTouch *)allocator.zero_allocate(size, sizeof(deeptouch_interface__msg__HandTouch), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = deeptouch_interface__msg__HandTouch__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        deeptouch_interface__msg__HandTouch__fini(&data[i - 1]);
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
deeptouch_interface__msg__HandTouch__Sequence__fini(deeptouch_interface__msg__HandTouch__Sequence * array)
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
      deeptouch_interface__msg__HandTouch__fini(&array->data[i]);
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

deeptouch_interface__msg__HandTouch__Sequence *
deeptouch_interface__msg__HandTouch__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  deeptouch_interface__msg__HandTouch__Sequence * array = (deeptouch_interface__msg__HandTouch__Sequence *)allocator.allocate(sizeof(deeptouch_interface__msg__HandTouch__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = deeptouch_interface__msg__HandTouch__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
deeptouch_interface__msg__HandTouch__Sequence__destroy(deeptouch_interface__msg__HandTouch__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    deeptouch_interface__msg__HandTouch__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
deeptouch_interface__msg__HandTouch__Sequence__are_equal(const deeptouch_interface__msg__HandTouch__Sequence * lhs, const deeptouch_interface__msg__HandTouch__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!deeptouch_interface__msg__HandTouch__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
deeptouch_interface__msg__HandTouch__Sequence__copy(
  const deeptouch_interface__msg__HandTouch__Sequence * input,
  deeptouch_interface__msg__HandTouch__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(deeptouch_interface__msg__HandTouch);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    deeptouch_interface__msg__HandTouch * data =
      (deeptouch_interface__msg__HandTouch *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!deeptouch_interface__msg__HandTouch__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          deeptouch_interface__msg__HandTouch__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!deeptouch_interface__msg__HandTouch__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
