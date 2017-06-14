#!/usr/bin/python
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: SocketTest.py 
@time: 17-5-19 下午5:32 
@version: v1.0 
"""
import socket
def run():
    host_name = socket.gethostname()
    host_name = "www.google.com"
    host_ip = socket.gethostbyname(host_name)
    print host_ip

    DstPort = 20480
    converPort = socket.htons(DstPort)

    strtmp = "jx_dns"
    tmpstr = strtmp[0:3]
    pass