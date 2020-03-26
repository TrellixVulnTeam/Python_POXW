"""
@file: test_fixture_simple.py
@time: 2019/11/25
@author: alfons
"""
import unittest
from UnitTest.simple import *


# 导入模块时调用
def setUpModule():
    print("do something before test Module prepare")



def tearDownModule():
    print("do something after test Module clean up")


class TestSimple(unittest.TestCase):
    # 执行测试前调用
    def setUp(self):
        print("do something before test prepare")

    # 执行测试后调用
    def tearDown(self):
        print("do something after test clean up")

    # 测试类初始化前调用
    @classmethod
    def setUpClass(cls) -> None:
        print("do something before test class prepare")

    # 测试类初始化后调用
    @classmethod
    def tearDownClass(cls) -> None:
        print("do something after test class clean")

    def test_add(self):
        print("In add")
        self.assertEqual(4, add(1, 3))

    def test_minus(self):
        print("In minus")
        self.assertEqual(2, minus(3, 1))

    def test_multi(self):
        print("In multi")
        self.assertEqual(3, multi(3, 1))


if __name__ == '__main__':
    unittest.main()
