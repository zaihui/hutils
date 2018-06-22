# -*- coding: utf-8 -*-
import unittest

import hutils


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
            res = hutils.data_types.get_data(data, *keys, optional=optional)
            self.assertListEqual(list(res), expect)

    def test_get_data_sample(self):
        data = {
            'offset': 0,
            'limit': 20,
            'from': 'yesterday',
            'to': 'today'
        }
        offset, limit, begin, end = hutils.get_data(data, 'offset', 'limit', 'from', 'to')
        self.assertEqual(offset, 0)
        self.assertEqual(limit, 20)
        self.assertEqual(begin, 'yesterday')
        self.assertEqual(end, 'today')
