# -*- coding: utf-8 -*-
import logging
import unittest

import hutils


class DecoratorTests(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_obj_cache(self):
        class Sample:

            def __init__(self):
                self.counter = 0

            @property
            @hutils.obj_cache('_value')
            def value(self):
                self.counter += 1
                return self.counter

        a = Sample()
        self.assertEqual(1, a.value)
        self.assertEqual(1, a.value)

        b = Sample()
        self.assertEqual(1, b.value)
        self.assertEqual(1, b.counter)

    def test_context_manager(self):
        with self.assertRaises(IOError), hutils.catches(ValueError, TypeError, raises=IOError()):
            raise ValueError('should wrap this error')
        with self.assertRaises(IOError), hutils.catches(ValueError, TypeError, raises=lambda x: IOError(str(x))):
            raise TypeError('should wrap this error')

    def test_decorator(self):
        @hutils.catches(ValueError, raises=IOError(), log=True)
        def raise_io_error():
            raise ValueError('should wrap this error')

        with self.assertRaises(IOError):
            raise_io_error()
