#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: groupby_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/5/18 18:15
# History:
#=============================================================================
"""
from operator import attrgetter
from itertools import groupby

from pydantic import BaseModel


class TestModel(BaseModel):
    name: str
    age: int


l_1 = [
    TestModel(name="a", age=12),
    TestModel(name="b", age=12),
]

d_a = dict(groupby(l_1, key=attrgetter("name")))
print(d_a)

for k, value in groupby(l_1, key=attrgetter("name")):
    print(k, list(value))
