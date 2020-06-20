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
from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    time.sleep(0.003)
    return "Hello world"


@app.route("/items/<item_id>")
def read_item(item_id: str):
    """

    :param item_id:
    :return:
    """
    item = {"item_id": item_id}

    q = request.args.get("q")
    if q:
        item.update({"q": q})

    short = request.args.get("short")
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


app.run(host="0.0.0.0", port=8000)
