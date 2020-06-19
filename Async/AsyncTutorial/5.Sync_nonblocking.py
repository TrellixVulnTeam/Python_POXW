"""
@file: 5.Sync_nonblocking.py
@time: 2019/8/23
@author: alfons
"""
import socket


def nonblocking_way():
    sock = socket.socket()
    sock.setblocking(False)     # 设置socket为非阻塞的方式
    host = "baidu.com"
    try:
        sock.connect((host, 80))
    except BlockingIOError:
        # print("Blocking Error!")
        pass

    request = f"GET / HTTP/1.0\r\nHost: {host}\r\n\r\n"
    data = request.encode("ascii")

    while True:
        try:
            sock.send(data)
            break
        except OSError:
            # print("No.1 OS Error!")
            pass

    response = b''
    while True:
        try:
            chunk = sock.recv(4096)
            while chunk:
                response += chunk
                chunk = sock.recv(4096)
            break
        except OSError:
            # print("No.2 OS Error!")
            pass

    return response


def sync_way():
    for i in range(10):
        print(nonblocking_way(), flush=True)


if __name__ == '__main__':
    import time

    start_time = time.time()
    sync_way()
    print("Use time -> {}'s.".format(time.time() - start_time))
