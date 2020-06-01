# -*- coding: utf-8 -*-
import contextlib
import functools as fn
from typing import Callable, Union

from hutils.shortcuts import log_error


@contextlib.contextmanager
def catches(*exceptions, raises: Union[BaseException, Callable[[Exception], BaseException]], logger=None):
    """ 封装转换错误类。transfer exceptions to a different type.

    Examples::

        with self.assertRaises(IOError), catches(ValueError, TypeError, raises=IOError()):
            raise ValueError('should wrap this error')

        @catches(raises=get_validation_error, log=True)
        def raise_io_error():
            raise ValueError('should wrap this error')
    """
    exceptions = exceptions or (Exception,)
    try:
        yield
    except exceptions as ex:
        if callable(raises):
            raises = raises(ex)
        if logger:
            log_error(logger, raises)
        raise raises from ex


class mutes:
    """ 出错时保持沉默，返回普通值。mute exception

    Examples::

        @mutes(returns=42)
        def get_answer(a, b):
            return a + b
    """

    def __init__(self, *exceptions, returns=None, logger=None):
        self.exceptions = exceptions or (Exception,)
        self.returns = returns
        self.logger = logger

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any([exc for exc in self.exceptions if isinstance(exc_val, exc)]):
            if self.logger:
                log_error(self.logger, exc_val)
            return True
        return False

    def __call__(self, func):
        @fn.wraps(func)
        def wrapper(*args, **kwargs):
            value = self.returns
            with self:
                value = func(*args, **kwargs)
            return value

        return wrapper
