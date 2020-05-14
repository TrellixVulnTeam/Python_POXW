#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: test_func.py
@time: 2020/4/12 上午11:38
@version: v1.0 
"""
import sys


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib_seq(n):
    seq = []
    if n > 0:
        seq.extend(fib_seq(n - 1))
    seq.append(fib(n))
    return seq


if __name__ == '__main__':
    # print(fib_seq(int(sys.argv[1])))
    print(fib_seq(20))