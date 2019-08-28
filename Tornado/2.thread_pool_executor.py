"""
@file: 2.thread_pool_executor.py
@time: 2019/8/28
@author: alfons
"""
import time
import logging

import tornado.ioloop
import tornado.web
import tornado.options

from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.write("Hello World!")
        self.finish()


class NoBlockingHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)  # 此处必须为executor，在 run_on_executor 装饰器函数中，会在self中获取executor属性，

    @run_on_executor
    def sleep(self, second):
        time.sleep(second)
        return second

    @gen.coroutine
    def get(self, *args, **kwargs):
        second = yield self.sleep(5)
        self.write("noblocking Request: {}".format(second))


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/noblock', NoBlockingHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
