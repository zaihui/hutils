# -*- coding: utf-8 -*-
#
# this module provides django rest framework related methods
import enum
import inspect

from django.core.exceptions import ValidationError
from django.db import models

from hutils import list_get, log_error


def get_validation_error(message, data=None, code=None):
    """ 方便快捷抛 400 的函数。shortcut for raising bad request error in django-rest-framework.

    Examples::

        raise get_validation_error('非法的请求')

    :rtype: rest_framework.exceptions.ValidationError
    """
    try:
        from rest_framework.exceptions import ValidationError

        error = {"message": str(message)}
        if data is not None:
            error["data"] = data
        if code is not None:
            error["code"] = code
        return ValidationError(error)
    except ImportError:
        from django.core.exceptions import ValidationError

        return ValidationError(message=message, code=code, params=data)


def check_error(error, *args, error_method=get_validation_error, **kwargs):
    """ 检查错误，有错抛错，没错继续。check errors or raise error

    Examples::

        check_error(1 + 1 != 2, 'the math')
    """
    if error:
        raise error_method(*args, **kwargs)


def get_object_or_error(
    cls, *queries, _select_models=(), _prefetch_models=(), _err_msg=None, _err_func=get_validation_error, **kwargs
):
    """ 类似 get_object_or_404。similar to get_object_or_404.

    Examples::
        user = get_object_or_error(User, uid=uid)

    :type cls: (() -> T) | T
    :type queries: django.db.models.query_utils.Q
    :type _select_models: tuple
    :type _prefetch_models: tuple
    :type _err_func: method
    :type _err_msg: str
    :rtype: T
    """
    if inspect.isclass(cls) and issubclass(cls, models.Model):
        queryset = cls.objects
        model = cls
    else:
        queryset = cls
        model = cls.model
    if queries:
        queryset = queryset.filter(*queries)
    if _select_models:
        queryset = queryset.select_related(*_select_models)
    if _prefetch_models:
        queryset = queryset.prefetch_related(*_prefetch_models)
    try:
        result = queryset.get(**kwargs)
    except (model.DoesNotExist, ValueError, ValidationError):  # 找不到，或者uid格式错误
        raise _err_func(_err_msg or "{} 不存在".format(model.__name__))
    return result


class Errors(enum.Enum):
    """ 错误类 """

    def __new__(cls, value, *args):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.obj_values = [value] + list(args)
        return obj

    def check(self, condition, **kwargs):
        check_error(condition, self.value.format(**kwargs), code=self.code)

    def error(self, *args, error_data=None, error_code=None, logger=None, **kwargs):
        if logger:
            log_error(logger, self.value)
        return get_validation_error(self.value.format(*args, **kwargs), data=error_data, code=error_code)

    @classmethod
    def lazy_error(cls, ex: Exception):
        """ 一般这里都是后端懒的搞，直接 except Exception 转前端报错。一般不推荐，所以在这种情况都统统打 sentry, 一定要处理 """
        log_error(__name__, ex)
        return get_validation_error(str(ex))

    @property
    def code(self):
        return list_get(self.obj_values, 1, default=None)
