"""
@author: Alfons
@contact: alfons_xh@163.com
@file: 2-4.dunder.py
@time: 2019/8/11 上午10:46
@version: v1.0 
"""
_Test__value = "hello"


class Test:
    def func(self):
        return __value


print(Test().func())
