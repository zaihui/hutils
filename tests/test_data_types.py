# -*- coding: utf-8 -*-
import datetime
import decimal
import json
import unittest

import bson

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

    def test_format_json_with_pymongo(self):
        test_date = datetime.date(2006, 1, 2)
        test_datetime = datetime.datetime(2006, 1, 2, 15, 4, 5)
        chinese = '强哥'

        test_case = {
            'chinese': chinese,
            'date': test_date,
            'datetime': test_datetime,
            'decimal': decimal.Decimal('3.14'),
            'bson_decimal': bson.Decimal128('0.01'),
        }
        expected = {
            'chinese': '强哥',
            'date': '2006-01-02',
            'datetime': '2006-01-02 15:04:05',
            'decimal': '3.14',
            'bson_decimal': '0.01',
        }
        result = hutils.data_types.format_json(test_case)
        self.assertDictEqual(json.loads(result), expected)

        # Test ensure_ascii
        ascii = chinese.encode('unicode-escape').decode()
        result = hutils.data_types.format_json(test_case,
                                               ensure_ascii=True)
        self.assertIn(ascii, result)

        # Test json options
        sorted_result = hutils.data_types.format_json(test_case,
                                                      sort_keys=True)
        sorted_expected = json.dumps(expected,
                                     ensure_ascii=False,
                                     sort_keys=True)
        self.assertEqual(sorted_result, sorted_expected)
