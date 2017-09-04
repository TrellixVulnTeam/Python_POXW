#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: WebSocket_client.py 
@time: 2017/9/4 11:25 
@version: v1.0 
"""
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.2.41", 7899))
print s.recv(1024)
for data in ["nihao", "lgd", "eg"]:
    s.send(data)
    print s.recv(1024)
s.send("exit")
s.close()
