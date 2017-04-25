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
    def __init__(self, name, loction):
        self.name = name
        self.loction = loction
        print self.name, "have been init."

    def live(self):
        print self.name, "living in", self.loction


class bird(animal):
    def __init__(self, name, loction, fly):
        self.name = name
        self.loction = loction
        self.fly = fly
        print self.name, "have been init."

    def live(self):
        print self.name, "living in", self.loction, "and it", self.fly, "fly"


class dog(animal):
    def __init__(self, name, loction, fly):
        self.name = name
        self.loction = loction
        self.fly = fly
        print self.name, "have been init."

    def live(self):
        print self.name, "living in", self.loction, "and it", self.fly, "fly"
