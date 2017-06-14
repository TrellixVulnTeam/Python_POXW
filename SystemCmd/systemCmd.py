#!/usr/bin/python
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: systemCmd.py 
@time: 17-6-12 下午3:43 
@version: v1.0 
"""

import os
ret1 = os.system("systemctl is-active ImportDB.service")
ret1 = ret1 >> 8

ret2 = os.popen("systemctl is-active httpd.service").readlines()

ret3 = os.popen("systemctl status httpd.service").readlines()

pass