#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com 
@file: Logic_Function.py 
@time: 2017/4/25 9:23 
@version: v1.0 
"""


def Logic():
    # new line,Function if-else
    print ("{0:_^64}".format("Logic_Function.if-elif()"))
    number = 333
    print("enter number:")
    guss = 333
    print(guss)

    if guss == number:
        print("guss == input number")
        print("hahahah")
    elif number > guss:
        print("guss < number")
    else:
        print("both shit")

    # NEW LINE,Function while
    print ("{0:_^64}".format("Logic_Function.while()"))
    number = 333
    running = True
    while running:
        guss = 333
        if guss == number:
            print("guss == input number")
            running = False
        elif guss < number:
            print("guss < number")
        else:
            print("both shit")
    else:
        print('The while loop is over.')
    print("")

    # NEW LINE,Function for
    print ("{0:_^64}".format("Logic_Function.for()"))
    sumer = 0
    for i in range(0, 10):
        sumer += i
    # print('sum is:{0}'.format(sumer))
    print("sum is:", sumer)  # print:('sum is:', 45)
    print"sum is:", sumer  # print: sum is: 45

    sumer = 1
    for i in range(1, 10):
        sumer *= i
    print"9! =", sumer
    print("")
