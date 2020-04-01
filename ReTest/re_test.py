#!/usr/bin/env python
# encoding: utf-8
"""
@file: re_test.py
@time: 2019/10/9
@author: alfons
"""
import re

part_name = "P0B00S01p1"
p = re.match(r"(.*)p([\d])*", part_name)
res_1 = p.group(1)
res_2 = p.group(2)

p = re.search(r".*?drbd([0-9]*)", "/dev/drbd1002")
res = p.group(1)

lun_path = "/dv/qdisk/LUN102"
lun_number = int(re.search(r".*?LUN([\d]*)", lun_path).group(1))
port_number = 3260 + lun_number


# # 获取版本号
# with open("qdata_version.conf", 'r') as f:
#     codes_str = f.read()
#
# pattern = re.compile(r'[.\n]*VERSION = "([\d.]+)".*')
# result = pattern.match(codes_str)
# r = result.group(2)
# print(r)
pass