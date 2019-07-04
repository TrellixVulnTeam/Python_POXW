"""
@author: Alfons
@contact: alfons_xh@163.com
@file: UnderLineTest.py
@time: 2019/7/4 下午9:50
@version: v1.0 
"""
_Test__arga = "hello"


class Test:
    def __init__(self):
        self.__ar = None

    def print(self):
        return __arga


t = Test()
print(t.print())
print(t._Test__ar)

print(dir(t))
