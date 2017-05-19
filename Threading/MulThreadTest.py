#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: MulThreadTest.py 
@time: 2017/5/19 15:07 
@version: v1.0 
"""
import threading, time, random
count = 0
lock = threading.Lock()


def doAdd():
    '''@summary: 将全局变量count 逐一的增加10000。
    '''
    global count, lock
    lock.acquire()
    for i in xrange(10000):
        count = count + 1
        print threading.currentThread(),count
    lock.release()


threading.Thread
threading.Thread(target = doAdd, args = (), name = 'thread').start()
time.sleep(2)  # 确保线程都执行完毕
print count
