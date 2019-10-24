"""
@file: re_test.py
@time: 2019/10/9
@author: alfons
"""
import re

# 获取版本号
with open("qdata_version.conf", 'r') as f:
    codes_str = f.read()

pattern = re.compile(r'[.\n]*VERSION = "([\d.]+)".*')
result = pattern.match(codes_str)
r = result.group(2)
print(r)
pass