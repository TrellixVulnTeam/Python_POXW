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
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    time.sleep(3)
    return "Hello ld"


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


class Item(BaseModel):
    name: str
    description: str = None
    price: float = None
    tax: float = None


@app.post("/post/{post_id}")
def post_func(post_id: str, form_1: str = Form(default=None), form_2: str = Form(...)):
    item = {
        "post_id": post_id,
        "form_1": form_1,
        "form_2": form_2,
    }
    # if args1:
    #     item.update({"args1": args1})
    # if not short:
    #     item.update(
    #         {"description": "This is an amazing item that has a long description"}
    #     )
    return item


uvicorn.run(app=app, host="0.0.0.0", port=8000)
