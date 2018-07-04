"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ReadImpoertMessage.py
 @Time    : 2018/6/29 15:21
"""
import os

# dir_a = "C:\\Users\\xiaohui\\Desktop\\Android远程植入调研（2018-06-25）\\植入测试\\download"
# keyword = b"5b1d21092c8c45"
#
#
# list_a = list()
# for fileinfo in os.walk(dir_a):
#     for file in (os.path.join(fileinfo[0], file) for file in fileinfo[2]):
#         if os.path.isfile(file):
#             with open(file, "rb") as f:
#                 content = f.read()
#                 if keyword in content:
#                     print("keyword find in {targetFile}".format(targetFile=file))
pass

# print(os.cpu_count())
# import time
# from tqdm import tqdm
#
# for i in tqdm(range(1000)):
#     time.sleep(.01)

import sys, time
import multiprocessing

flush = sys.stdout.flush
DELAY = 0.1
DISPLAY = ['|', '/', '-', '\\']


def spinner_func(before='', after=''):
    write, flush = sys.stdout.write, sys.stdout.flush
    pos = -1
    while True:
        pos = (pos + 1) % len(DISPLAY)
        msg = before + DISPLAY[pos] + after
        write(msg);
        flush()
        write('\x08' * len(msg))
        time.sleep(DELAY)


def long_computation():
    # emulate a long computation
    time.sleep(3)


if __name__ == '__main__':
    spinner = multiprocessing.Process(None, spinner_func, args=('Please wait ... ', ''))
    spinner.start()
    try:
        long_computation()
        print('Computation done')
    finally:
        spinner.terminate()

from threading import Thread

import asyncio

@asyncio.coroutine

