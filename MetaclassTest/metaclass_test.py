#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: metaclass_test.py
# Author: alfons
# LastChange:  2020/7/8 下午3:20
#=============================================================================
"""
class Meta(type):
    def __new__(cls, name, bases, namespace, **kwargs):

