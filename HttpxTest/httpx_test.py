#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: httpx_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/2/3 11:17 上午
# History:
#=============================================================================
"""
import httpx

res = httpx.post(url="http://10.10.100.220:11112/api/v1/media/raid/attach",
                 json=dict(slots=["P0B00S09", "P0B00S08"]))
pass
