import contextlib
import datetime
import socket
import time
from unittest import mock

from hutils.shortcuts import str_to_datetime


def get_disable_migration_module():
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

        def __getattr__(self, item):
            raise Exception('Network through socket is disabled!')

    socket.socket = DisableNetwork


class MockDateTime(datetime.datetime):
    """ class for mocking datetime.datetime """

    @classmethod
    def now(cls, tz=None):
        return cls.today()

    def __sub__(self, other):
        result = super(MockDateTime, self).__sub__(other)
        if hasattr(result, 'timetuple'):
            return MockDateTime.fromtimestamp(time.mktime(result.timetuple()))
        return result


class Mogician:
    """ class for mocking any time """

    @staticmethod
    def mock_field_default(field):
        from django.db import DefaultConnectionProxy

        if field.has_default():
            if callable(field.default):
                if field.default.__name__ == 'now':
                    return datetime.datetime.now()
                return field.default()
            return field.default
        if not field.empty_strings_allowed or \
                (field.null and not DefaultConnectionProxy().features.interprets_empty_strings_as_nulls):
            return None
        return ''

    def __init__(self, fake_to):
        self.the_datetime = fake_to if isinstance(fake_to, datetime.datetime) else str_to_datetime(fake_to)
        self.patchers = [
            mock.patch('time.time', lambda: time.mktime(self.the_datetime.timetuple())),
            mock.patch('datetime.datetime', MockDateTime),
            mock.patch('django.utils.timezone.now', MockDateTime.now),
        ]
        try:
            import django  # NOQA

            self.patchers.append(mock.patch('django.db.models.fields.Field.get_default', Mogician.mock_field_default))
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
