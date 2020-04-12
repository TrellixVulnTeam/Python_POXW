#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: special_func.py
@time: 2020/4/12 上午10:03
@version: v1.0 
"""
import cProfile
import pstats
from test_func import fib_seq

profile = cProfile.Profile()
profile.enable()
fib_seq(30)
profile.disable()
profile.print_stats()

# ps = pstats.Stats()
