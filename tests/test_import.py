# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import unittest


class ImportTests(unittest.TestCase):
    def test_import(self):
        import hutils

        self.assertTrue(hutils)
