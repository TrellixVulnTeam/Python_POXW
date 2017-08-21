#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ReadAircrackDoc.py
@time: 2017/8/21 14:15
@version: v1.0
"""

import subprocess

doc_path = "func_list"

with open(doc_path, "r") as f:
    funcs_list = f.readlines()
    for func in funcs_list:
        func_name = func.split("(")[0].strip()
        func_num = func.split("(")[1].split(")")[0]
        cmd = "touch " + func_name + ".txt"
        subprocess.call(cmd, shell = True)
        cmd = "man " + func_num + " " + func_name + "> " + "/home/xiaohui/Desktop/" + func_name + ".txt"
        subprocess.call(cmd, shell = True)
        pass
