"""
@file: 6.Sync_callback.py
@time: 2019/8/23
@author: alfons
"""
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = False
urls_todo = 10


class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = None
        self.response = b''

    def fetch(self):
        """无穷无尽的回调"""
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect((self.url, 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)      # 写回调，对方服务器有返回时，会对socket的文件描述符产生变化，触发写回调

    def connected(self, key, mask):
        selector.unregister(key.fd)
        get = "GET / HTTP/1.0\r\nHost: {}\r\n\r\n".format(self.url)
        self.sock.send(get.encode("ascii"))
        selector.register(key.fd, EVENT_READ, self.read_response)       # 读回调，进行服务器返回值的处理

    def read_response(self, key, mask):
        global stopped
        global urls_todo

        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(key.fd)         # 接收结束后，注销socket的文件描述符
            urls_todo -= 1
            if not urls_todo:               # 如果所有的次数都用完了，则停止
                stopped = True


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)


if __name__ == '__main__':
    import time

    start_time = time.time()
    for i in range(urls_todo):
        crawler = Crawler("baidu.com")
        crawler.fetch()         # 这一步，其实是为了将后续的回调方法注册到selector中

    loop()
    print("Use time -> {}'s.".format(time.time() - start_time))