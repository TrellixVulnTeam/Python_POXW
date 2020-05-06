#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: profile_lsprof.py
@time: 2020/4/19 上午10:30
@version: v1.0 
"""
import _lsprof
from test_func import fib_seq

profile = _lsprof.Profiler()
profile.enable()
fib_seq(30)
profile.disable()

res = profile.getstats()
print "\n".join([str(r) for r in res])