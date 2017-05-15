#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ReadPath.py 
@time: 2017/5/15 15:36 
@version: v1.0 
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os

f = open("C:\Users\shangchenhui\Desktop\TestApk.txt","w")
rootdir = unicode("""D:\downloads\\apps""", "GB2312")
root = os.listdir(rootdir)
for subRootPath in root:
    subRootPathTmp = "D:\downloads\\apps\\" + subRootPath
    if not os.path.isdir(subRootPathTmp):
        continue
    subRoot = os.listdir(subRootPathTmp)
    f.write(subRootPath+":\n")
    for apk in subRoot:
        if os.path.splitext(apk)[1]=='.apk':
            f.write("\t\t")
            f.write(apk)
            f.write('\n')
f.close()
pass

