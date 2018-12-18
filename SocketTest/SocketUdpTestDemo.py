"""
@file: SocketUdpTestDemo.py
@time: 2018/12/17
@author: sch
"""
import os
import socket
import traceback
import struct


def IPInt2Str(ipInt):
    return socket.inet_ntoa(struct.pack('I', socket.htonl(ipInt)))


cmd = "ping {ip}:{port}".format(ip = IPInt2Str(3662778923), port = 24627)
returncode = os.system(cmd)

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.settimeout(5)

try:
    # sk.connect((IPInt2Str(3662778923), 24627))
    sk.sendto(b"hello", (IPInt2Str(3662778923), 24627))
    print("Connect success")
except:
    traceback.print_exc()
    print("Connect fail!")
