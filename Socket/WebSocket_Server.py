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
import logging
from websocket_server import WebsocketServer
import json


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], len(message)))
    print("Client(%d) said: %s" % (client['id'], message))
    server.send_message_to_all(json.dumps({"type": 1}))


PORT = 9001
server = WebsocketServer(PORT, host = "192.168.2.41")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

#
# def Receive(socket, nickname):
#     try:
#         while True:
#             data = socket.recv(1024)
#             if data == 'exit' or not data:
#                 break
#             BroadData(socket, "%s >>  %s" % (nickname, data))
#     except:
#         pass
#     socket.close()
#     CONNECTION_LIST.remove(socket)
#     BroadData(socket, nickname + " leaved chatroom.")
#
#
# def SendData(sock):
#     try:
#         while True:
#             data = raw_input()
#             if data == "":
#                 continue
#             BroadData(server, "*" * 25 + "%s" % data + "*" * 25)
#     except:
#         pass
#
#
# def BroadData(sock, message):
#     print message
#     for socket in CONNECTION_LIST:
#         if socket != sock and socket != server:
#             try:
#                 socket.send(message)
#             except:
#                 socket.close()
#                 CONNECTION_LIST.remove(socket)
#
#
# if __name__ == "__main__":
#     CONNECTION_LIST = []
#
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.setsockopt()
#     server.bind(('0.0.0.0', 7899))
#     server.listen(5)
#
#     CONNECTION_LIST.append(server)
#     print "Waiting NEW connection..."
#
#     while True:
#         sock, addr = server.accept()
#         CONNECTION_LIST.append(sock)
#         nickname = sock.recv(1024)
#         BroadData(server, "Wlecome " + nickname + "(%s:%s)" % addr + " enter chatroom.")
#         r = threading.Thread(target = Receive, args = (sock, nickname)).start()
#         s = threading.Thread(target = SendData, args = (sock,)).start()
