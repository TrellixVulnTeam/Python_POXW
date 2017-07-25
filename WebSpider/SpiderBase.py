#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: SpiderBase.py 
@time: 2017/7/25 17:37 
@version: v1.0 
"""
import os

def IsDirEmpty(dir_path):
    files = os.listdir(dir_path)
    if not files:
        return True
    return False