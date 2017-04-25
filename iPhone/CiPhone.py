#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: CiPhone.py 
@time: 2017/4/25 11:51 
@version: v1.0 
"""
class iPhone_v:
    """表示一个型号的iPhone"""
    population = 0

    def __init__(self,name):
        """init data"""
        self.name = name
        print "New iPhone have publish:",self.name
        iPhone_v.population += 1

    def recycle(self):
        """this iPhone is recycle"""
        print "This iPhone will be recycle:",self.name
        iPhone_v.population -= 1

        if iPhone_v.population == 0:
            print "no iPhone_v has publish\n"
        else:
            print "There still have",iPhone_v.population,"iPhone_v publish.\n"

    def say_hi(self):
        """new iPhone publish"""
        print "This is new iPhone",self.name,"publish."

    @classmethod
    def how_many(cls):
        """print how many iPhone_v have been publish"""
        print "There have published",iPhone_v.population,"iPhones."
