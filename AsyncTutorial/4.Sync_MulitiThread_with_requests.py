"""
@file: 3.Sync_MulitiThread_with_requests.py
@time: 2019/8/22
@author: alfons
"""
import requests
from concurrent import futures


def blocking_way():

    host = "https://baidu.com"
    response = requests.get(host).content
    return response


def thread_way():
    workers = 10
    with futures.ThreadPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(workers)}
    return len([fut.result() for fut in futs])


if __name__ == '__main__':
    import time

    start_time = time.time()
    thread_way()
    print("Use time -> {}'s.".format(time.time() - start_time))
