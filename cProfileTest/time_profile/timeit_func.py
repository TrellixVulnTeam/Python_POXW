#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: timeit_func.py
@time: 2020/4/12 上午11:47
@version: v1.0 
"""
import timeit
from test_func import fib_seq


def test_code():
    fib_seq(30)


# res = timeit.repeat(test_code, number=1, repeat=5)
res = timeit.timeit(test_code, number=1)
print "timeit use -> {}'s.".format(res)

import time

start_time = time.time()
fib_seq(30)
print "time use -> {}'s.".format(time.time() - start_time)
