"""
@author: Alfons
@contact: alfons_xh@163.com
@file: frame.py
@time: 2019/4/7 下午4:11
@version: v1.0 
"""
import sys

version = 1


def g():
    frame = sys._getframe()
    print('current function is : ', frame.f_code.co_name)
    caller = frame.f_back
    print('g() function is called by ', caller.f_code.co_name)
    print('local namespace: ', caller.f_locals)
    print('global namaspace: ', caller.f_globals.keys())


def f():
    a = 1
    b = 2
    g()


def show():
    f()


show()
