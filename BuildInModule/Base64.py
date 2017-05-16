#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Base64.py 
@time: 2017/5/16 9:53 
@version: v1.0 
"""
import base64
str_1 = "helloworld++//"
base64_A = base64.encodestring(str_1)
base64_B = base64.decodestring(base64_A)
base64_C = base64.urlsafe_b64decode(base64_A)
pass