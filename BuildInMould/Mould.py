#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Mould.py 
@time: 2017/5/15 20:24 
@version: v1.0 
"""
#内建模块collections
print ("\n{0:_^64}".format("Build-in mould:namedtuple"))
from collections import namedtuple

cricle = namedtuple('cricle', ['x', 'y', 'r'])
cricleA = cricle(1, 2, 3)
print cricleA

print ("\n{0:_^64}".format("Build-in mould:deque"))
from collections import deque

q = deque([])