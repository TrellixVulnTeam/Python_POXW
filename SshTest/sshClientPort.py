#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: sshClientPort.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2019/10/28 下午6:31
# History:
#=============================================================================
"""
import re
import os

port = "2234342"
with open("/etc/services", 'r') as f:
    st = f.read()

p = re.sub(r"ssh\s*\d+/tcp", "ssh\t\t{p}/tcp".format(p=port), st, count=1, flags=re.M | re.I)
if p == st:
    print True
else:
    os.system("echo \"{str}\" > {file}".format(str=p.replace("\"", " "), file="/etc/services"))
pass
