# -*- coding: utf-8 -*-
#
# this module provides various validators
import re
import uuid


def is_uuid(string):
    """ 检查字符串是不是合法的 UUID。validate if string is a valid uuid.

    Examples::

        if is_uuid('wrong string'): ...

    :rtype: bool
    """
    try:
        return bool(string and uuid.UUID(string).hex == string)
    except ValueError:
        return False


def is_int(string):
    """ 检查字符串是不是合法的 int. validate if string is a valid int.

    Examples::

        if is_int('wrong string'): ...

    :rtype: bool
    """
    try:
        int(string)
        return True
    except ValueError:
        return False


CHINESE_PHONE_REGEX = re.compile(r'^1[3-9][0-9]{9}$')


def is_chinese_phone(string):
    """ 检查字符串是不是合法的大陆手机号。validate if string is a valid chinese mainland phone number.

    Examples::

        if is_chinese_phone('12345678910'): ...

    :rtype: bool
    """
    return bool(CHINESE_PHONE_REGEX.match(string))
