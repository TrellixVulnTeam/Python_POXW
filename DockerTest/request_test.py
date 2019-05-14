"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : request_test.py
 @Time    : 2019/2/15 17:52
"""
from threading import Thread
import requests

url = "http://192.168.2.68:6301/helloworld"


def Request(t_id):
    content = requests.get(url).content
    if b"APP1" in content:
        print("{} --> Get Hi: b'Helloworld-APP1'".format(t_id))
    elif b"APP2" in content:
        print("{} --> Get Hi: b'Helloworld-APP2'".format(t_id))


if __name__ == '__main__':
    # Request()

    thread_list = list()
    for i in range(2 ** 20):
        t = Thread(target=Request, name="thread{}".format(i), args=(i,))
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()
