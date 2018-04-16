#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ${}
@time: 2017/7/30 8:32
@version: v1.0 
"""
from bottle import route
from bottle import run
from bottle import static_file


@route('/hello/:name')
def HelloWorld(name = "world"):
    return "hello" + name


@route("/download/:filename")
def Download(filename):
    return static_file(filename, root = u'../WebSpider/taobao_model/LadysImage/安琪儿_28_杭州市', download = filename)


if __name__ == "__main__":
    run(host = '127.0.0.1', port = 8080)
