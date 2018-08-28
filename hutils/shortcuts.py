# -*- coding: utf-8 -*-
#
# this module provides various one liners
from __future__ import absolute_import, unicode_literals

import datetime


def datetime_combine(start_date, end_date=None):
    """ 获取一段日期的起止时间。get start/end datetime from date.

    Args:
        start_date (datetime.date): start date.
        end_date (datetime.date): end date.

    Examples:
        >>> start, end = datetime_combine(datetime.date.today())

    Returns:
        tuple[datetime, datetime]
    """
    end_date = end_date or start_date
    return (
        datetime.datetime.combine(start_date, datetime.time.min),
        datetime.datetime.combine(end_date, datetime.time.max),
    )


def get_uid(instance):
    """ 获取实例的 uid (hex). get hex uid from instance.

    Examples:
    Before:
        >>> data = {
        >>>     'uid': instance.uid.hex if instance else None,
        >>>     'related_uid': instance.related.uid.hex if instance.related else None,
        >>> }
    After:
        >>> data = {
        >>>     'uid': get_uid(instance),
        >>>     'related_uid': get_uid(instance.related),
        >>> }

    :rtype: str | None
    """
    return instance.uid.hex if instance else None


def list_first(instances, default=None):
    """ 获取列表的第一个元素，假如没有第一个元素则返回默认值。get first value of a list or default value.

    Examples:
        >>> list_first(instances)
        None

    Args:
        instances (list): the list
        default: the default value
    """
    return list_get(instances, 0, default=default)


def list_get(instances, index, default=None):
    """ 根据索引号获取列表值或者默认值。get default value on index out of range for list.

    Examples:
        >>> list_get([0, 1, 2], 3, 4)
        4

    Args:
        instances (list): the list
        index (int): the index
        default: the default value
    """
    try:
        return instances[index]
    except IndexError:
        return default


def mock_lambda(return_value=None, raises=None, **kwargs):
    """ 伪造返回数据的快捷函数。convenient method to mock return value.

    Examples:
        >>> mock.patch('hutils.merge_dicts', mock_lambda(a=1, b=2))
        >>> mock.patch('hutils.merge_dicts', mock_lambda(raises=ValueError))

    Args:
        return_value: the return value
        raises: the exception to raise
        kwargs: a shortcut for define dictionary return value
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
