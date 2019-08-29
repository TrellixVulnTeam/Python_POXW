"""
@file: 3.mix_gen_coroutine_and_thread_executor.py
@time: 2019/8/29
@author: alfons
"""
import time

import asyncio

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


class ExecutorWithGen(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    @run_on_executor
    def sleep(self, second):
        gen.sleep(second)
        return second

    @gen.coroutine
    def get(self, *args, **kwargs):
        second = yield self.sleep(5)
        self.write("noblocking Request: {}".format(second))


class Executor(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(4)

    def func_y(self):
        for i in range(10):
            yield i

    async def sleep(self, second):
        # time.sleep(second)
        for i in self.func_y():
            pass

        await asyncio.sleep(second)
        return second

    @gen.coroutine
    def get(self, *args, **kwargs):
        second = yield self.executor.submit(self.sleep, second=5)
        self.write("noblocking Request: {}".format(second))


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/noblock', ExecutorWithGen),
        (r'/executor', Executor),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
