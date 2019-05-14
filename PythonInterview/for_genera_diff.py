"""
@author: Alfons
@contact: alfons_xh@163.com
@file: tmp.py
@time: 19-3-18 下午11:23
@version: v1.0 
"""
import time
import sys

list_len = 10 ** 6

# for 循环使用时间及内存
start_time = time.time()

tmp = list()
for i in range(list_len):
    tmp.append(i)

print("for use time: {}'s.".format(time.time() - start_time))
print("for use memory: {} bytes.".format(sys.getsizeof(tmp)))

# 列表生成式使用时间及内存
start_time = time.time()

tmp = [i for i in range(list_len)]

print("list genera use time: {}'s.".format(time.time() - start_time))
print("list genera use memory: {} bytes.".format(sys.getsizeof(tmp)))

# yield 使用时间及内存
start_time = time.time()

tmp = (i for i in range(list_len))

print("yield use time: {}'s.".format(time.time() - start_time))
print("yield use memory: {} bytes.".format(sys.getsizeof(tmp)))


