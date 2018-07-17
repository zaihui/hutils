# -*- coding: utf-8 -*-
#
# this module provides various validators
import uuid


def is_uuid(string):
    """ 检查字符串是不是合法的 UUID。validate if string is a valid uuid.
    Examples:
        >>> if is_uuid('wrong string'): ...

    Returns: bool
    """
    try:
        return bool(string and uuid.UUID(string).hex == string)
    except ValueError:
        return False


def is_int(string):
    """ 检查字符串是不是合法的 int. validate if string is a valid int.
    Examples:
        >>> if is_int('wrong string'): ...

    Returns: bool
    """
    try:
        return bool(int(string) or True)
    except ValueError:
        return False
