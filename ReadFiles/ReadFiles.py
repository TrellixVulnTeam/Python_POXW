#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: ShangChenHui
@file: ReadFiles.py 
@time: 17-12-12 下午3:26 
"""
import os
import hashlib


def ReadFiles(rootDir, level = 1, file_dict = {}):
    if level == 1:
        print(rootDir)
    for lists in os.listdir(rootDir):
        filepath = os.path.join(rootDir, lists)
        # print '│  ' * (level - 1) + '│--' + lists
        print(filepath)
        md5 = ""
        if os.path.isdir(filepath):
            ReadFiles(filepath, level + 1, file_dict)
        else:
            md5 = CalMD5(filepath)
        file_dict.update({filepath: md5})


def CalMD5(filepath):
    with open(filepath, "rb") as f:
        m = hashlib.md5()
        m.update(f.read())
        return m.hexdigest()


if __name__ == "__main__":
    rootDir = "D:/svn\Wifi/trunk/Codes/wifilz.pack"
    files_dict = dict()
    ReadFiles(rootDir, file_dict = files_dict)
    pass
