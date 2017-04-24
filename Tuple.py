#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Tuple.py 
@time: 2017/4/24 17:49 
@version: v1.0 
"""

def tuple(num,*number,**userName):
    """这是一个遍历元祖的函数,输出每个元祖的元素"""
    print"Function___tuple"
    print num
    for iter in number:
        print "elem in number is:",iter

    for first_iter,second_iter in userName.items():
        print first_iter,":",second_iter
