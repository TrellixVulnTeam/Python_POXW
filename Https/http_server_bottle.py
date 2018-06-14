#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ${}
@time: 2017/7/30 8:32
@version: v1.0 
"""
from bottle import route, run, static_file, request


@route('/hello/:name')
def HelloWorld(name="world"):
    return "hello" + name


@route("/download/:filename")
def Download(filename):
    return static_file(filename, root=u'../WebSpider/taobao_model/LadysImage/安琪儿_28_杭州市', download=filename)


@route("/postfile", method="POST")
def PostFile():
    file = request.POST.get('files')
    with open("1", "wb") as f:
        f.write(file)
    return '{"result": 0}'


if __name__ == "__main__":
    run(host='127.0.0.1', port=80)
