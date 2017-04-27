#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: animal.py 
@time: 2017/4/25 12:23 
@version: v1.0 
"""


class animal:
    def run(self):
        print "Animal running..."


class dog(animal):
    def __init__(self, food):
        self.__food = food

    def run(self):
        print "Dog running..."

    def eat(self):
        print "Dog eating ", self.__food


class cat(animal):
    def __init__(self, food):
        self.__food = food

    def run(self):
        print "Cat running..."

    def eat(self):
        print "Cat eating...", self.__food
