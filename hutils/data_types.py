# -*- coding: utf-8 -*-
#
# this module provides various data types operation
from __future__ import absolute_import, unicode_literals

import decimal


def bytes_to_str(data):
    """ 二进制类型转换为字符串，支持嵌套数组。bytes to string, supports nested list.

    Example:
        string_value = bytes_to_str(redis.get('key'))
    Or:
        values = bytes_to_str(redis.mget(*keys))
    """
    if data is None:
        return data
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, str):
        return data
    return [bytes_to_str(_) for _ in data]


def get_data(data, *keys, optional=False):
    """ 从字典数据类型中批量获取变量。get list data from dict.

    Example:
        offset, limit, from_date, to_date = get_data(request.data, 'offset', 'limit', 'from', 'to', optional=True)

    :type data: dict
    :type keys: str
    :type optional: bool
    """
    if optional:
        return map(lambda key: data.get(key), keys)
    return map(lambda key: data[key], keys)


def merge_dicts(*dicts):
    """ 依次合并多个字典。merge multiple dict one by one.

    Example:
        offset_limit_schema = {'offset': Validation(...), 'limit': Validation(...)}
        ...
        schema = merge_dicts(offset_limit_schema, from_to_schema, payment_schema)

    :type dicts: dict
    :rtype: dict
    """
    dict_merged = {}
    for d in dicts:
        dict_merged.update(d)
    return dict_merged


def quantize(value, rounding=decimal.ROUND_HALF_UP):
    """ 强制转换为两位小数类型。quantize value to two digits decimal.

    Example:
        price_list = [(5.25, 3.33), (6.98, 3.14)]
        sales_volume = sum(quantize(unit_price * amount) for unit_price, amount in price_list)

    :rtype: decimal.Decimal
    """
    return decimal.Decimal(value).quantize(decimal.Decimal('.01'), rounding=rounding)
