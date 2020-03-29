#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: __init__.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/2/21 下午3:27
# History:
#=============================================================================
"""
import datetime
from celery import Celery

app = Celery("test", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@app.task
def print_test():
    print datetime.datetime.now()