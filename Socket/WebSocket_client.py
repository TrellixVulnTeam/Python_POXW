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
import websocket



def SendData(sock, receiver):
    while True:
        data = raw_input()
        if data == "exit":
            break
        sock.send(data,)
        print "Me >>  %s" % data
    sock.close()
    receiver.join()


def ReceiveData(sock):
    while True:
        data = sock.recv()
        print data


if __name__ == "__main__":
    #
    #
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(("ws://192.168.2.24/RcsDataSys/ws/httpsData/command",8088))
    # nickname = raw_input("Input your nickname:")
    # client.send(nickname)
    # r = threading.Thread(target = ReceiveData, args = (client,))
    # r.start()
    # s = threading.Thread(target = SendData, args = (client, r)).start()

    client = websocket.WebSocket()
    # ws.connect(url ="ws://192.168.2.24:8088/RcsDataSys/ws/httpsData/command")
    client.connect(url = "ws://127.0.0.1:9001")
    client.recv()
    client.send()
    r = threading.Thread(target = ReceiveData, args = (client,))
    r.start()
    s = threading.Thread(target = SendData, args = (client, r)).start()
    pass
