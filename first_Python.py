#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: print_max.py 
@time: 2017/4/24 16:52 
@version: v1.0 
"""

print("hell sa")
i = 4 + 1
print(i)
print("{name} is find {client}".format(name = 'Alfons', client = "dota2"))
print("{0:.3}".format(10.0 / 3))
print("{0:.^13}".format('hello'))
print(not 0)

# NEW LINE,Function Logic()
print("NEW Function----Logic:")
import Logic_Function

Logic_Function.Logic()
print("")

# NEW LINE,Function print_max()
print("NEW Function----print_max:")
import print_max

print_max.print_max(4, 5)
print_max.print_max(5, 4)
print_max.print_max(4, 4)
print("")

# NEW LINE,Function tuple
from Tuple import tuple

print(tuple(3, 1, 2, 3, alfons = 12, aal = 32))
print tuple.__name__
print tuple.__doc__
print('')

# NEW LINE,Function DataStruct
import DataStructers
print ("{0:_^64}".format("DataStructers.list_func()"))
DataStructers.list_func()
print ("{0:_^64}".format("DataStructers.tuple_func()"))
DataStructers.tuple_func()
print ("{0:_^64}".format("DataStructers.dictionary_func()"))
DataStructers.dictionary_func()
print ("{0:_^64}".format("DataStructers.seq_function()"))
DataStructers.seq_function()