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
import asyncio

async def run_as_async(func, *args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func=func, *args)

if __name__ == '__main__':
