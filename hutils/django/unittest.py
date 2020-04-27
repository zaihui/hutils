import json
import math

from django.db.backends.signals import connection_created
from django.dispatch import receiver


def extend_django_sqlite():
    """ 给 django sqlite 补上一些基础函数 """

    def float_max(value_x, value_y):
        return float(max(float(value_x), float(value_y)))

    def json_contains(column_value, value):
        return json.loads(value) in json.loads(column_value)

    def json_extract(value, path):
        data = json.loads(value)
        keys = path[2:].split(".")
        result = data
        for key in keys:
            if isinstance(result, dict):
                result = result.get(key)
            else:
                result = None
        return result

    @receiver(connection_created)
    def extend_sqlite(connection=None, **_):
        if not connection or connection.vendor != "sqlite":
            return
        create_function = connection.connection.create_function
        create_function("POW", 2, pow)
        create_function("SQRT", 1, math.sqrt)
        create_function("COS", 1, math.cos)
        create_function("SIN", 1, math.sin)
        create_function("ATAN2", 2, math.atan2)
        create_function("RADIANS", 1, math.radians)
        create_function("MAX", 2, float_max)
        create_function("GREATEST", 2, max)
        create_function("FLOOR", 1, math.floor)
        create_function("JSON_CONTAINS", 2, json_contains)
        create_function("JSON_EXTRACT", 2, json_extract)
