#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Popen.py
@time: 18-6-20 下午9:58
@version: v1.0 
"""
import datetime
from subprocess import call, Popen

print("Start time {time}.".format(time=datetime.datetime.now()))

prog = Popen("sleep 3; touch popen.txt", shell=True)
print("Popen finish time {time}.".format(time=datetime.datetime.now()))

call("sleep 3; touch call.txt", shell=True)
print("call finish time {time}.".format(time=datetime.datetime.now()))
