#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: ShangChenHui
@file: ReadFiles.py 
@time: 17-12-12 下午3:26 
"""
import os
import hashlib


def ReadFiles(rootDir, level = 1):
    if level == 1:
        print rootDir
    for lists in os.listdir(rootDir):
        filepath = os.path.join(rootDir, lists)
        print '│  ' * (level - 1) + '│--' + lists
        if os.path.isdir(filepath):
            ReadFiles(filepath, level + 1)
        else:
            CalMD5(filepath)


def CalMD5(filepath):
    with open(filepath, "rb") as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()


rootDir = "/home/xiaohui/svn/Wifi/trunk/Codes/wifilz.pack"
ReadFiles(rootDir)