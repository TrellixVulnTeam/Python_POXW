#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
    """
    将全局变量count 逐一的增加10000。
    :return:
    """
    global count, lock
    # lock.acquire()
    # for i in range(10000000):
    #     count = count + 1
    # lock.release()
    #
    # with lock:
    #     for i in range(1000000000):
    #         count = count + 1

    for i in range(1000000000):
        count = count + 1


def do_sleep(n):
    i = 0
    while True:
        if i >= n:
            break
        else:
            i += 1
            time.sleep(1)


threadTmp = threading.Thread(target=do_sleep, args=(5,), name='thread')
threadTmp.start()

for i in range(100):
    time.sleep(0.1)
    print threadTmp.isAlive()

print(count)

# import time
#
#
# def fun_a(t):
#     time.sleep(t)
#     return t
#
#
# from multiprocessing.pool import ThreadPool
#
# t_pool = ThreadPool(4)
# res = t_pool.map_async(func=fun_a, iterable=[1, 2, 3, 4])
# t_pool.close()
# t_pool.join()
# print(res.get())
