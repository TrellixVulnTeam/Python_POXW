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
import os
os.execv()
import sys
sys.exit()
import socket
print(socket.getprotobyname('tcp'))


from dateutil.parser import parse

r = parse("1622597224")
print(r)

import time
from datetime import datetime
print(datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
pass
