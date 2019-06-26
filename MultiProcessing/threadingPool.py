"""
@author: Alfons
@contact: alfons_xh@163.com
@file: threadingPool.py
@time: 2019/6/22 下午5:12
@version: v1.0 
"""
import time
import threading
from queue import Queue
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool


def func(x, return_dict):
    time.sleep(1)
    print(x << 2)
    return_dict[x] = x * x


def add(x, y):
    return x + y


def PoolByModule():
    pool = ThreadPool(processes=cpu_count() << 2)

    # for i in range(20):
    #     pool.apply(func, args=(i,))         # 同步方式，会等待上一个线程执行结束
    #     # pool.apply_async(func, args=(i,))      # 异步方式，'并行'

    # 线程池map操作
    # res = pool.map(func, range(20))
    # print(res)

    # res = pool.map_async(func, range(20))
    # print(res.get())

    # 线程池imap操作
    # res = pool.imap(func, range(20))
    # print([i for i in res])

    # res = pool.imap_unordered(func, range(20))
    # print([i for i in res])

    # 多输入参数方法实现调用
    res = pool.starmap(add, enumerate(range(20)))
    print(res)

    res = pool.starmap_async(add, enumerate(range(20)))
    print(res.get())


def PoolByUser():
    pool = list()
    # return_dict = dict()
    return_dict = dict()

    for i in range(10):
        p = threading.Thread(target=func, args=(i, return_dict))
        p.start()
        pool.append(p)

    for p in pool:
        p.join()

    print(return_dict)


task_queue = Queue()
need_run = True
return_dict = dict()


def task_func(return_dit):
    while need_run:
        try:
            x = task_queue.get(timeout=2)
            return_dit.update({x: x * x})
        except:
            pass


def PoolUseTaskQueue():
    t_list = list()
    for i in range(10):
        t = threading.Thread(target=task_func, args=(return_dict,))
        t.start()
        t_list.append(t)

    [task_queue.put(i) for i in range(20)]

    global need_run
    need_run = False
    for t in t_list:
        t.join()
    print(return_dict)


if __name__ == '__main__':
    PoolByUser()
    # PoolUseTaskQueue()
