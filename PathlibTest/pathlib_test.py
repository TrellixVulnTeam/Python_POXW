#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: pathlib_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/1/5 9:49 AM
# History:
#=============================================================================
"""
import pathlib

a_file = pathlib.Path("/test/test_a")
a_file.parent.mkdir(parents=True, exist_ok=True)    # 创建父文件夹
a_file.write_text("xxxxx")      # 写入文件内容
