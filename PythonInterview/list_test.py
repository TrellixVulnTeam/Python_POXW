"""
@author: Alfons
@contact: alfons_xh@163.com
@file: list.py
@time: 2019/4/7 下午7:42
@version: v1.0 
"""
list_a = [1, 23, 4]
list_a.insert(-9, 0)
print(list_a)

dict_a = dict(a=1)
print(len(dict_a))

from dis import dis
import sys


def func_list():
    list_a = [0, 1, 2, 3, 4, 5]


def func_tuple():
    tuple_a = (1, 23, 4, 5, 6, 7, 8, 9, 0, 0)


def func_str():
    str_a = "hello"


def func_dict():
    dict_a = dict(a='1')


def func_yield():
    # for i in range(10):
    yield 2
    yield 3
    yield 10


print("list compile:")
print(dis(func_list))
print("tuple compile:")
print(dis(func_tuple))
print("dcit compile:")
print(dis(func_dict))
print("str compile:")
print(dis(func_str))
print("yield compile:")
print(dis(func_yield))
frame = sys._getframe()
print(frame)


def func_for():
    list_a = []
    for i in range(10):
        list_a.append(i)


def func_iter():
    list_a = [i for i in range(10)]


def func_gen():
    list_a = (i for i in range(10))


def func_gen2():
    for i in range(10):
        yield i

print("func_for compile:")
print(dis(func_for))
print("func_iter compile:")
print(dis(func_iter))
print("func_gen compile:")
print(dis(func_gen))
print("func_gen2 compile:")
print(dis(func_gen2))
