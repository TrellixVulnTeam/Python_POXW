#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: print_max.py 
@time: 2017/4/24 16:52 
@version: v1.0 
"""

def print_max(a, b):
    if a > b:
        print("{0} is maxnumber".format(a))
    elif a < b:
        print("{0} is maxnumber".format(b))
    else:
        print("{0} = {1}".format(a, b))
