#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: tornado_test.py
# Author: alfons
# LastChange:  2020/6/19 下午3:14
#=============================================================================
"""
import time
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(0.003)
        self.write("Hello, world")

# class ItemHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.request
#         item = {"item_id": item_id}
#         if q:
#             item.update({"q": q})
#         if not short:
#             item.update(
#                 {"description": "This is an amazing item that has a long description"}
#             )
#         return item


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
