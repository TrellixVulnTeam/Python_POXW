"""
@author: Alfons
@contact: alfons_xh@163.com
@file: copy_and_deepcopy.py
@time: 2019/4/6 上午11:26
@version: v1.0 
"""
import copy

list_a = [1, 2, 3, 4, 5]
list_b = (list_a, 6, 7, 8)

list_c = [list_a, list_b, 9, 10]
list_d = copy.deepcopy(list_c)
list_e = copy.copy(list_c)

print(id(list_c[1]), id(list_d[1]))
print(id(list_c[1]), id(list_e[1]))

list_a.append(11)
print(list_d)


class A:
    def __init__(self):
        self.list_a = [1, 2, 3, 4, 5]
        self.list_b = [self.list_a, 6, 7, 8]
        self.list_c = [self.list_a, self.list_b, 9, 10]


cls_a = A()
cls_b = cls_a
cls_a.list_a.append(6)
print(cls_b.list_a)
cls_c = copy.deepcopy(cls_a)

str_a = "fasdfdfadsfasdfaaaa#fddddddddddddddaaaaaaaaaaaaaaaaaa"
print(id(str_a))
del str_a

str_b = "fasdfdfadsfasdfaaaa#fddddddddddddddaaaaaaaaaaaaaaaaaa"
print(id(str_b))
