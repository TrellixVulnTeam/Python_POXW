"""
@file: 1.web_asynchronous_gen_coroutine.py
@time: 2019/8/28
@author: alfons
"""
import time
import logging

import tornado.ioloop
import tornado.web
import tornado.options

from tornado import gen

tornado.options.parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        self.write("Hello World!")
        self.finish()


class NoBlockingHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        yield gen.sleep(10)     # 此处yield右侧的方法或函数必须是非阻塞的，否则程序仍是阻塞状态，会卡在里面
        self.write("No Blocking Request")


class BlockingHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(10)
        #for i in range(2**100):
        #    pass
        self.write("Blocking Request")


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/noblock', NoBlockingHandler),
        (r'/block', BlockingHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
