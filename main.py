#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
list_a = ["1_0", "1_1", "1_2"]
list_b = ["2_0", "2_1", "2_2"]
list_c = list()
[list_c.append([a, b]) for a in list_a for b in list_b]
print list_c

from collections import defaultdict

dict_a = defaultdict(list)
pass

list_a = ["bo", "ao"]
str_a = str(list_a)
print ','.join(set(list_a))
pass
