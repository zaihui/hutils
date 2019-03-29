# -*- coding: utf-8 -*-
#
# this module provides various schema operations
from __future__ import absolute_import, unicode_literals

import contextlib
import enum
from typing import List, Tuple

from hutils.shortcuts import list_get


class EmptyContextManager(contextlib.ContextDecorator):
    """ empty context manager. """

    def __init__(self):
        """ do nothing """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Always throw exception """
        return False


class TupleEnum(enum.Enum):
    """ 元组枚举类，可以用来存储多层信息。tuple enum for multi-dimension data enum.

    Examples::

        class Genders(TupleEnum):
            UNKNOWN = 0, '未知'
            MALE = 1, '男性'
            FEMALE = 2, '女性'
            OTHERS = 3, '其他'
        assert Genders.FEMALE.value == 3
        assert Genders.MALE.chinese == '男性'
    """

    def __new__(cls, value, *args):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.obj_values = [value] + list(args)
        return obj

    def get_value_at(self, index, default=None):
        return list_get(self.obj_values, index, default=default)

    def get_value_from(self, index, key, default=None):
        return self.get_value_at(index, {}).get(key, default)

    @property
    def chinese(self):
        return self.get_value_at(1)

    @property
    def lower_name(self):
        """ name in lower case """
        return self.name.lower()

    @classmethod
    def chinese_choices(cls) -> List[Tuple]:
        return [(_.value, _.chinese) for _ in cls]

    @classmethod
    def values(cls) -> Tuple:
        return tuple(_.value for _ in cls)

    @classmethod
    def from_lower(cls, lower_name):
        upper_name = lower_name.upper()
        for value in cls:
            if value.name == upper_name:
                return value
        raise ValueError('{!r} is not a valid {}'.format(upper_name, cls.__name__))
