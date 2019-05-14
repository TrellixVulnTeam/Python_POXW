"""
@author: Alfons
@contact: alfons_xh@163.com
@file: nametuple_more.py
@time: 2019/4/5 上午11:23
@version: v1.0 
"""
from collections import namedtuple

Student = namedtuple("test", "name,age,sex")

s = Student("alfons", 15, "male")
print(s)

list_a = list(range(9, 2, -1))
list_b = list_a[-1:-6:-1]
print(list_b)

# a = 1


def func1():
    b = 2

    def func3():
        global a
        a = 2
        nonlocal b
        b = 3
        c = 3
        print(f"a={a}, b={b}, c={c}")
        print(locals())

    func3()
    print(f"b={b}")


func1()
print(a)
print(globals())
print(locals())
print()

l_a = [1, 2, 3, 4]
t_a = tuple((l_a, 1, 2))
print(id(l_a))
print(t_a)
del t_a
print(id(l_a))

l_b = l_a
print(id(l_a), id(l_b))
del l_a
print(id(l_b))

