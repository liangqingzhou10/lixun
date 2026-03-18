// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from deeptouch_interface:msg/TeleOptCmd.idl
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
#include "deeptouch_interface/msg/detail/tele_opt_cmd__struct.h"
#include "deeptouch_interface/msg/detail/tele_opt_cmd__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool geometry_msgs__msg__pose__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * geometry_msgs__msg__pose__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool deeptouch_interface__msg__tele_opt_cmd__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[49];
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
    assert(strncmp("deeptouch_interface.msg._tele_opt_cmd.TeleOptCmd", full_classname_dest, 48) == 0);
  }
  deeptouch_interface__msg__TeleOptCmd * ros_message = _ros_message;
  {  // is_follow
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_follow");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_follow = (Py_True == field);
    Py_DECREF(field);
  }
  {  // is_calibrate_start_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_calibrate_start_pose");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_calibrate_start_pose = (Py_True == field);
    Py_DECREF(field);
  }
  {  // is_absolute_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_absolute_pose");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_absolute_pose = (Py_True == field);
    Py_DECREF(field);
  }
  {  // is_initial_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_initial_pose");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_initial_pose = (Py_True == field);
    Py_DECREF(field);
  }
  {  // hand_pose
    PyObject * field = PyObject_GetAttrString(_pymsg, "hand_pose");
    if (!field) {
      return false;
    }
    if (!geometry_msgs__msg__pose__convert_from_py(field, &ros_message->hand_pose)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // gripper_cmd
    PyObject * field = PyObject_GetAttrString(_pymsg, "gripper_cmd");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->gripper_cmd = (Py_True == field);
    Py_DECREF(field);
  }
  {  // record_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "record_state");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->record_state, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // scale
    PyObject * field = PyObject_GetAttrString(_pymsg, "scale");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->scale = (float)PyFloat_AS_DOUBLE(field);
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
  {  // rating
    PyObject * field = PyObject_GetAttrString(_pymsg, "rating");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->rating = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * deeptouch_interface__msg__tele_opt_cmd__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of TeleOptCmd */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("deeptouch_interface.msg._tele_opt_cmd");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "TeleOptCmd");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  deeptouch_interface__msg__TeleOptCmd * ros_message = (deeptouch_interface__msg__TeleOptCmd *)raw_ros_message;
  {  // is_follow
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_follow ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_follow", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // is_calibrate_start_pose
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_calibrate_start_pose ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_calibrate_start_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // is_absolute_pose
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_absolute_pose ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_absolute_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // is_initial_pose
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_initial_pose ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_initial_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // hand_pose
    PyObject * field = NULL;
    field = geometry_msgs__msg__pose__convert_to_py(&ros_message->hand_pose);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "hand_pose", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // gripper_cmd
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->gripper_cmd ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "gripper_cmd", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // record_state
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->record_state.data,
      strlen(ros_message->record_state.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "record_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // scale
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->scale);
    {
      int rc = PyObject_SetAttrString(_pymessage, "scale", field);
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
  {  // rating
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->rating);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rating", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
