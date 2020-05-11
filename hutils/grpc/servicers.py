import functools as fn

import grpc
from django.core.exceptions import ValidationError

from hutils import format_json


def register_servicer_command(func):
    @fn.wraps(func)
    def wrapper(request, context):
        try:
            return func(request, context)
        except ValidationError as ex:
            details = ex.params or {}
            details["message"] = ex.message
            context.abort(ex.code or grpc.StatusCode.INVALID_ARGUMENT, format_json(details))

    return wrapper


class GrpcMetaclass(type):
    def __new__(mcs, what, bases, attrs):
        for key in attrs.keys():
            if key[0].isupper():
                attrs[key] = register_servicer_command(attrs[key])
        return super(GrpcMetaclass, mcs).__new__(mcs, what, bases, attrs)
