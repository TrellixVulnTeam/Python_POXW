#!/usr/bin/env python
# encoding: utf-8
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : soft_list_parser.py
 @Time    : 2019/3/26 10:01
"""
import io
import sys
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import json

soft_sum = dict()

with open("./soft_list.txt", 'r', encoding="utf-8") as f:
    for soft in f.readlines():
        soft_name = soft.split('-', maxsplit=2)[0].strip()
        if "腾讯bugly包名" in soft_name or "mopub包名" in soft_name or soft_name.startswith("安卓"):
            continue

        if soft_name in soft_sum:
            soft_sum[soft_name] += 1
        else:
            soft_sum[soft_name] = 1
soft_sum = {k: v for k, v in sorted(soft_sum.items(), key=lambda item: item[1], reverse=True) if v > 100}

with open("soft_res.json", "wb") as f:
    res = json.dumps(list(soft_sum.keys()), indent=4, ensure_ascii=False).encode("gbk", "ignore")
    f.write(res)
