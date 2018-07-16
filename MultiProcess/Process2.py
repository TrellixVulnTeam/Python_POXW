"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Process2.py
@time: 18-6-25 下午11:25
@version: v1.0 
"""
import mmap, os, time

m = mmap.mmap(os.open('xxx', os.O_RDWR), 1)
last = None
while True:
    m.resize(m.size())
    data = m[:]
    if data != last:
        print(data)
        last = data
    time.sleep(5)
