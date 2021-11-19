#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: tasks.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/6/23 4:17 下午
# History:
#=============================================================================
"""
from invoke import task, Context


@task(help={'name': "Name of the person to say hi to."})
def hi(ctx, name):
    """
    Say hi to someone.
    """
    ctx.run("ls -l")


if __name__ == '__main__':
    from invoke import Collection, Program

    coll = Collection()
    coll.add_task(task=hi)
    program = Program(namespace=coll, version='0.1.0')
    program.run("nv hi name=hal")
