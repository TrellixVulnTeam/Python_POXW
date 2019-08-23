"""
@file: web.py
@time: 2019/8/2
@author: alfons
"""
import logging
import tornado.ioloop
import tornado.web
from tornado import gen
from tornado.concurrent import Future
from tornado.escape import json_decode, json_encode

logger = logging.getLogger(__name__)


def future(f):
    r = Future()
    r.set_result(f)
    return r


class MainHandler(tornado.web.RequestHandler):
    def _return(self):
        yield future({"a": 3})
        return {"b": 4}

    @gen.coroutine
    def get(self):
        # if not self.current_user:
        #     logger.error("can not get current user")
        #     self.write("Need login")

        a = yield from self._return()
        print(a)
        self.write("Hello, world")


class Login(tornado.web.RequestHandler):
    def get(self):
        self.write("You are login!")


class Returnhandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        response = yield future({"fetch": "it's ok"})
        self.write(gen.Return(json_encode(response)))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", Login),
    (r"/return", Returnhandler),
])

settings = {
    "login_url": "/login",
    "debug": True,
}

if __name__ == "__main__":
    get = MainHandler.get
    print(dir(get))
    code = get.__code__
    print(dir(code))
    for co in dir(code):
        if not co.startswith('co'):
            continue
        print("{name} -> {value}".format(name=co, value=getattr(code, co)))

    application.settings = settings
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
