#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: main36.py 
@time: 2017/12/28 17:28 
@version: v1.0 
"""
from array import array

nums = array("h", [-2, -1, 0, 1, 2])
print(nums)
mmv = memoryview(nums)
mmv[2] = 89
print(nums)
pass