"""
@file: GIL_multi_thread.py
@time: 2019/01/29
@author: sch
"""
import time
from threading import Thread


def single_thread(n):
    for i in range(n):
        pass


def multi_thread(n, thread_num):
    start_time = time.time()

    thread_list = list()
    for _ in range(thread_num):
        t = Thread(target = single_thread, args = (int(n / thread_num),))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print("use time: {}'s.".format(time.time() - start_time))


if __name__ == '__main__':
    multi_thread(10 ** 8, 2)
