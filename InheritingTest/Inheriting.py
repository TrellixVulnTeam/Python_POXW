"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Inheriting.py
@time: 2019/5/14 下午8:37
@version: v1.0 
"""


class A:
    def SayHello(self):
        print("A hello")


class B:
    def SayGoodBye(self):
        print("B goodbye")


class C(A, B):
    pass


class D:
    def __init__(self):
        self.a_obj = A()
        self.b_ojb = B()

    def SayHello(self):
        return self.a_obj.SayHello()

    def SayGoodBye(self):
        return self.b_ojb.SayGoodBye()


if __name__ == '__main__':
    c_obj = C()
    c_obj.SayHello()
    c_obj.SayGoodBye()

    d_obj = D()
    d_obj.SayHello()
    d_obj.SayGoodBye()
