#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: toml_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/5/25 5:19 下午
# History:
#=============================================================================
"""
import json
import toml
import pprint

print(json.dumps(toml.load("./test.toml"), indent=4))