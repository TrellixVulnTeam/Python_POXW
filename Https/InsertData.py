#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: InsertData.py 
@time: 2017/5/11 19:17 
@version: v1.0 
"""
import MySQLdb
import time

db = MySQLdb.connect(host = "127.0.0.1",
                     port = 3306,
                     db = "wifilz",
                     user = "vm_user",
                     passwd = "xiaohui",
                     charset = "utf8")
cursor = db.cursor()
import os
import os.path
rootdir = "C:\Users\shangchenhui\Desktop\ImportData"  # 指明被遍历的文件夹

files = []
for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    files = filenames

n = 0
while True:
    for file in files:
        f = open(rootdir + "\\" + file, 'r')
        for line in f:
            if line:
                cursor.execute(line)
        f.close()
    db.commit()
    n += 1
    print "commit number:" + str(n)
    time.sleep(10)
