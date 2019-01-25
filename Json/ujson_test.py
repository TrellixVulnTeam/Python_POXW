"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ujson_test.py
@time: 19-1-25 下午10:49
@version: v1.0 
"""
import ujson
import json

d = dict()
d[1] = "h"

p = ujson.dumps(d)
print(type(p))
print(p)
