# generated from rosidl_generator_py/resource/_idl.py.em
# with input from deeptouch_interface:msg/HandTouch.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_HandTouch(type):
    """Metaclass of message 'HandTouch'."""

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
                'deeptouch_interface.msg.HandTouch')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__hand_touch
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__hand_touch
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__hand_touch
            cls._TYPE_SUPPORT = module.type_support_msg__msg__hand_touch
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__hand_touch

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class HandTouch(metaclass=Metaclass_HandTouch):
    """Message class 'HandTouch'."""

    __slots__ = [
        '_one',
        '_two',
        '_three',
        '_four',
        '_menu',
        '_primary_thumb',
        '_hand_trigger',
        '_index_trigger',
        '_thumbstick_x',
        '_thumbstick_y',
    ]

    _fields_and_field_types = {
        'one': 'uint8',
        'two': 'uint8',
        'three': 'uint8',
        'four': 'uint8',
        'menu': 'uint8',
        'primary_thumb': 'uint8',
        'hand_trigger': 'float',
        'index_trigger': 'float',
        'thumbstick_x': 'float',
        'thumbstick_y': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.one = kwargs.get('one', int())
        self.two = kwargs.get('two', int())
        self.three = kwargs.get('three', int())
        self.four = kwargs.get('four', int())
        self.menu = kwargs.get('menu', int())
        self.primary_thumb = kwargs.get('primary_thumb', int())
        self.hand_trigger = kwargs.get('hand_trigger', float())
        self.index_trigger = kwargs.get('index_trigger', float())
        self.thumbstick_x = kwargs.get('thumbstick_x', float())
        self.thumbstick_y = kwargs.get('thumbstick_y', float())

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
        if self.one != other.one:
            return False
        if self.two != other.two:
            return False
        if self.three != other.three:
            return False
        if self.four != other.four:
            return False
        if self.menu != other.menu:
            return False
        if self.primary_thumb != other.primary_thumb:
            return False
        if self.hand_trigger != other.hand_trigger:
            return False
        if self.index_trigger != other.index_trigger:
            return False
        if self.thumbstick_x != other.thumbstick_x:
            return False
        if self.thumbstick_y != other.thumbstick_y:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def one(self):
        """Message field 'one'."""
        return self._one

    @one.setter
    def one(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'one' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'one' field must be an unsigned integer in [0, 255]"
        self._one = value

    @builtins.property
    def two(self):
        """Message field 'two'."""
        return self._two

    @two.setter
    def two(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'two' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'two' field must be an unsigned integer in [0, 255]"
        self._two = value

    @builtins.property
    def three(self):
        """Message field 'three'."""
        return self._three

    @three.setter
    def three(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'three' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'three' field must be an unsigned integer in [0, 255]"
        self._three = value

    @builtins.property
    def four(self):
        """Message field 'four'."""
        return self._four

    @four.setter
    def four(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'four' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'four' field must be an unsigned integer in [0, 255]"
        self._four = value

    @builtins.property
    def menu(self):
        """Message field 'menu'."""
        return self._menu

    @menu.setter
    def menu(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'menu' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'menu' field must be an unsigned integer in [0, 255]"
        self._menu = value

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
    def hand_trigger(self):
        """Message field 'hand_trigger'."""
        return self._hand_trigger

    @hand_trigger.setter
    def hand_trigger(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'hand_trigger' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'hand_trigger' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._hand_trigger = value

    @builtins.property
    def index_trigger(self):
        """Message field 'index_trigger'."""
        return self._index_trigger

    @index_trigger.setter
    def index_trigger(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'index_trigger' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'index_trigger' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._index_trigger = value

    @builtins.property
    def thumbstick_x(self):
        """Message field 'thumbstick_x'."""
        return self._thumbstick_x

    @thumbstick_x.setter
    def thumbstick_x(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'thumbstick_x' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'thumbstick_x' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._thumbstick_x = value

    @builtins.property
    def thumbstick_y(self):
        """Message field 'thumbstick_y'."""
        return self._thumbstick_y

    @thumbstick_y.setter
    def thumbstick_y(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'thumbstick_y' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'thumbstick_y' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._thumbstick_y = value
