#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: server.py
@time: 2020/5/22
@author: alfons
"""
from flask import Flask, request

app = Flask(__name__)


@app.route('/sms/v2/send-same', methods=["post"])
def hello_world():
    print request.content_type
    print request.data
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
