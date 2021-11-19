#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: performance_test.py
@time: 2020/6/19
@author: alfons
"""
import time
import requests
# from multiprocessing.pool import ThreadPool
import threading

REQUEST_GET = "get"
REQUEST_POST = "post"

total_num = 0


def func_request(method: str = REQUEST_GET, url: str = None, num: int = None):
    if method == REQUEST_GET:
        response = requests.get(url)
        global total_num
        total_num += 1
        # print("{}: {}".format(num, response.content))


def test_time(thread_num: int):
    global total_num
    total_num = 0

    start_time = time.time()

    thread_list = list()
    for i in range(thread_num):
        t = threading.Thread(target=func_request, args=(REQUEST_GET, "http://127.0.0.1:8000", i))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    time_use = time.time() - start_time
    print("Total time use: {:.2f}'s.".format(time_use))
    print(f"Total number: {total_num}.")
    return time_use


def test_worker_time(worker_num: int, thread_one_worker: int = 20, max_thread: int = None, time_wait: int = 3):
    thread_high = worker_num * thread_one_worker + 1 if not max_thread else max_thread

    standard_num = 0
    while standard_num < 3:
        print("\n")
        print(f"Worker {worker_num} use threads {thread_high} test, {standard_num + 1} time".center(64, "="))
        time_use = test_time(thread_high)
        if abs(time_use - time_wait) < 0.5:
            standard_num += 1
        else:
            thread_high -= 1
            standard_num = 0

    return thread_high


worker_num = 10
t_num = test_worker_time(worker_num, max_thread=20)
print("\nWorker {worker_num}, max thread {t_num}".format(worker_num=worker_num, t_num=t_num))
