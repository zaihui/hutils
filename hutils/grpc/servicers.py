import functools as fn

import grpc

from hutils import format_json


def register_servicer_command(func):
    @fn.wraps(func)
    def wrapper(request, context):
        from django.core.exceptions import ValidationError

        try:
            return func(request, context)
        except ValidationError as ex:
            details = ex.params or {}
            details["message"] = ex.message
            context.abort(ex.code or grpc.StatusCode.INVALID_ARGUMENT, format_json(details))

    return wrapper


class GrpcMetaclass(type):
    def __init__(cls, what, bases=None, attrs=None):
        super(GrpcMetaclass, cls).__init__(what, bases, attrs)

        for key in attrs.keys():
            if key[0].isupper():
                attrs[key] = register_servicer_command(attrs[key])
