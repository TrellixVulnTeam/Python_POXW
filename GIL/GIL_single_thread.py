"""
@file: GIL.py
@time: 2019/01/29
@author: sch
"""
import time


def single_thread(n):
    for i in range(n):
        pass


if __name__ == '__main__':
    start_time = time.time()
    single_thread(10 ** 8)
    print("use time: {}'s.".format(time.time() - start_time))
