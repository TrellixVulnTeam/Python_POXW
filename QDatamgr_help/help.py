#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: help.py
@time: 2020/6/3
@author: alfons
"""
import os
import yaml

with open("./modules.yml", "r") as f:
    modules = yaml.load(f)
    for m in modules:
        os.system("source /home/sendoh/sendoh-dev-env/bin/activate && python /tmp/pycharm_project_789/src/main.py {} -h".format(m))
        pass