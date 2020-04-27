# -*- coding: utf-8 -*-
import contextlib
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


@contextlib.contextmanager
def mutes(*exceptions, returns=None, logger=None):
    """ 出错时保持沉默，返回普通值。mute exception

    Examples::

        @mutes(returns=42)
        def get_answer(a, b):
            return a + b
    """

    exceptions = exceptions or (Exception,)

    try:
        yield
    except exceptions as ex:
        if logger:
            log_error(logger, ex)
        return returns
