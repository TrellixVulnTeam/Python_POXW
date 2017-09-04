#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: WebSocket_Server.py
@time: 2017/9/4 10:02
@version: v1.0
"""
import socket
import threading
import time


def tcplink(sock, addr):
    print "Accept new connection from %s:%s..." % addr
    sock.send('hello %s!' % addr)
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if data == 'exit' or not data:
            break
        sock.send("%s: %s" % addr, data)
    sock.close()
    print "Connection from %s:%s closed." % addr


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 7899))
s.listen(3)
print "Waiting NEW connection..."

while True:
    sock, addr = s.accept()
    t = threading.Tread(target = tcplink, args = (sock, addr))
    t.start
