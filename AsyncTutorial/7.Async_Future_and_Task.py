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
    """可以理解为每个执行步骤的载体，yield语句返回的结果，起占位作用"""
    def __init__(self):
        self.result = None
        self._callbacks = []

    def add_done_callback(self, step):
        self._callbacks.append(step)

    def set_result(self, result):
        self.result = result
        for step in self._callbacks:      # 每次set_result后，都会启动回调函数，这里的回调函数其实是Task中step方法，这会形成了一个调用环，每次调用完后，转到下一个yield语句处
            step(self)


class Runner:
    """发动机"""
    def __init__(self, coro):
        self.coro = coro

    def run(self):
        print("run run run")
        f = Future()
        f.set_result(None)
        self.step(f)        # 3 coro为一个生成器，这一步，其实就是为了 send(None) 给 #2 处的生成器

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)     # 4 返回result结果，将暂停的生成器继续启用，并接收 Future实例，调用完后，程序主体跳转到下一个yield语句处
        except StopIteration:
            return
        next_future.add_done_callback(self.step)        # 6 next_future为 下一个生成器返回的 Future实例


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        print("dasdasddasdas")
        try:
            sock.connect((self.url, 80))
        except BlockingIOError:
            pass

        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f     # 2 此处主要是占位，运行至此时，函数将控制权交还给上一级

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
            chunk = yield f             # 5 此处为真正的调用主体，每次会返回Future实例，这里的Future实例的作用实际是返回sock读取的内容
                                        # 此处在循环中，所以会不停的返回 Future实例，直到从服务器接收完所有的信息
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
        event = selector.select()       # 每次都会选出那些已经触发的事件，下面则进行回调函数的触发
        for event_key, event_mask in event:
            callback = event_key.data
            callback()      # 回调函数可以是


if __name__ == '__main__':
    import time

    start_time = time.time()
    for _ in range(urls_todo):
        crawler = Crawler("baidu.com")
        runner = Runner(crawler.fetch())
        runner.run()        # 1 此处运行至 #2 处，传入Task的参数是一个 生成器 gen，此时已经完成了socket connect步骤

    loop()      # 事件循环开始，会根据注册的事件响应，回调对应的函数。开始时，事件只有socket connect由服务器返回结果的事件

    print("Use time -> {}'s.".format(time.time() - start_time))
