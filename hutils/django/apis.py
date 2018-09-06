# -*- coding: utf-8 -*-
#
# this module provides django rest framework related methods
from django.db import models

from hutils.shortcuts import list_first


def get_validation_error(message: str, data=None, code=None):
    """ 方便快捷抛 400 的函数。shortcut for raising bad request error in django-rest-framework.

    Examples::

        raise get_validation_error('非法的请求')

    :rtype: rest_framework.exceptions.ValidationError
    """
    from rest_framework.exceptions import ValidationError

    error = {'message': message}
    if data is not None:
        error['data'] = data
    if code is not None:
        error['code'] = code
    return ValidationError(error)


def get_object_or_not_found(
        cls, *queries, _select_models=(), _prefetch_models=(), _err_msg=None, _err_func=get_validation_error, **kwargs):
    """ 类似 get_object_or_404。similar to get_object_or_404.

    Examples::
        user = get_object_or_not_found(User, uid=uid)

    :type cls: (() -> T) | T
    :type queries: django.db.models.query_utils.Q
    :type _select_models: tuple
    :type _prefetch_models: tuple
    :type _err_func: method
    :type _err_msg: str
    :rtype: T
    """
    manager = list_first(queries)
    if not isinstance(manager, models.Manager):
        manager = cls.objects
    try:
        result = manager.filter(*queries).select_related(*_select_models).prefetch_related(*_prefetch_models) \
            .get(**kwargs)
    except (cls.DoesNotExist, ValueError):  # 找不到，或者uid格式错误
        raise _err_func(_err_msg or '{} 不存在'.format(cls.__name__))
    return result
