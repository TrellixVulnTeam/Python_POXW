#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: CollectionsDict.py 
@time: 2017/5/15 20:24 
@version: v1.0 
"""
# 内建模块collections
print ("\n{0:_^64}".format("Build-in mould:namedtuple"))
from collections import namedtuple

cricle = namedtuple('cricle', ['x', 'y', 'r'])
cricleA = cricle(1, 2, 3)
x, y, z = cricleA
print type(cricleA)
print cricleA

print ("\n{0:_^64}".format("Build-in mould:deque"))
from collections import deque

dequeA = deque(maxlen = 12)
dequeA.append('x')
dequeA.appendleft('z')
dequeA.append('y')
print dequeA
dequeA.reverse()
print dequeA
dequeA.remove('x')
dequeA.pop()
dequeA.popleft()
dequeA.append('shd')
dequeA.clear()
print(dequeA.maxlen)
pass

print ("\n{0:_^64}".format("Build-in mould:defaultdict"))
# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict
from collections import defaultdict

dictB = defaultdict(lambda: "N.A.A")
dictB['key1'] = 'abc'
print dictB['key1']  # key1存在
print dictB['key2']  # key2不存在，返回默认值
print dictB.default_factory()

print ("\n{0:_^64}".format("Build-in mould:OrderedDict"))
# 注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序：
from collections import OrderedDict

orderDictA = OrderedDict()
orderDictA[1] = "sd"
orderDictA[2] = "sb"
orderDictA[5] = "ssd"
orderDictA[4] = "sssss"
orderDictA[3] = 1
pass
