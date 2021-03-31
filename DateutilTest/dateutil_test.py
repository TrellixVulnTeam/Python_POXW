#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: dateutil_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/1/14 4:12 下午
# History:
#=============================================================================
"""
from dateutil.parser import parse

r = parse("06-08-2020 01:56:33 AM").timestamp()
print(r)

import time
from datetime import datetime
print(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
pass
