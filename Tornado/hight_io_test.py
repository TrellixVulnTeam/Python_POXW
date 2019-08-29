"""
@file: hight_io_test.py
@time: 2019/8/29
@author: alfons
"""
from multiprocessing.pool import ThreadPool
import requests


def get(i):
    status = requests.get("http://127.0.0.1:8000/test").status_code
    print(f"status -> {status}, id -> {i}", flush=True)


# thread_num = 1024       # select 文件数过多
thread_num = 256
thread_pool = ThreadPool(thread_num)

for i in range(thread_num):
    thread_pool.apply_async(get, args=(i,))

thread_pool.close()
thread_pool.join()
