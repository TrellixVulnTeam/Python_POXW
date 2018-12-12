"""
@file: GeneratorsTest.py
@time: 2018/12/11
@author: sch
"""
import time


def TailF(file_handle):
    while True:
        line = file_handle.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def Grep(pattern, lines):
    for line in lines:
        if pattern in line.lower():
            yield line


logfile = open("feedback.log", "r")
lines = TailF(logfile)

for line in Grep("feedback", lines):
    print(line)
