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


def Receive(socket, nickname):
    while True:
        data = socket.recv(1024)
        if data == 'exit' or not data:
            break
        BroadData(socket, "%s: %s" % (nickname, data))
    socket.close()
    CONNECTION_LIST.remove(socket)
    print nickname + " leaved chatroom."
    BroadData(socket, nickname + " leaved chatroom.")


def SendData(sock):
    pass


def BroadData(sock, message):
    print message
    for socket in CONNECTION_LIST:
        if socket != sock:
            try:
                socket.send(message)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)


if __name__ == "__main__":
    CONNECTION_LIST = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 7899))
    server.listen(5)

    CONNECTION_LIST.append(server)
    print "Waiting NEW connection..."

    while True:
        sock, addr = server.accept()
        CONNECTION_LIST.append(sock)
        nickname = sock.recv(1024)
        BroadData(server, "Wlecome " + nickname + " enter chatroom.")
        r = threading.Thread(target = Receive, args = (sock, nickname))
        s = threading.Thread(target = SendData, args = (sock,))
        r.start()
        s.start()
