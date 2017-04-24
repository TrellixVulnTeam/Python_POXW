#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: print_max.py 
@time: 2017/4/24 16:52 
@version: v1.0 
"""

print("hell sa")
i = 4 + 1
print(i)
print("{name} is find {client}".format(name = 'Alfons', client = "dota2"))
print("{0:.3}".format(10.0 / 3))
print("{0:.^13}".format('hello'))
print(not 0)

# new line,Function if-else
number = 333
print("enter number:")
guss = int(input())
print(guss)

if guss == number:
    print("guss == input number")
    print("hahahah")
elif number > guss:
    print("guss < number")
else:
    print("both shit")

# NEW LINE,Function while
number = 333
running = True
while running:
    guss = int(input("input a int:"))
    if guss == number:
        print("guss == input number")
        running = False
    elif guss < number:
        print("guss < number")
    else:
        print("both shit")
else:
    print('The while loop is over.')

# NEW LINE,Function for
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

# NEW LINE,Function def
from print_max import print_max

print_max(4, 5)
print_max(5, 4)
print_max(4, 4)
