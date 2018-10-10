"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ReadElf.py
 @Time    : 2018/9/30 9:27
"""
import os
from subprocess import call

fileList = [os.path.join("./", file) for file in os.listdir("./") if file.endswith(".so")]

for file in fileList:
    call("readelf {file} -a > {file}.txt".format(file = file), shell=True)
