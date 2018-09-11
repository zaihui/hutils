# -*- coding: utf-8 -*-
from .classes import EmptyContextManager, TupleEnum
from .data_types import bytes_to_str, format_json, get_data, merge_dicts, normalize, quantize
from .schemas import get_offset_and_limit, get_start_and_end_time
from .shortcuts import (
    date_to_str, datetime_combine, datetime_to_str, get_uid, list_first, list_get, mock_lambda,
    str_to_date, str_to_datetime,
)
from .storages import obj_cache
from .validators import is_chinese_phone, is_int, is_uuid

__version__ = '0.3.2'

__all__ = [
    'EmptyContextManager',
    'TupleEnum',
    'bytes_to_str',
    'format_json',
    'get_data',
    'merge_dicts',
    'normalize',
    'quantize',
    'get_offset_and_limit',
    'get_start_and_end_time',
    'date_to_str',
    'datetime_combine',
    'datetime_to_str',
    'get_uid',
    'list_first',
    'list_get',
    'mock_lambda',
    'str_to_date',
    'str_to_datetime',
    'obj_cache',
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
