# generated from rosidl_generator_py/resource/_idl.py.em
# with input from deeptouch_interface:msg/TeleOptDevice.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TeleOptDevice(type):
    """Metaclass of message 'TeleOptDevice'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('deeptouch_interface')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'deeptouch_interface.msg.TeleOptDevice')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tele_opt_device
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tele_opt_device
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tele_opt_device
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tele_opt_device
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tele_opt_device

            from deeptouch_interface.msg import HandTouch
            if HandTouch.__class__._TYPE_SUPPORT is None:
                HandTouch.__class__.__import_type_support__()

            from geometry_msgs.msg import Pose
            if Pose.__class__._TYPE_SUPPORT is None:
                Pose.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class TeleOptDevice(metaclass=Metaclass_TeleOptDevice):
    """Message class 'TeleOptDevice'."""

    __slots__ = [
        '_timestamp',
        '_frame_id',
        '_hand_touch',
        '_hand_pose',
        '_head_pose',
    ]

    _fields_and_field_types = {
        'timestamp': 'float',
        'frame_id': 'uint32',
        'hand_touch': 'deeptouch_interface/HandTouch',
        'hand_pose': 'geometry_msgs/Pose',
        'head_pose': 'geometry_msgs/Pose',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['deeptouch_interface', 'msg'], 'HandTouch'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.timestamp = kwargs.get('timestamp', float())
        self.frame_id = kwargs.get('frame_id', int())
        from deeptouch_interface.msg import HandTouch
        self.hand_touch = kwargs.get('hand_touch', HandTouch())
        from geometry_msgs.msg import Pose
        self.hand_pose = kwargs.get('hand_pose', Pose())
        from geometry_msgs.msg import Pose
        self.head_pose = kwargs.get('head_pose', Pose())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.frame_id != other.frame_id:
            return False
        if self.hand_touch != other.hand_touch:
            return False
        if self.hand_pose != other.hand_pose:
            return False
        if self.head_pose != other.head_pose:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def timestamp(self):
        """Message field 'timestamp'."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'timestamp' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'timestamp' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._timestamp = value

    @builtins.property
    def frame_id(self):
        """Message field 'frame_id'."""
        return self._frame_id

    @frame_id.setter
    def frame_id(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'frame_id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'frame_id' field must be an unsigned integer in [0, 4294967295]"
        self._frame_id = value

    @builtins.property
    def hand_touch(self):
        """Message field 'hand_touch'."""
        return self._hand_touch

    @hand_touch.setter
    def hand_touch(self, value):
        if __debug__:
            from deeptouch_interface.msg import HandTouch
            assert \
                isinstance(value, HandTouch), \
                "The 'hand_touch' field must be a sub message of type 'HandTouch'"
        self._hand_touch = value

    @builtins.property
    def hand_pose(self):
        """Message field 'hand_pose'."""
        return self._hand_pose

    @hand_pose.setter
    def hand_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'hand_pose' field must be a sub message of type 'Pose'"
        self._hand_pose = value

    @builtins.property
    def head_pose(self):
        """Message field 'head_pose'."""
        return self._head_pose

    @head_pose.setter
    def head_pose(self, value):
        if __debug__:
            from geometry_msgs.msg import Pose
            assert \
                isinstance(value, Pose), \
                "The 'head_pose' field must be a sub message of type 'Pose'"
        self._head_pose = value
