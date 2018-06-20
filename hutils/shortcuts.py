# -*- coding: utf-8 -*-
#
# this module provides various one liners
from __future__ import absolute_import, unicode_literals


def get_uid(instance):
    """ 获取实例的 uid (hex). get hex uid from instance.

    Example:
    Before:
        data = {
            'uid': instance.uid.hex if instance else None,
            'related_uid': instance.related.uid.hex if instance.related else None,
        }
    After:
        data = {
            'uid': get_uid(instance),
            'related_uid': get_uid(instance.related),
        }

    :rtype: str | None
    """
    return instance.uid.hex if instance else None
