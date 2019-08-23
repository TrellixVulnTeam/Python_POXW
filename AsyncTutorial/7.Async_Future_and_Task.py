"""
@file: 7.Async_Future_and_Task.py
@time: 2019/8/23
@author: alfons
"""
import sys
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stop = False
urls_todo = 10


class Future:
    """可以理解为执行结果的载体"""
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, fn):
        self._callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callbacks:
            fn(self)


class Task:
    """启动Future实例"""
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)        # 这一步，其实就是为了 send(None) 给yield

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)

        try:
            sock.connect((self.url, 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f     # 此处主要是占位，起控制作用

        selector.unregister(sock.fileno())
        get = "GET / HTTP/1.0\r\nHost: {}\r\n\r\n".format(self.url)
        sock.send(get.encode("ascii"))

        global stop
        global urls_todo
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)       # 注册及下面的取消注册为的是触发sock读事件
            chunk = yield f             # 此处为真正的调用主体，每次会返回Future实例，这里的Future实例的作用实际是返回sock读取的内容
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
            else:
                urls_todo -= 1
                if not urls_todo:
                    stop = True
                break

        print(self.response)
        sys.stdout.flush()


def loop():
    while not stop:
        event = selector.select()
        for event_key, event_mask in event:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time

    start_time = time.time()
    for _ in range(urls_todo):
        crawler = Crawler("baidu.com")
        Task(crawler.fetch())

    loop()

    print("Use time -> {}'s.".format(time.time() - start_time))
