#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: clickTest.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/7/16 4:12 下午
# History:
#=============================================================================
"""
import click


@click.group()
@click.option('-i', '--input', default=23)
def cli(input):
    return 42


@cli.result_callback()
def process_result(result, input):
    return result + input


if __name__ == '__main__':
    cli()
