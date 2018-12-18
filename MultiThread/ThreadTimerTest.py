"""
@file: ThreadTimerTest.py
@time: 2018/12/18
@author: sch
"""
import threading
import time

i = 0


def PrintOnTime(interval):
    print("hello", time.strftime("%Y-%m-%d %X", time.localtime()))

    timer = threading.Timer(interval, PrintOnTime, args = (interval,))
    timer.start()

    global i
    i += 1
    if i > 5:
        timer.cancel()


if __name__ == '__main__':
    PrintOnTime(3)
