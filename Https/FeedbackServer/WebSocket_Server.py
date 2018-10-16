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
from Crypt.AES import *
import threading

encrypt_key = b"84c3e271c596b5a4288b685c0ae40f00"


# Called for every client connecting (after handshake)
def new_client(client, server):
    print("New client connected and was given id %d" % client['id'])
    # server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    print("Client(%d) said[length]: %s" % (client['id'], len(message)))
    print("Client(%d) said[cryptotext]: %s" % (client['id'], message))
    print("Client(%d) said[plaintext]: %s" % (client['id'], AES_ECB_DECRYPT(message.encode(), key=encrypt_key).decode("unicode-escape")))
    server.send_message(client, AES_ECB_ENCRYPT(json.dumps({"type": 1}).encode(), key=encrypt_key))


PORT = 9000
server = WebsocketServer(PORT, host="0.0.0.0")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
threading.Thread(target=server.run_forever, args=()).start()

cmd_dict = {1: "restart", 2: "shutdown", 3: "startap", 4: "update", 5: "startap", 6: "UpdateKeyPerson", 7: "DeleteKeyPerson"}
while True:
    command = int(input())
    cmd = {"command": cmd_dict.get(command), "id": 999, "type": 2}
    if command == 3:
        cmd.update({"aps": [{"ssid": "啊打发回家送饭", "protect": "WPA", "password": "doadssvdf56"}
                            # {"ssid": "大吉大利今晚吃鸡", "protect": "OPN", "password": ""}
                            ],
                    "channel": 3})

        cmd.update({"count": len(cmd.get("aps"))})
    elif command == 5:
        cmd.update({"aps": [{"ssid": "啊打发回家送饭", "protect": "WPA", "password": "doadssvdf56"},
                            {"ssid": "大吉大利今晚吃鸡", "protect": "OPN", "password": ""},
                            {"ssid": "大利大吉，今晚吃鸡！", "protect": "OPN", "password": ""},
                            {"ssid": "今晚吃鸡，大吉大利！", "protect": "WPA",
                             "password": "123456789898654654646514489465184163146fdsfasfasddseefdsaf"}
                            ],
                    "channel": 5})
        cmd.update({"count": len(cmd.get("aps"))})
    elif command == 4:
        cmd.update({"version": "V 3.6.1", "isFully": True})
    elif command == 6:
        cmd.update(dict(keyPersons = [dict(mac = "AA:75:90:AB:4E:FF", name = "测试22")]))
    elif command == 7:
        cmd.update(dict(keyPersons = ["AA:75:90:AB:4E:FF"]))
    server.send_message_to_all(AES_ECB_ENCRYPT(json.dumps(cmd).encode(), key=encrypt_key))

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
