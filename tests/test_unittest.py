from unittest import TestCase

from hutils.unittest import TestCaseMixin


class HUtils:
    num = 10
    key = 'value'


class HUtilsTestCase(TestCase, TestCaseMixin):
    pass


class FuncTestCaseAPITests(HUtilsTestCase):

    def test_assert_increases(self):
        value = 10
        with self.assert_increases(5, lambda: value):
            value += 5

        obj = HUtils()
        with self.assert_increases(5, lambda: obj.num):
            obj.num += 5

    def test_assert_data(self):
        expected_data = {
            'dict': {
                'key': 'value',
            },
            'list': [{'key': 'value'}]
        }

        actual_data = {
            'count': 1,
            'dict': {
                'key': 'value',
                'value': 'key',
            },
            'list': [{'key': 'value'}]
        }
        self.assert_data(expected_data, actual_data)

    def test_assert_same(self):
        data = {'key': 'value'}
        self.assert_same(data, key='value')

        data = ['key', 'value']
        self.assert_same(data, _0='key', _1='value', length=2)

        data = {
            'nested': {
                'dict': {
                    'key': 'value',
                },
                'list': ['key', 'value'],
                'object': HUtils(),
                'bool_false': None,
                'bool_true': 'value',
            },
        }
        self.assert_same(
            data,
            nested__dict__key='value',
            nested__list__0='key',
            nested__list__1='value',
            nested__list__length=2,
            nested__object___key='value',
            nested__bool_false__bool=False,
            nested__bool_true__bool=True,
        )
