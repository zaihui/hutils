# -*- coding: utf-8 -*-
import unittest

import hutils


class DecoratorTests(unittest.TestCase):
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
