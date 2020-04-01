# -*- coding: utf-8 -*-
import logging
import unittest
import uuid

import hutils


class ValidatorsTests(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_is_uuid(self):
        uid = uuid.uuid4().hex
        self.assertTrue(hutils.is_uuid(uid))

        fake_uid = "php is the best..."
        self.assertFalse(hutils.is_uuid(fake_uid))

    def test_is_int(self):
        self.assertTrue(hutils.is_int("1"))
        self.assertFalse(hutils.is_int("a"))

    def test_is_chinese_phone(self):
        self.assertTrue(hutils.is_chinese_phone("17600001234"))
        self.assertFalse(hutils.is_chinese_phone("91234567"))

    def test_is_singapore_phone(self):
        self.assertTrue(hutils.is_singapore_phone("91234567"))
        self.assertFalse(hutils.is_singapore_phone("17600001234"))

    def test_is_phone(self):
        self.assertTrue(hutils.is_phone("91234567"))
        self.assertTrue(hutils.is_phone("17600001234"))
        self.assertFalse(hutils.is_phone("+85212345678"))
