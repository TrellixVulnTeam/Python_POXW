#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: codeinGame.py 
@time: 2017/9/18 19:58 
@version: v1.0 
"""
import sys
import math

# The while loop represents the game.
# Each iteration represents a turn of the game
# where you are given inputs (the heights of the mountains)
# and where you have to print an output (the index of the mountain to fire on)
# The inputs you are given are automatically updated according to your last actions.


# game loop
while True:

    mountain_dict = dict()
    for i in xrange(8):
        mountain_h = int(raw_input())  # represents the height of one mountain.
        mountain_dict.update({mountain_h: i})
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # The index of the mountain to fire on.
    mou_h = mountain_dict.keys()
    mou_h.sort()
    mou_h.reverse()
    for h in mou_h:
        print mountain_dict[h]