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
import random

import logging
import traceback

db = MySQLdb.connect(host = "127.0.0.1",
                     port = 3306,
                     db = "wifilz",
                     user = "vm_user",
                     passwd = "xiaohui",
                     charset = "utf8")

import os
import os.path
rootdir = "C:\Users\shangchenhui\Desktop\ImportData"  # 指明被遍历的文件夹

files = []
for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    files = filenames


def Run(n,db):
    try:
        cursor = db.cursor()
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
            timetmp = random.randint(20,60)
            time.sleep(timetmp)
    except:
        cursor.close()
        db.close()
        logging.error("回传数据错误 : %s" % traceback.format_exc())
        time.sleep(random.randint(20,60))
        newdb = MySQLdb.connect(host = "192.168.10.124",
                             port = 3306,
                             db = "wifilz",
                             user = "root",
                             passwd = "ygwifidb_password",
                             charset = "utf8")
        Run(n, newdb)

if __name__ == "__main__":
    n = 0
    Run(n,db)