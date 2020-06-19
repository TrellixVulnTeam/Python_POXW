#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: flask_test.py
# Author: alfons
# LastChange:  2020/6/19 下午2:25
#=============================================================================
"""
import time
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    time.sleep(3)
    return "Hello world"


@app.route("/items/{item_id}")
def read_item(item_id: str, q: str = None, short: bool = False):
    """

    :param item_id:
    :param q:
    :param short:
    :return:
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


app.run(host="0.0.0.0", port=8000)
