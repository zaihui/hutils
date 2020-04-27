# -*- coding: utf-8 -*-
import logging
import unittest

import hutils


class DecoratorTests(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_context_manager(self):
        with self.assertRaises(IOError), hutils.catches(ValueError, TypeError, raises=IOError()):
            raise ValueError("should wrap this error")
        with self.assertRaises(IOError), hutils.catches(ValueError, TypeError, raises=lambda x: IOError(str(x))):
            raise TypeError("should wrap this error")

    def test_decorator(self):
        @hutils.catches(ValueError, raises=IOError(), logger=__name__)
        def raise_io_error():
            raise ValueError("should wrap this error")

        with self.assertRaises(IOError):
            raise_io_error()

    def test_mute(self):
        def value_error():
            raise ValueError()

        mute_value_error = hutils.mutes(ValueError)(value_error)
        mute_value_error()

        with hutils.mutes(ValueError):
            value_error()

        with self.assertRaises(ValueError), hutils.mutes(IOError):
            value_error()

        self.assertTrue(True)
