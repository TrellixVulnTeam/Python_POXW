"""
@author: Alfons
@contact: alfons_xh@163.com
@file: class_inter.py
@time: 2019/4/7 下午10:41
@version: v1.0 
"""
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B,C):
    pass


print(D.__mro__)