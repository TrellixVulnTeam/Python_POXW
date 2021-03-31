#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: rich_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/2 5:17 下午
# History:
#=============================================================================
"""

from rich import print, get_console
from rich.prompt import Confirm, IntPrompt, Prompt

if __name__ == '__main__':
    console = get_console()

    console.log(
        "JSONRPC [i]request[/i]",
        5,
        1.3,
        True,
        False,
        None,
        {
            "jsonrpc": "2.0",
            "method": "subtract",
            "params": {"minuend": 42, "subtrahend": 23},
            "id": 3,
        },
    )

    console.log("Hello, World!", "{'a': 1}", repr(console))
    console.input(prompt="fdsa abdf")
    console.log("foo")
