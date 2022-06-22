"""
@file: SocketTestDemo.py
@time: 2018/12/17
@author: sch
"""
import socket
import traceback

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.settimeout(5)

try:
    sk.connect(("localhost", 1234))
    sk.send(b"hello world")
    print("Connect success!")
except:
    traceback.print_exc()
    print("port 80 con not connect!")
sk.close()
