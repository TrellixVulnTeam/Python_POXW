"""
@file: GIL_multi_process.py
@time: 2019/01/29
@author: sch
"""
import time
from multiprocessing import Process


def single_thread(n):
    for i in range(n):
        pass


def multi_process(n, thread_num):
    thread_list = list()
    for _ in range(thread_num):
        t = Process(target = single_thread, args = (int(n / thread_num),))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start_time = time.time()
    multi_process(10 ** 8, 2)
    print("use time: {}'s.".format(time.time() - start_time))
