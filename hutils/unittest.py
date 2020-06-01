import contextlib
import datetime
import os
import socket
import time
from collections.abc import Callable
from http import HTTPStatus
from unittest import mock

from hutils.shortcuts import str_to_datetime


def disable_migration():
    """ get disable migration """

    class DisableMigration:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    return DisableMigration()


def disable_network():
    """ Disable network """

    class DisableNetwork:
        def __init__(self, *args, **kwargs):
            raise Exception("Network through socket is disabled!")

        def __call__(self, *args, **kwargs):
            raise Exception("Network through socket is disabled!")

    real_socket = socket.socket
    socket.socket = DisableNetwork
    patcher = mock.patch("asyncio.selector_events.socket.socket", real_socket)
    patcher.start()

    return patcher


def disable_elastic_apm():
    """ disable elastic apm """
    os.environ["ELASTIC_APM_DISABLE_SEND"] = "true"
    os.environ["ELASTIC_APM_CENTRAL_CONFIG"] = "false"


class MockDateTime(datetime.datetime):
    """ class for mocking datetime.datetime """

    @classmethod
    def now(cls, tz=None):
        return cls.today()

    def __sub__(self, other):
        result = super(MockDateTime, self).__sub__(other)
        if hasattr(result, "timetuple"):
            return MockDateTime.fromtimestamp(time.mktime(result.timetuple()))
        return result


class Mogician:
    """ class for mocking any time """

    @staticmethod
    def mock_field_default(field):
        from django.db import DefaultConnectionProxy

        if field.has_default():
            if callable(field.default):
                if field.default.__name__ == "now":
                    return datetime.datetime.now()
                return field.default()
            return field.default
        if not field.empty_strings_allowed or (
            field.null and not DefaultConnectionProxy().features.interprets_empty_strings_as_nulls
        ):
            return None
        return ""

    def __init__(self, fake_to):
        self.the_datetime = fake_to if isinstance(fake_to, datetime.datetime) else str_to_datetime(fake_to)
        self.patchers = [
            mock.patch("datetime.datetime", MockDateTime),
            mock.patch("time.localtime", lambda: time.struct_time(self.the_datetime.timetuple())),
            mock.patch("time.time", lambda: time.mktime(self.the_datetime.timetuple())),
        ]
        try:
            import django  # NOQA

            self.patchers.extend(
                [
                    mock.patch("django.db.models.fields.Field.get_default", Mogician.mock_field_default),
                    mock.patch("django.utils.timezone.now", MockDateTime.now),
                ]
            )
        except ImportError:
            pass

    def __enter__(self):
        for patcher in self.patchers:
            patcher.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for patcher in self.patchers:
            patcher.stop()


@contextlib.contextmanager
def fake_time(fake_to):
    """ short cut for mocking time or datetime, supports django.

    Examples::

        @fake_time('2018-08-08 12:00:00')
        def test_something_related_to_datetime(self):
            pass

    :type fake_to: str | datetime.datetime
    """
    with Mogician(fake_to):
        yield


class TestCaseMixin:
    """
    增加一些便于测试的小方法的 Mixin

    Examples:

        from rest_framework.test import APITestCase

        class TestCase(APITestCase, TestCaseMixin):
            pass

        class ExampleTest(TestCase):

            def test_something(self):
                response = self.client.get(url)
                self.ok(response)

    For details, see <tests.test_unittest.FuncTestCaseAPITests>
    """

    def ok(self, response, *, is_201=False, is_204=False, **kwargs):
        """ shortcuts to response 20X """
        expected = (is_201 and HTTPStatus.CREATED) or (is_204 and HTTPStatus.NO_CONTENT) or HTTPStatus.OK
        self.assertEqual(
            expected,
            response.status_code,
            "status code should be {}: {}".format(expected, getattr(response, "data", "")),
        )
        if kwargs:
            self.assert_same(response.data, **kwargs)
        return self

    def bad_request(self, response, **kwargs):
        """ shortcuts to response 400 """
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code, "status code should be 400")
        if kwargs:
            self.assert_same(response.data, **kwargs)
        return self

    def not_found(self, response):
        """ shortcuts to response 404 """
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        return self

    def forbidden(self, response, **kwargs):
        """ shortcuts to response 403 """
        self.assertEqual(HTTPStatus.FORBIDDEN, response.status_code, "status code should be 403")
        if kwargs:
            self.assert_same(response.data, **kwargs)
        return self

    def assert_increases(self, delta: int, func: Callable, name=""):
        """ shortcuts to verify func change is equal to delta """
        test_case = self

        class Detector:
            def __init__(self):
                self.previous = None

            def __enter__(self):
                self.previous = func()

            def __exit__(self, exc_type, exc_val, exc_tb):
                if not exc_val:
                    test_case.assertEqual(
                        self.previous + delta, func(), "{} should change {}".format(name, delta).strip()
                    )

        return Detector()

    def assert_model_increases(self, *models, delta: int = 1, **lookups):
        """ shortcuts to verify value change """
        stack = contextlib.ExitStack()
        for case in models:
            if isinstance(case, tuple):
                model, delta = case
            else:
                model, delta = case, 1
            stack.enter_context(self.assert_increases(delta, model.all_objects.filter(**lookups).count, model.__name__))
        return stack

    def assert_same(self, data, **expects):
        """ shortcuts to compare value (support nested dictionaries, lists and array length) """

        def _get_key(_data, _key: str):
            """ get the expanded value """
            _value = _data
            for part in _key.split("__"):
                if part == "length":
                    _value = len(_value)
                elif part == "bool":
                    _value = bool(_value)
                elif part.startswith("_"):
                    try:
                        _value = _value[int(part[1:])]
                    except ValueError:
                        _value = getattr(_value, part[1:])
                else:
                    try:
                        _value = _value[int(part)]
                    except ValueError:
                        _value = _value[part]
            return _value

        for key, expect in expects.items():
            actual = _get_key(data, key)
            try:
                self.assertEqual(
                    expect,
                    actual,
                    "{} value not match.\nExpect: {} ({})\nActual: {} ({})".format(
                        key, expect, type(expect), actual, type(actual)
                    ),
                )
            except Exception:
                print("\nAssertionError:")
                print("Actual: {}".format(data))
                print("Expect: {}".format(expects))
                raise
        return self

    def assert_data(self, expected_data, actual_data):
        """ shortcuts to compare data (expected_data can be subset of actual_data) """

        if isinstance(expected_data, list):
            data = list(actual_data)
            self.assertEqual(len(expected_data), len(data))
            for index, item in enumerate(expected_data):
                self.assert_data(item, data[index])
        elif isinstance(expected_data, dict):
            for k, v in expected_data.items():
                self.assertTrue(k in actual_data, msg="{} not in actual_data".format(k))
                self.assert_data(v, actual_data[k])
        else:
            self.assertEqual(expected_data, actual_data)
        return self
