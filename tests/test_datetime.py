# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import datetime
import unittest

import hutils


class DateTimeTests(unittest.TestCase):

    @hutils.fake_time('2017-01-01 08:00:00')
    def test_decorator(self):
        self.assertEqual(datetime.datetime(2017, 1, 1, 8, 0, 0), datetime.datetime.now())

    def test_context_manager(self):
        with hutils.fake_time('2017-01-01 08:00:00'):
            self.assertEqual(datetime.datetime(2017, 1, 1, 8, 0, 0), datetime.datetime.now())
