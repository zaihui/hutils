# -*- coding: utf-8 -*-
from .classes import EmptyContextManager, TupleEnum
from .data_types import JSONEncoder, bytes_to_str, format_json, get_data, merge_dicts, normalize, quantize
from .decorators import catches, mutes
from .schemas import get_offset_and_limit, get_start_and_end_time
from .shortcuts import (
    date_to_str,
    datetime_combine,
    datetime_to_str,
    get_uid,
    identity,
    list_first,
    list_get,
    log_error,
    mock_lambda,
    str_to_date,
    str_to_datetime,
    tomorrow,
    yesterday,
)
from .unittest import TestCaseMixin, disable_elastic_apm, disable_migration, disable_network, fake_time
from .validators import is_chinese_phone, is_int, is_phone, is_singapore_phone, is_uuid

__version__ = "1.0.10"

__all__ = [
    "EmptyContextManager",
    "JSONEncoder",
    "TestCaseMixin",
    "TupleEnum",
    "bytes_to_str",
    "catches",
    "date_to_str",
    "datetime_combine",
    "datetime_to_str",
    "disable_elastic_apm",
    "disable_migration",
    "disable_network",
    "fake_time",
    "format_json",
    "get_data",
    "get_offset_and_limit",
    "get_start_and_end_time",
    "get_uid",
    "identity",
    "is_chinese_phone",
    "is_int",
    "is_phone",
    "is_singapore_phone",
    "is_uuid",
    "list_first",
    "list_get",
    "log_error",
    "merge_dicts",
    "mock_lambda",
    "mutes",
    "normalize",
    "quantize",
    "str_to_date",
    "str_to_datetime",
    "tomorrow",
    "yesterday",
]

try:
    from .django.apis import Errors, check_error, get_validation_error, get_object_or_error  # NOQA
    from .django.databases import DynamicField, ExtendModelMixin, HManager, HQuerySet, ModelMixin  # NOQA
    from .django.migrations import AlterDefault  # NOQA
    from .django.unittest import extend_django_sqlite  # NOQA

    __all__.extend(
        [
            "AlterDefault",
            "DynamicField",
            "Errors",
            "ExtendModelMixin",
            "HManager",
            "HQuerySet",
            "ModelMixin",
            "check_error",
            "extend_django_sqlite",
            "get_object_or_error",
            "get_validation_error",
        ]
    )
except ImportError:
    pass
