#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: socket_client_with_select.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/6/7 10:35
# History:
#=============================================================================
"""
import time
import socket
from multiprocessing.pool import ThreadPool

total_num = 0

messages = [
    'This is the message ',
    'It will be sent ',
    'in parts ',
]

server_address = ('localhost', 8090)


def _send_to_server(i: int):
    try:

        # Create aTCP/IP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect thesocket to the port where the server is listening
        print('connecting to %s port %s' % server_address)

        # 连接到服务器
        s.connect(server_address)

        for index, message in enumerate(messages):
            # Send messages on both sockets
            print('%s: sending "%s"' % (s.getsockname(), message + str(i) + '-' + str(index)))
            s.send((message + str(index)).encode('utf-8'))
            # Read responses on both sockets

        data = s.recv(1024)
        print('%s: received "%s"' % (s.getsockname(), data))
        if data != "":
            print('closing socket', s.getsockname())
            s.close()
    except Exception as e:
        print(f"Error: {e}")

    global total_num
    total_num += 1


def send_test():
    start_time = time.time()
    with ThreadPool(1000) as pool:
        for i in range(10 ** 4):
            pool.apply_async(_send_to_server, (i,))
            # pool.apply_async(
            #     func_request,
            #     (REQUEST_GET, f"http://127.0.0.1:9090/api/v1/query?query=node_time%7Btid%3D%27100006%27%2Cjob%3D%27Host%27%2Cexporter%3D%27host%27%7D&time=1647338807.366", i)
            # )
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_with_sync_time", i))
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/run_sync_as_async_time", i))
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_with_thread_time", i))

        pool.close()
        pool.join()

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


if __name__ == '__main__':
    # aiohttp_test()
    # httpx_test()
    send_test()
