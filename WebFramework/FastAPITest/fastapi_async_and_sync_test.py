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
import sys
import time
import asyncio
import paramiko
import uvicorn
import functools
from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()
route = app.router


@route.get("/sync_time")
def sync():
    print("sync_time".center(64, "="))
    time.sleep(5)
    return "sync_time"


@route.get("/sync")
def sync():
    print("sync".center(64, "="))
    return "sync"


def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner


class SSH:
    def __init__(self):
        self.h = "hello world"

    # @run_in_executor
    def exec_cmd(self, cmd, timeout):
        print(self.h)
        client = paramiko.SSHClient()
        client.get_host_keys().clear()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname="10.10.100.218",
                       username="root",
                       port=22,
                       password="cljslrl0620",
                       look_for_keys=False
                       )
        _, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        print(stdout.read())
        print(stderr.read())
        return "async"


ssh = SSH()


@route.get("/sync_ssh")
def sync_ssh():
    print("sync_ssh".center(64, "="))
    return ssh.exec_cmd("ls /tmp && sleep 5", timeout=10)


# @route.get("/async_ssh")
# async def async_ssh():
#     print("async".center(64, "="))
#     return await ssh.exec_cmd("ls /tmp && sleep 5", timeout=10)


def main():
    uvicorn.run(app="fastapi_async_and_sync_test:app", host="0.0.0.0", port=8000, workers=10)
    # uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)


if __name__ == '__main__':
    main()
