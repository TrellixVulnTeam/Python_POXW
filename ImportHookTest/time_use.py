#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: time_use.py
@time: 2020/4/14
@author: alfons
"""
with open("./time_use.txt", "r") as f:
    print "Total time use {}'s.".format(sum([float(line[line.rfind(':') + 2: line.rfind('\'')]) for line in f.readlines()]))
