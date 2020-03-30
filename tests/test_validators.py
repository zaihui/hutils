# -*- coding: utf-8 -*-
import uuid
import logging
import unittest

import hutils


class ValidatorsTests(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_is_uuid(self):
        uid = uuid.uuid4().hex
        assert hutils.validators.is_uuid(uid) is True

        fake_uid = "php is the best..."
        assert hutils.validators.is_uuid(fake_uid) is False

    def test_is_int(self):
        assert hutils.validators.is_int("1") is True
        assert hutils.validators.is_int("a") is False

    def test_is_chinese_phone(self):
        assert hutils.validators.is_chinese_phone("17600001234") is True
        assert hutils.validators.is_chinese_phone("91234567") is False

    def test_is_singapore_phone(self):
        assert hutils.validators.is_singapore_phone("91234567") is True
        assert hutils.validators.is_singapore_phone("17600001234") is False

    def test_is_phone(self):
        assert hutils.validators.is_phone("91234567") is True
        assert hutils.validators.is_phone("17600001234") is True
        assert hutils.validators.is_phone("+85212345678") is False

