#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: cProfileTest.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/3/26 上午10:37
# History:
#=============================================================================
"""
import cProfile
from cProfile import Profile

import pstats
from pstats import Stats


def sum_func(n):
    total = 0
    for i in range(n):
        total += i
    return total


def test_a():
    sum_func(1000000)
    sum_func(20000000)


cProfile.run("test_a()")
