#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: animal.py 
@time: 2017/4/25 12:23 
@version: v1.0 
"""


class Animal(object):
    pass


class Mammal(Animal):
    def run(self):
        print "Mammal running..."


class Bird(Animal):
    def fly(self):
        print "Birds running..."


class Dog(Mammal):
    def __init__(self, food):
        self.__food = food

    def eat(self):
        print "Dog eating ", self.__food


class Cat(Mammal):
    def __init__(self, food):
        self.__food = food

    def eat(self):
        print "Cat eating...", self.__food

