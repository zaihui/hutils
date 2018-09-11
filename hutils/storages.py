# -*- coding: utf-8 -*-
import functools


def obj_cache(key):
    """ 使用对象的属性来充当方法缓存。use object attribute as cache.

    Examples::

        class A:
            @obj_cache('_value')
            def get_value(self, *args):
                ...

    :type key: str
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(obj, *args, **kwargs):
            if hasattr(obj, key):
                return getattr(obj, key)
            value = func(obj, *args, **kwargs)
            setattr(obj, key, value)
            return value

        return wrapper

    return decorator
