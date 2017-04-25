#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: File_func.py 
@time: 2017/4/25 14:35 
@version: v1.0 
"""


def file_w_r():
    str = """
    这是一个字符串。
    里面是一些文字，
    用于测试此函数。
    """

    f = open("file_func.txt", 'w')
    f.write(str)
    f.close()

    f = open("file_func.txt", 'r')
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        print line,

    f.close()
