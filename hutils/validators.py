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
