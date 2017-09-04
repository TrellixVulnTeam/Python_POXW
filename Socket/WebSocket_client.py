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
import threading

def SendData(sock):
    while True:
        data = raw_input()
        if data == "exit":
            break
        sock.send(data)
        print "Me : %s" % data
    sock.close()

def ReceiveData(sock):
    while True:
        data = sock.recv(1024)
        print data

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.2.41", 7899))
    nickname = raw_input("Input your nickname:")
    client.send(nickname)
    r = threading.Thread(target = SendData, args = client)
    s = threading.Thread(target = ReceiveData, args = client)
    r.start()
    s.start()
