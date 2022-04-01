#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: fastapi_async_and_sync_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/10/28 11:16 上午
# History:
#=============================================================================
"""
import concurrent.futures
import time
import asyncio
import uvicorn
import functools
from fastapi import FastAPI

# ----------------------------------------
app = FastAPI()
route = app.router


# -------------------- 同步接口，同步方法 --------------------
@route.get("/sync_time")
def sync_time():
    print("sync_time".center(64, "="))
    time.sleep(0.1)
    return "sync_time"


# -------------------- 异步接口，异步方法 --------------------
@route.get("/async_time")
async def async_time():
    print("async_time".center(64, "="))
    await asyncio.sleep(5)
    return "async_time"


# -------------------- 异步接口，同步方法 --------------------
@route.get("/async_with_sync_time")
async def async_time():
    print("async_with_sync_time".center(64, "="))
    time.sleep(5)
    return "async_with_sync_time"


thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=12800)


async def run_as_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(thread_executor, lambda: func(*args, **kwargs))


@route.get("/run_sync_as_async_time")
async def async_time():
    print("async_with_sync_time".center(64, "="))
    # time.sleep(5)
    await run_as_async(time.sleep, 5)
    return "run_sync_as_async_time"


# -------------------- 使用线程池模拟异步 --------------------
def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(thread_executor, lambda: f(*args, **kwargs))

    return inner


@run_in_executor
def thread_time_sleep(time_out: int):
    time.sleep(time_out)


@route.get("/async_with_thread_time")
async def async_time():
    print("async_with_thread_time".center(64, "="))
    await thread_time_sleep(5)
    return "async_with_thread_time"


@route.on_event("startup")
def add_thread_pool():
    loop = asyncio.get_running_loop()
    loop.set_default_executor(thread_executor)


def main():
    asyncio.to_thread()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        loop="asyncio",
    )


if __name__ == '__main__':
    main()
