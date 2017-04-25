#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: main.py 
@time: 2017/4/25 11:40 
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
from Function import Logic_Function

Logic_Function.Logic()
print("")

# NEW LINE,Function print_max()
print("NEW Function----print_max:")
from Function import print_max

print_max.print_max(4, 5)
print_max.print_max(5, 4)
print_max.print_max(4, 4)
print("")

# NEW LINE,Function tuple
from Function.Tuple import print_tuple

print(print_tuple(3, 1, 2, 3, alfons = 12, aal = 32))
print print_tuple.__name__
print print_tuple.__doc__
print('')

# NEW LINE,Function DataStruct
from Function import DataStructers

print ("{0:_^64}".format("DataStructers.list_func()"))
DataStructers.list_func()
print ("\n{0:_^64}".format("DataStructers.tuple_func()"))
DataStructers.tuple_func()
print ("\n{0:_^64}".format("DataStructers.dictionary_func()"))
DataStructers.dictionary_func()
print ("\n{0:_^64}".format("DataStructers.seq_function()"))
DataStructers.seq_function()

# NEW LINE,Class iPhone
from iPhone.CiPhone import iPhone_v

print ("\n{0:_^64}".format("class iPhone_v"))
iPhone_3G = iPhone_v("iPhone_3G")
iPhone_3G.say_hi()
iPhone_v.how_many()
print ""

iPhone_4s = iPhone_v("iPhone_4s")
iPhone_4s.say_hi()
iPhone_v.how_many()
print ""

iPhone_3G.recycle()
iPhone_4s.recycle()
iPhone_v.how_many()

# NEW LINE,Class Animal
from Animal.animal import *

print ("\n{0:_^64}".format("class Animal"))
bird = bird("鹦鹉", "jugle", "can")
bird.live()

dog = dog("哈士奇", "home", "maybe")
dog.live()

print ""
animals = [bird, dog]
for animal in animals:
    animal.live()

# NEW LINE,File_func
from Function.io import io_using_file

print ("\n{0:_^64}".format("File_func"))
io_using_file.file_w_r()

