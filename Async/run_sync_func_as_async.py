#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: run_sync_func_as_async.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/2/18 4:08 PM
# History:
#=============================================================================
"""
import os
import typing
from typing import Any
import concurrent.futures
import functools
import asyncio
import time
import threading

# 线程执行器，线程数量 = CPU数量 * 10
thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=(os.cpu_count() or 10) * 10)


def run_in_executor(func) -> typing.Any:
    """
    改造同步函数或方法，使之变成异步函数。

    使用方法：
        @run_in_executor
        def sync_func(args_a, args_time: int):
            time.sleep(args_time)
            return args_a

        async def run():
            return await sync_func("hello world", args_time=3)

    注意事项：使用该装饰器装饰后，所装饰的函数或方法只能以异步方式执行
    """

    @functools.wraps(func)
    async def wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        is_coroutine = asyncio.iscoroutinefunction(func)

        if is_coroutine:
            return await func(*args, **kwargs)
        else:
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(thread_executor, lambda: func(*args, **kwargs))

    return wrapper


async def run_as_async(func: typing.Any, *args: Any, **kwargs: Any) -> Any:
    """
    在异步方法中，使用await改造同步方法

    使用方法:
        def func_A(timeout: int):
            time.sleep(timeout)

        async def func_B(timeout: int):
            await run_as_async(func_A, timeout)
            await run_as_async(func_A, timeout=timeout)

    :param func: 执行的同步方法
    :param args: 请求参数
    :param kwargs: 请求参数
    :return:
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(thread_executor, lambda: func(*args, **kwargs))


async def run_parallel(
        async_funcs,
        loop=None,
        return_exceptions: bool = False,
):
    """
    并发执行多个异步方法，以节省时间消耗。

    需要注意的是，并发执行多个异步方法，在执行结束之后不会返回全部的结果。需要通过传入的参数进行获取

    async def func(a):
        ...

    await run_parallel(coros_or_futures=[func(i) for i in range(100)])

    :param async_funcs: 异步方法
    :param loop: 事件循环
    :param return_exceptions: 是否在执行异常时返回
    :return:
    """
    return await asyncio.gather(
        *async_funcs,
        loop=loop,
        return_exceptions=return_exceptions,
    )


def run_in_threadsafe(coro):
    def get_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    new_loop = asyncio.new_event_loop()  # 在当前线程下创建时间循环，（未启用），在start_loop里面启动它
    t = threading.Thread(target=get_loop, args=(new_loop,))  # 通过当前线程开启新的线程去启动事件循环
    t.start()

    fut = asyncio.run_coroutine_threadsafe(coro, new_loop)  # type: asyncio.Future
    return fut.result()


async def hello1():
    print(f"Hello world 01 begin,my thread is:{threading.currentThread()}")
    await asyncio.sleep(3)
    print("Hello again 01 end")


async def hello2():
    print(f"Hello world 02 begin,my thread is:{threading.currentThread()}")
    await asyncio.sleep(2)
    print("Hello again 02 end")

    return 2


@run_in_executor
def hello4():
    print(f"Hello world 04 begin,my thread is:{threading.currentThread()}")
    import time
    time.sleep(4)
    print("Hello again 04 end")


async def hello3():
    print(f"Hello world 03 begin,my thread is:{threading.currentThread()}")

    # await hello2()
    # await hello1()

    print(run_in_threadsafe(hello2()))

    # await run_parallel([hello2(), hello1(), hello4()])

    print("Hello again 03 end")


def main():
    a = time.time()
    loop = asyncio.get_event_loop()
    tasks = [hello3()]
    loop.run_until_complete(asyncio.wait(tasks))

    loop.close()

    print(f"Time use -> {time.time() - a}'s.")


if __name__ == '__main__':
    main()
