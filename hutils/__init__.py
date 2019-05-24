# -*- coding: utf-8 -*-
from .classes import EmptyContextManager, TupleEnum
from .data_types import bytes_to_str, format_json, get_data, merge_dicts, normalize, quantize
from .decorators import catches, ignore_error, mutes, obj_cache
from .schemas import get_offset_and_limit, get_start_and_end_time
from .shortcuts import (
    date_to_str, datetime_combine, datetime_to_str, get_uid, list_first, list_get, log_error, mock_lambda, str_to_date,
    str_to_datetime, tomorrow, yesterday,
)
from .unittest import TestCaseMixin, disable_network, fake_time, get_disable_migration_module
from .validators import is_chinese_phone, is_int, is_uuid

__version__ = '0.6.0'

__all__ = [
    'EmptyContextManager',
    'TestCaseMixin',
    'TupleEnum',
    'bytes_to_str',
    'catches',
    'date_to_str',
    'datetime_combine',
    'datetime_to_str',
    'disable_network',
    'fake_time',
    'format_json',
    'get_data',
    'get_disable_migration_module',
    'get_offset_and_limit',
    'get_start_and_end_time',
    'get_uid',
    'ignore_error',
    'is_chinese_phone',
    'is_int',
    'is_uuid',
    'list_first',
    'list_get',
    'log_error',
    'merge_dicts',
    'mock_lambda',
    'mutes',
    'normalize',
    'obj_cache',
    'quantize',
    'str_to_date',
    'str_to_datetime',
    'tomorrow',
    'yesterday',
]

try:
    from .django.apis import check_error, get_validation_error, get_object_or_error  # NOQA
    from .django.databases import DynamicField, HManager, HQuerySet, ModelMixin  # NOQA
    from .django.migrations import AlterDefault  # NOQA

    __all__.extend([
        'check_error',
        'get_object_or_error',
        'get_validation_error',
        'DynamicField',
        'HManager',
        'HQuerySet',
        'ModelMixin',
        'AlterDefault',
    ])
except ImportError:
    pass
