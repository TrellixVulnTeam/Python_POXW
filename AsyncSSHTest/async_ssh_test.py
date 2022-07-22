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


def gen_ws_name(*args, **kwargs) -> str:
    """
    生成websocket特征名

    :return:
    """
    return "_".join(list(args) + list(kwargs.values()))

res = gen_ws_name()
print(res)