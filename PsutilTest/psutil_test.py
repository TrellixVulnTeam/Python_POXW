#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: psutil_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/5/13 3:56 下午
# History:
#=============================================================================
"""
import psutil


for p in psutil.process_iter():
    print(p.pid)
    print(p.name())
    print(p.status())