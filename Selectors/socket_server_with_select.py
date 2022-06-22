#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: socket_server_with_select.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/6/7 10:35
# History:
#=============================================================================
"""
import selectors
import socket

# sel = selectors.DefaultSelector()
sel = selectors.PollSelector()


def _server_accept(sock: socket.socket, mask):
    connection, client_address = sock.accept()
    print('accepted', connection, 'from', client_address)
    connection.setblocking(False)
    sel.register(connection, selectors.EVENT_READ, _server_read)


def _server_read(connection: socket.socket, mask):
    try:
        data = connection.recv(1024)
        if data:
            print('echoing', repr(data), 'to', connection)
            connection.send(data)  # Hope it won't block
        else:
            print('closing', connection)
            sel.unregister(connection)
            connection.close()
    except:
        print('closing', connection)


# Create a TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('localhost', 8090))
server.listen(5)
sel.register(server, selectors.EVENT_READ, _server_accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
