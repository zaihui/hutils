# -*- coding: utf-8 -*-
#
# this module provides various schema operations
from __future__ import absolute_import, unicode_literals

import datetime


def get_offset_and_limit(data, max_limit=None, default_offset=0, default_limit=20):
    """ 从数据中获取偏移量和每页数量。get offset and limit from data.

    Examples::

        offset, limit = get_offset_and_limit(request.data, max_limit=100)

    :type data: dict
    :type max_limit: int
    :type default_offset: int
    :type default_limit: int
    :rtype: (int, int)
    """
    offset = int(data.get("offset", default_offset))
    limit = int(data.get("limit", default_limit))
    if offset < 0 or limit < offset:
        raise ValueError("偏移量或每页数量低于限制，请重新选择")
    if max_limit and limit > max_limit:
        raise ValueError("每页数量不能多于 {} 个，请重新选择".format(max_limit))
    return offset, limit


def get_start_and_end_time(data, max_delta_days=400, prefix="", is_datetime=True):
    """ 从数据中获取起止日期。get start and end time from data.

    Examples::

        start, end = get_start_and_end_time(request.data, is_datetime=False)

    :type data: dict
    :type max_delta_days: int
    :type prefix: str
    :type is_datetime: bool
    :rtype: (datetime.datetime | datetime.date, datetime.datetime | datetime.date)
    """
    start = data.get(prefix + "from")
    end = data.get(prefix + "to")
    if start and end and end < start:
        raise ValueError("时间范围错误，起始日期超过结束日期，请选择正确的起止日期")
    if start and end and end - start > datetime.timedelta(days=max_delta_days):
        raise ValueError("时间范围错误，间隔天数超出 {} 天，请选择更小的间隔范围".format(max_delta_days))
    if is_datetime:
        if start:
            start = datetime.datetime.combine(start, datetime.time.min)
        if end:
            end = datetime.datetime.combine(end, datetime.time.max)
    return start, end
