# -*- coding: utf-8 -*-
from .classes import EmptyContextManager, TupleEnum
from .data_types import bytes_to_str, format_json, get_data, merge_dicts, normalize, quantize
from .decorators import catches, obj_cache
from .schemas import get_offset_and_limit, get_start_and_end_time
from .shortcuts import (
    date_to_str, datetime_combine, datetime_to_str, get_uid, list_first, list_get, log_error, mock_lambda, str_to_date,
    str_to_datetime,
)
from .validators import is_chinese_phone, is_int, is_uuid

__version__ = '0.3.6'

__all__ = [
    'EmptyContextManager',
    'TupleEnum',
    'bytes_to_str',
    'format_json',
    'get_data',
    'merge_dicts',
    'normalize',
    'quantize',
    'catches',
    'obj_cache',
    'get_offset_and_limit',
    'get_start_and_end_time',
    'date_to_str',
    'datetime_combine',
    'datetime_to_str',
    'get_uid',
    'list_first',
    'list_get',
    'log_error',
    'mock_lambda',
    'str_to_date',
    'str_to_datetime',
    'is_chinese_phone',
    'is_int',
    'is_uuid',
]

try:
    from .django.apis import get_validation_error, get_object_or_error  # NOQA
    from .django.databases import DynamicField, ModelMixin, flat_transaction  # NOQA

    __all__.extend([
        'get_object_or_error',
        'get_validation_error',
        'DynamicField',
        'ModelMixin',
        'flat_transaction',
    ])
except ImportError:
    pass
