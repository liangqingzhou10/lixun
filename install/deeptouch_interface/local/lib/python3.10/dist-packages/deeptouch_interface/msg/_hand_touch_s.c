// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from deeptouch_interface:msg/HandTouch.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "deeptouch_interface/msg/detail/hand_touch__struct.h"
#include "deeptouch_interface/msg/detail/hand_touch__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool deeptouch_interface__msg__hand_touch__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[46];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("deeptouch_interface.msg._hand_touch.HandTouch", full_classname_dest, 45) == 0);
  }
  deeptouch_interface__msg__HandTouch * ros_message = _ros_message;
  {  // one
    PyObject * field = PyObject_GetAttrString(_pymsg, "one");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->one = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // two
    PyObject * field = PyObject_GetAttrString(_pymsg, "two");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->two = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // three
    PyObject * field = PyObject_GetAttrString(_pymsg, "three");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->three = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // four
    PyObject * field = PyObject_GetAttrString(_pymsg, "four");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->four = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // menu
    PyObject * field = PyObject_GetAttrString(_pymsg, "menu");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->menu = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // primary_thumb
    PyObject * field = PyObject_GetAttrString(_pymsg, "primary_thumb");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->primary_thumb = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // hand_trigger
    PyObject * field = PyObject_GetAttrString(_pymsg, "hand_trigger");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->hand_trigger = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // index_trigger
    PyObject * field = PyObject_GetAttrString(_pymsg, "index_trigger");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->index_trigger = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // thumbstick_x
    PyObject * field = PyObject_GetAttrString(_pymsg, "thumbstick_x");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->thumbstick_x = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // thumbstick_y
    PyObject * field = PyObject_GetAttrString(_pymsg, "thumbstick_y");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->thumbstick_y = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * deeptouch_interface__msg__hand_touch__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of HandTouch */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("deeptouch_interface.msg._hand_touch");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "HandTouch");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  deeptouch_interface__msg__HandTouch * ros_message = (deeptouch_interface__msg__HandTouch *)raw_ros_message;
  {  // one
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->one);
    {
      int rc = PyObject_SetAttrString(_pymessage, "one", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // two
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->two);
    {
      int rc = PyObject_SetAttrString(_pymessage, "two", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // three
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->three);
    {
      int rc = PyObject_SetAttrString(_pymessage, "three", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // four
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->four);
    {
      int rc = PyObject_SetAttrString(_pymessage, "four", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // menu
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->menu);
    {
      int rc = PyObject_SetAttrString(_pymessage, "menu", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // primary_thumb
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->primary_thumb);
    {
      int rc = PyObject_SetAttrString(_pymessage, "primary_thumb", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // hand_trigger
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->hand_trigger);
    {
      int rc = PyObject_SetAttrString(_pymessage, "hand_trigger", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // index_trigger
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->index_trigger);
    {
      int rc = PyObject_SetAttrString(_pymessage, "index_trigger", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // thumbstick_x
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->thumbstick_x);
    {
      int rc = PyObject_SetAttrString(_pymessage, "thumbstick_x", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // thumbstick_y
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->thumbstick_y);
    {
      int rc = PyObject_SetAttrString(_pymessage, "thumbstick_y", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
