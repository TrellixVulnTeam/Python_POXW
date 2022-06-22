#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: performance_test.py
@time: 2020/6/19
@author: alfons
"""
import asyncio
import time
import requests
import httpx
import aiohttp
from multiprocessing.pool import ThreadPool

REQUEST_GET = "get"
REQUEST_POST = "post"

total_num = 0

# ----------------- aiohttp -----------------
# aiohttp_session = aiohttp.ClientSession(
#     headers={"Content-Type": "application/json; charset=UTF-8"},
#     # timeout=5,
# )


async def aiohttp_request(url: str = None, num: int = None):
    start_time = time.time()

    # async with aiohttp_session.get(url) as response:
    #     response = await response.read()

    async with aiohttp.ClientSession(
            headers={"Content-Type": "application/json; charset=UTF-8"},
            # timeout=5,
    ) as session:
        async with session.get(url) as response:
            response = await response.read()

    global total_num
    total_num += 1

    print(f"{num} time use {time.time() - start_time}'s: {response} ")


def aiohttp_test():
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(asyncio.gather(
        *[
            aiohttp_request(f"http://10.10.100.65:9090/api/v1/query?query=node_time%7Btid%3D%27100006%27%2Cjob%3D%27Host%27%2Cexporter%3D%27host%27%7D&time=1647338807.366", i)
            for i in range(1000)]
    ))

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


# ----------------- httpx -----------------
prometheus_session = httpx.AsyncClient(
    headers={"Content-Type": "application/json; charset=UTF-8"},
    timeout=5,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=100),
)


async def httpx_request(url: str = None, num: int = None):
    start_time = time.time()
    response = await prometheus_session.get(url)

    # async with httpx.AsyncClient(
    #     headers={"Content-Type": "application/json; charset=UTF-8"},
    #     timeout=5,
    # ) as session:
    #     response = await session.get(url)

    global total_num
    total_num += 1

    print(f"{num} time use {time.time() - start_time}'s: {response.content} ")


def httpx_test():
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(asyncio.gather(
        *[
            httpx_request(f"http://10.10.100.65:9090/api/v1/query?query=node_time%7Btid%3D%27100006%27%2Cjob%3D%27Host%27%2Cexporter%3D%27host%27%7D&time=1647338807.366", i)
            for i in range(1000)]
    ))

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


# ----------------- request -----------------
def func_request(method: str = REQUEST_GET, url: str = None, num: int = None):
    if method == REQUEST_GET:
        time_start = time.time()
        response = requests.get(url)
        global total_num
        total_num += 1

        print(f"{num} time use {time.time() - time_start}'s: {response.content}.")


def request_test():
    start_time = time.time()
    with ThreadPool(1000) as pool:

        for i in range(5):
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_time", i))
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/sync_time", i))
            # pool.apply_async(
            #     func_request,
            #     (REQUEST_GET, f"http://127.0.0.1:9090/api/v1/query?query=node_time%7Btid%3D%27100006%27%2Cjob%3D%27Host%27%2Cexporter%3D%27host%27%7D&time=1647338807.366", i)
            # )
            pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_with_sync_time", i))
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/run_sync_as_async_time", i))
            # pool.apply_async(func_request, (REQUEST_GET, f"http://127.0.0.1:8000/async_with_thread_time", i))

        pool.close()
        pool.join()

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


if __name__ == '__main__':
    # aiohttp_test()
    # httpx_test()
    request_test()
