# -*- coding: utf-8 -*-
#
# this module provides various data types operation
from __future__ import absolute_import, unicode_literals

import datetime
import decimal
import json

try:
    import pymongo  # NOQA
    import bson
except ImportError:
    bson = False


def bytes_to_str(data):
    """ 二进制类型转换为字符串，支持嵌套数组。bytes to string, supports nested list.

    Examples::

        string_value = bytes_to_str(redis.get('key'))
        values = bytes_to_str(redis.mget(*keys))
    """
    if data is None:
        return data
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, str):
        return data
    return [bytes_to_str(_) for _ in data]


class JSONEncoder(json.JSONEncoder):
    """ 序列化 JSON """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        if bson and isinstance(o, bson.Decimal128):
            return str(o.to_decimal())
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        return json.JSONEncoder.default(self, o)


def format_json(data, ensure_ascii=False, **kwargs):
    """ 序列化 JSON，支持中文和 datetime, decimal 类型。format json with utf8/datetime/decimal support.

    Examples::

        format_json({'key': 'name', 'value': '强哥'})
        # '{"key": "name", "value": "强哥"}'

    :rtype: str
    """

    kwargs.update(ensure_ascii=ensure_ascii, cls=JSONEncoder)
    return json.dumps(data, **kwargs)


def get_data(data, *keys, optional=False):
    """ 从字典数据类型中批量获取变量。get list data from dict.

    Examples::

        offset, limit, from_date, to_date = get_data(request.data, 'offset', 'limit', 'from', 'to', optional=True)

    :type data: dict
    :type keys: str
    :type optional: bool
    """
    if optional:
        return map(lambda key: data.get(key), keys)
    return map(lambda key: data[key], keys)


def merge_dicts(*dicts: dict) -> dict:
    """ 依次合并多个字典。merge multiple dict one by one.

    Examples::

        offset_limit_schema = {'offset': Validation(...), 'limit': Validation(...)}
        ...
        schema = merge_dicts(offset_limit_schema, from_to_schema, payment_schema)
    """
    dict_merged = {}
    for d in dicts:
        dict_merged.update(d)
    return dict_merged


def normalize(value):
    """ 将一个数右边的零给干掉。remove trailing zeros from number.

    Examples::

        normalize('80.00')
        # '80'
        normalize('12.30')
        # '12.3'
        normalize('6.66')
        # '6.66'

    :rtype: str
    """
    str_value = str(value)
    return str_value.rstrip("0").rstrip(".") if "." in str_value else str_value


def quantize(value, rounding=decimal.ROUND_HALF_UP):
    """ 强制转换为两位小数类型。quantize value to two digits decimal.

    Examples::

        price_list = [(5.25, 3.33), (6.98, 3.14)]
        sales_volume = sum(quantize(unit_price * amount) for unit_price, amount in price_list)

    :rtype: decimal.Decimal
    """
    return decimal.Decimal(value).quantize(decimal.Decimal(".01"), rounding=rounding)
