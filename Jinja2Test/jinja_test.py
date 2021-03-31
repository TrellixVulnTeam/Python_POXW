#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: jinja_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/2/22 5:24 下午
# History:
#=============================================================================
"""
import pathlib
import jinja2

temp = jinja2.Template(pathlib.Path('./drbd.res.template').read_text())
print(temp.render(drbd_resource="fdasfasd"))
pass