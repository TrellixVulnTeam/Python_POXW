#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: async_ssh_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/6/22 17:31
# History:
#=============================================================================
"""
import asyncio
import asyncssh
from asyncssh import SSHClientConnection


async def test_asyncssh():
    async with asyncssh.connect(
        '10.10.90.78',
        port=22,
        username='root',
        password='Cljslrl0620!!',
    ) as conn:  # type: SSHClientConnection
        res = await conn.run('ls ', input="/tmp")
        print(res)


if __name__ == '__main__':
    asyncio.run(test_asyncssh())
