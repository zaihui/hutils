# -*- coding: utf-8 -*-
import unittest

from hutils import data_types


class TestDataTypes(unittest.TestCase):
    def test_get_data(self):
        test_cases = [
            ({}, False, [], []),
            ({
                'a': 1
            }, False, ['a'], [1]),
            ({
                'a': 1,
                'b': 2
            }, True, ['a', 'c'], [1, None]),
        ]
        for data, optional, keys, expect in test_cases:
            res = data_types.get_data(data, optional, *keys)
            self.assertListEqual(list(res), expect)
