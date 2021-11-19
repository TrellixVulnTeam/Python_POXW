#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: execute_sequence_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/4/25 2:13 下午
# History:
#=============================================================================
"""


def func_a(func):
    print("func_a")
    return func


def func_b(func):
    print("func_b")
    return func


@func_a
@func_b
def func_exe():
    print("This is true")


func_exe()
