# -*- coding: utf-8 -*-
#
# this module provides various one liners
from __future__ import absolute_import, unicode_literals

import datetime
from typing import Iterable, Tuple, Type


def datetime_combine(
        start_date: datetime.date, end_date: datetime.date = None) -> Tuple[datetime.datetime, datetime.datetime]:
    """ 获取一段日期的起止时间。get start/end datetime from date.

    Examples::

        start, end = datetime_combine(datetime.date.today())
    """
    end_date = end_date or start_date
    return (
        datetime.datetime.combine(start_date, datetime.time.min),
        datetime.datetime.combine(end_date, datetime.time.max),
    )


def get_uid(instance):
    """ 获取实例的 uid (hex). get hex uid from instance.

    Examples::

        data = {
            'uid': instance.uid.hex if instance else None,
            'related_uid': instance.related.uid.hex if instance.related else None,
        }

        data = {
            'uid': get_uid(instance),
            'related_uid': get_uid(instance.related),
        }

    :rtype: str | None
    """
    return instance.uid.hex if instance else None


def list_first(instances: Iterable, default=None):
    """ 获取列表的第一个元素，假如没有第一个元素则返回默认值。get first value of a list or default value.

    Examples::

        list_first(instances)
        # None
    """
    return list_get(instances, 0, default=default)


def list_get(instances: Iterable, index: int, default=None):
    """ 根据索引号获取列表值或者默认值。get default value on index out of range for list.

    Examples::

        list_get([0, 1, 2], 3, 4)
        # 4
    """
    try:
        return list(instances)[index]
    except IndexError:
        return default


def mock_lambda(return_value=None, raises: Type[Exception] = None, **kwargs):
    """ 伪造返回数据的快捷函数。convenient method to mock return value.

    Examples::

        mock.patch('hutils.merge_dicts', mock_lambda(a=1, b=2))
        mock.patch('hutils.merge_dicts', mock_lambda(raises=ValueError))
    """

    def func(*_, **__):
        if raises is not None:
            raise raises
        if return_value is not None:
            if isinstance(return_value, dict):
                return return_value.copy()
            return return_value
        return kwargs.copy()

    return func
