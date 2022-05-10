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
        self.assertTrue(hutils.is_int("-1"))
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

    def test_telephone_success(self):
        self.assertTrue(hutils.is_telephone("0510-85858999"))

    def test_telephone_success_2(self):
        telephone = "010-85858909"
        self.assertTrue(hutils.is_telephone(telephone))

    def test_telephone_too_long(self):
        telephone = "0511-858589991"
        self.assertFalse(hutils.is_telephone(telephone))

    def test_telephone_too_long_2(self):
        telephone = "051-8585899911"
        self.assertFalse(hutils.is_telephone(telephone))

    def test_telephone_too_long_prefix(self):
        telephone = "05111-858589991"
        self.assertFalse(hutils.is_telephone(telephone))

    def test_telephone_too_short_prefix(self):
        telephone = "01-85858999"
        self.assertFalse(hutils.is_telephone(telephone))

    def test_telephone_too_short_end(self):
        telephone = "010-858589"
        self.assertFalse(hutils.is_telephone(telephone))

    def test_telephone_too_long_end(self):
        telephone = "010-858589111"
        self.assertFalse(hutils.is_telephone(telephone))
