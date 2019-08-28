"""
@file: 1.Sync_blocking.py
@time: 2019/8/22
@author: alfons
"""
import socket


def blocking_way():
    sock = socket.socket()

    host = "baidu.com"
    sock.connect((host, 80))
    request = f'GET / HTTP/1.0\r\nHost: {host}\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)

    return response


def sync_way():
    for i in range(10):
        print(blocking_way(), flush=True)


if __name__ == '__main__':
    import time

    start_time = time.time()
    sync_way()
    print("Use time -> {}'s.".format(time.time() - start_time))
