# -*- coding: utf-8 -*-
#
# this module provides various schema operations
from __future__ import absolute_import, unicode_literals

from enum import Enum


class EmptyContextManager(object):
    """ empty context manager. """

    def __init__(self):
        """ do nothing """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Always throw exception """
        return False


class TupleEnum(Enum):
    """ 元组枚举类，可以用来存储多层信息。tuple enum for multi-dimension data enum.

    Example:
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
        obj.values = [value] + list(args)
        return obj

    def get_value_at(self, index):
        return self.values[index]

    @property
    def chinese(self):
        return self.get_value_at(1)

    @classmethod
    def chinese_choices(cls):
        return [(_.value, _.chinese) for _ in cls]
