"""
@file: 2.Sync_MultiProcess.py
@time: 2019/8/22
@author: alfons
"""
import socket
from concurrent import futures


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


def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as executor:
        futs = {executor.submit(blocking_way) for i in range(workers)}
    return len([fut.result() for fut in futs])


if __name__ == '__main__':
    import time

    start_time = time.time()
    process_way()
    print("Use time -> {}'s.".format(time.time() - start_time))
