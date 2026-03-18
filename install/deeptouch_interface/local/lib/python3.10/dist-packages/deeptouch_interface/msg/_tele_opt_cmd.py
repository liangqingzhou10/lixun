# generated from rosidl_generator_py/resource/_idl.py.em
# with input from deeptouch_interface:msg/TeleOptCmd.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TeleOptCmd(type):
    """Metaclass of message 'TeleOptCmd'."""

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
                'deeptouch_interface.msg.TeleOptCmd')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__tele_opt_cmd
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__tele_opt_cmd
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__tele_opt_cmd
            cls._TYPE_SUPPORT = module.type_support_msg__msg__tele_opt_cmd
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__tele_opt_cmd

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


class TeleOptCmd(metaclass=Metaclass_TeleOptCmd):
    """Message class 'TeleOptCmd'."""

    __slots__ = [
        '_is_follow',
        '_is_calibrate_start_pose',
        '_is_absolute_pose',
        '_is_initial_pose',
        '_hand_pose',
        '_gripper_cmd',
        '_record_state',
        '_scale',
        '_primary_thumb',
        '_rating',
    ]

    _fields_and_field_types = {
        'is_follow': 'boolean',
        'is_calibrate_start_pose': 'boolean',
        'is_absolute_pose': 'boolean',
        'is_initial_pose': 'boolean',
        'hand_pose': 'geometry_msgs/Pose',
        'gripper_cmd': 'boolean',
        'record_state': 'string',
        'scale': 'float',
        'primary_thumb': 'uint8',
        'rating': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['geometry_msgs', 'msg'], 'Pose'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.is_follow = kwargs.get('is_follow', bool())
        self.is_calibrate_start_pose = kwargs.get('is_calibrate_start_pose', bool())
        self.is_absolute_pose = kwargs.get('is_absolute_pose', bool())
        self.is_initial_pose = kwargs.get('is_initial_pose', bool())
        from geometry_msgs.msg import Pose
        self.hand_pose = kwargs.get('hand_pose', Pose())
        self.gripper_cmd = kwargs.get('gripper_cmd', bool())
        self.record_state = kwargs.get('record_state', str())
        self.scale = kwargs.get('scale', float())
        self.primary_thumb = kwargs.get('primary_thumb', int())
        self.rating = kwargs.get('rating', int())

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
        if self.is_follow != other.is_follow:
            return False
        if self.is_calibrate_start_pose != other.is_calibrate_start_pose:
            return False
        if self.is_absolute_pose != other.is_absolute_pose:
            return False
        if self.is_initial_pose != other.is_initial_pose:
            return False
        if self.hand_pose != other.hand_pose:
            return False
        if self.gripper_cmd != other.gripper_cmd:
            return False
        if self.record_state != other.record_state:
            return False
        if self.scale != other.scale:
            return False
        if self.primary_thumb != other.primary_thumb:
            return False
        if self.rating != other.rating:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def is_follow(self):
        """Message field 'is_follow'."""
        return self._is_follow

    @is_follow.setter
    def is_follow(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_follow' field must be of type 'bool'"
        self._is_follow = value

    @builtins.property
    def is_calibrate_start_pose(self):
        """Message field 'is_calibrate_start_pose'."""
        return self._is_calibrate_start_pose

    @is_calibrate_start_pose.setter
    def is_calibrate_start_pose(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_calibrate_start_pose' field must be of type 'bool'"
        self._is_calibrate_start_pose = value

    @builtins.property
    def is_absolute_pose(self):
        """Message field 'is_absolute_pose'."""
        return self._is_absolute_pose

    @is_absolute_pose.setter
    def is_absolute_pose(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_absolute_pose' field must be of type 'bool'"
        self._is_absolute_pose = value

    @builtins.property
    def is_initial_pose(self):
        """Message field 'is_initial_pose'."""
        return self._is_initial_pose

    @is_initial_pose.setter
    def is_initial_pose(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'is_initial_pose' field must be of type 'bool'"
        self._is_initial_pose = value

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
    def gripper_cmd(self):
        """Message field 'gripper_cmd'."""
        return self._gripper_cmd

    @gripper_cmd.setter
    def gripper_cmd(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'gripper_cmd' field must be of type 'bool'"
        self._gripper_cmd = value

    @builtins.property
    def record_state(self):
        """Message field 'record_state'."""
        return self._record_state

    @record_state.setter
    def record_state(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'record_state' field must be of type 'str'"
        self._record_state = value

    @builtins.property
    def scale(self):
        """Message field 'scale'."""
        return self._scale

    @scale.setter
    def scale(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'scale' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'scale' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._scale = value

    @builtins.property
    def primary_thumb(self):
        """Message field 'primary_thumb'."""
        return self._primary_thumb

    @primary_thumb.setter
    def primary_thumb(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'primary_thumb' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'primary_thumb' field must be an unsigned integer in [0, 255]"
        self._primary_thumb = value

    @builtins.property
    def rating(self):
        """Message field 'rating'."""
        return self._rating

    @rating.setter
    def rating(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'rating' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'rating' field must be an unsigned integer in [0, 255]"
        self._rating = value
