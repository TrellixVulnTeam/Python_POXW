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

threadList = list()
for _ in range(10):
    threadTmp = threading.Thread(target=doAdd, name='thread')
    threadTmp.start()
    threadList.append(threadTmp)

for thread in threadList:
    thread.join()

print(count)
