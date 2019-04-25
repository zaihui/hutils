# -*- coding: utf-8 -*-
#
# this module provides various one liners
from __future__ import absolute_import, unicode_literals

import datetime
import logging
from typing import Iterable, Optional, Tuple


def datetime_combine(
        start_date: datetime.date, end_date: datetime.date = None,
        delta_days: Optional[int] = None) -> Tuple[datetime.datetime, datetime.datetime]:
    """ 获取一段日期的起止时间。get start/end datetime from date.

    Examples::

        start, end = datetime_combine(datetime.date.today())
        yesterday, today = datetime_combine(datetime.date.today(), delta_days=-1)
        today, a_week_after = datetime_combine(datetime.date.today(), delta_days=7)
    """
    if end_date and delta_days is not None:
        raise ValueError('Can not specify end_date and delta_days at the same time')
    if delta_days is not None:
        start_date, end_date = start_date, start_date + datetime.timedelta(days=delta_days)
        if delta_days < 0:
            start_date, end_date = end_date, start_date
    end_date = end_date or start_date
    return (
        datetime.datetime.combine(start_date, datetime.time.min),
        datetime.datetime.combine(end_date, datetime.time.max),
    )


def datetime_to_str(value, fmt='%Y-%m-%d %H:%M:%S'):
    """ 时间类型转换为字符串。datetime to string.

    :type value: datetime.datetime
    :type fmt: str
    :rtype: str
    """
    return value.strftime(fmt)


def date_to_str(value, fmt='%Y-%m-%d'):
    """ 日期类型转换为字符串。date to string.

    :type value: datetime.date
    :type fmt: str
    :rtype: str
    """
    return value.strftime(fmt)


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


def mock_lambda(return_value=None, raises: Exception = None, **kwargs):
    """ 伪造返回数据的快捷函数。convenient method to mock return value.

    Examples::

        mock.patch('hutils.merge_dicts', mock_lambda(a=1, b=2))
        mock.patch('hutils.merge_dicts', mock_lambda(raises=ValueError()))
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


def log_error(logger, message, *args, exc_info=True, **kwargs):
    """ 记录错误日志的快捷方式，顺带支持 Sentry。log error, supports sentry detail trace.

    Examples::

        log_error(logger, ex)
        log_error(__name__, 'this message will show on sentry')
    """
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    if isinstance(message, Exception) or exc_info:
        logger.exception(message, *args, **kwargs)
    else:
        # https://github.com/getsentry/raven-python/blob/master/docs/integrations/logging.rst#usage
        logger.error(message, *args, extra={'stack': True}, **kwargs)


def str_to_datetime(value, fmt='%Y-%m-%d %H:%M:%S'):
    """ 时间类型转换为字符串。datetime to string.

    :type value: str
    :type fmt: str
    :rtype: datetime.datetime
    """
    return datetime.datetime.strptime(value, fmt)


def str_to_date(value, fmt='%Y-%m-%d'):
    """ 日期类型转换为字符串。date to string.

    :type value: str
    :type fmt: str
    :rtype: datetime.date
    """
    return datetime.datetime.strptime(value, fmt).date()


def tomorrow() -> datetime.datetime:
    """ 获取昨天的时间 """
    return datetime.datetime.now() + datetime.timedelta(days=1)


def yesterday() -> datetime.datetime:
    """ 获取昨天的时间 """
    return datetime.datetime.now() - datetime.timedelta(days=1)
