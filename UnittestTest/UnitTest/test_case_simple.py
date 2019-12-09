"""
@file: test_simple.py
@time: 2019/11/25
@author: alfons
"""
import unittest
from UnitTest.simple import *


class TestSimple(unittest.TestCase):
    def test_add(self):
        self.assertEqual(3, add(1, 2))

    def test_minus(self):
        self.assertEqual(1, minus(3, 2))
        self.assertNotEqual(1, minus(4, 2))


if __name__ == '__main__':
    unittest.main()
