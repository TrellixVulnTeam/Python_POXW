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

import subprocess

p = subprocess.Popen(["ls"], stdout = subprocess.PIPE)
out = p.stdout.readlines()
print out

DN = open(os.devnull, 'w')
print DN
import  pyric.pyw as pyw
AP_List = pyw.interfaces()
cards = pyw.getcard(AP_List[4])
phyInfo = pyw.phyinfo(cards)
devmode = pyw.devmodes(cards)

pass

