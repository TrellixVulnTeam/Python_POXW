#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: test_hulk_high_connect.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/11/6 9:38 上午
# History:
#=============================================================================
"""
import time
import requests


def try_one(url):
    start = time.perf_counter()
    c = requests.get(url=url).content
    return time.perf_counter() - start


def try_more(url):
    max_time = 0
    while True:
        tmp_time = max(max_time, try_one(url=url) * 1000)
        if max_time != tmp_time:
            max_time = tmp_time
            print(f"{max_time=} ms")


try_more(
    url="http://127.0.0.1:11102/hulk/ai_ops/replace_disk/disk_group_info?cluster_id=3&disk_group=CHDGGGG&timestamp=1604142156603&sort_reverse=false&page=1&page_size=10")
