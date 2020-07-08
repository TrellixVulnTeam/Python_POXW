#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: fastapi_query_path_test.py
# Author: alfons
# LastChange:  2020/6/30 上午10:05
#=============================================================================
"""
import uvicorn
from typing import Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, Path, Query

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]


class User(BaseModel):
    username: str
    full_name: Optional[str]


@app.get("/items/{item_id}")
async def read_items(
        item_args: Item,
        user_args: User,
        item_id: int = Path(..., title="The ID of the item to get"),
        # q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)


if __name__ == '__main__':
    main()
