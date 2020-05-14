#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: special_func.py
@time: 2020/4/12 上午10:03
@version: v1.0 
"""
# import profile
import cProfile
from test_func import fib_seq

profile = cProfile.Profile()
profile.enable()
fib_seq(30)
profile.disable()

# profile.print_stats()
profile.dump_stats("fib.prof")

import pstats

p = pstats.Stats(profile)

print('print_stats("fib", 0.5)'.center(64, '='))
p.sort_stats("cumu").print_stats("fib", 0.5)

print('print_stats(0.5, "fib")'.center(64, '='))
p.sort_stats("cumu").print_stats(0.5, "fib")
# p.sort_stats("cumu").print_line("fib_seq")
