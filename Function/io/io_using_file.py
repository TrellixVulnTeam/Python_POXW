#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: io_using_file.py 
@time: 2017/4/25 14:35 
@version: v1.0 
"""


def file_w_r():
    str = """
    这是一个字符串。
    里面是一些文字，
    用于测试此函数。
    """
    filename = "file_func.txt"
    f = open(filename, 'w')
    f.write(str)
    f.close()

    f = open(filename, 'r')
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print line,

    f.close()
    import os
    os.remove(filename)
