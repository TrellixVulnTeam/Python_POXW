#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: httpx_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/2/3 11:17 上午
# History:
#=============================================================================
"""
import json
from typing import Dict
import asyncio
import httpx


async def test_oracle_encrypt():
    url = f"http://127.0.0.1:9101/encrypt"
    auth_json: Dict[str, str] = {
        "username": "db_username",
        "password": "db_password",
    }
    post_value: Dict[str, str] = {
        "value": json.dumps(auth_json)
    }
    async with httpx.AsyncClient(verify=False) as client:
        res = (await client.post(
            url=url,
            content=json.dumps(post_value),
        )).json()
        print(res)
        return res


async def test_oracle_decrypt(ciphertext:str):
    url = f"http://127.0.0.1:9101/decrypt"
    post_value: Dict[str, str] = {
        "value": ciphertext
    }
    async with httpx.AsyncClient(verify=False) as client:   # type: httpx.AsyncClient
        res = (await client.post(
            url=url,
            content=json.dumps(post_value),
        )).json()
        print(res)
        return res


if __name__ == '__main__':
    res = asyncio.run(test_oracle_encrypt())
    asyncio.run(test_oracle_decrypt(res["data"]))
