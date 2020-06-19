#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: fastapi_test.py
# Author: alfons
# LastChange:  2020/6/16 下午5:28
#=============================================================================
"""
import time
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    time.sleep(30)
    return "Hello world"


@app.get("/items/{item_id}")
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

uvicorn.run(app, host="0.0.0.0")