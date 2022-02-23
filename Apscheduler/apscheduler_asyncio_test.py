#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: apscheduler_asyncio_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/3/31 10:19 上午
# History:
#=============================================================================
"""
from functools import partial


class Foo(partial):
    def __ror__(self, other):
        return self(other)


import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler


def sync_time_sleep(task_id, timeout):
    print(f"sync {task_id=} begin\n")
    time.sleep(timeout)
    print(f"sync {task_id=} end\n")


async def async_time_sleep(task_id, timeout):
    print(f"async {task_id=} begin")
    await asyncio.sleep(timeout)
    print(f"async {task_id=} end")


scheduler = AsyncIOScheduler()
for i in range(10):
    print(scheduler.add_job(func=sync_time_sleep,
                            args=(i, 10), ))

for i in range(10):
    print(scheduler.add_job(func=async_time_sleep,
                            args=(i, 1), ))
scheduler.start()

asyncio.get_event_loop().run_forever()
asyncio.get_event_loop().run_forever()
