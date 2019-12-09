"""
@file: test_suite_simple.py
@time: 2019/11/25
@author: alfons
"""
import unittest
from UnitTest.test_case_simple import TestSimple

if __name__ == '__main__':
    suite = unittest.TestSuite()

    test_list = [
        TestSimple("test_add"),
        TestSimple("test_minus"),
    ]
    suite.addTests(test_list)

    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)

    with open("UnittestReport.txt", 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        runner.run(suite)
