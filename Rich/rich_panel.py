#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: rich_panel.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/10/12 3:38 下午
# History:
#=============================================================================
"""
from rich import box
from rich.console import RenderableType, RenderGroup
from rich.panel import Panel
from rich.style import Style
from rich.table import Table

from rich import print
from rich.panel import Panel
from rich.box import DOUBLE
from rich.table import Table
from rich.console import Console
from rich.box import (
    ASCII,
    ASCII2,
    ASCII_DOUBLE_HEAD,
    SQUARE,
    SQUARE_DOUBLE_HEAD,
    MINIMAL,
    MINIMAL_HEAVY_HEAD,
    MINIMAL_DOUBLE_HEAD,
    SIMPLE,
    SIMPLE_HEAD,
    SIMPLE_HEAVY,
    HORIZONTALS,
    ROUNDED,
    HEAVY,
)


def format_title(title):
    table = Table(
        title=title,
        show_lines=True,
        box=box.ASCII,
        header_style=Style(color="blue", bold=True),
        title_style=Style(color="#ffffff", bgcolor="deep_sky_blue3", bold=True, frame=True),
    )


def format_version_output(
        title: str,
        data_dict,
        box,
) -> Panel:
    """
    将version函数的输出结果转换成rich的Panel对象
        ╭─ Client ───────────────────────────────╮
        │ Version:           v8.0.0              │
        │ Git commit:        e0cc403             │
        │ Python version:    3.8.6               │
        │ Built:             2021-06-30 14:18:51 │
        ╰────────────────────────────────────────╯
        ╭─ Server ───────────────────────────────╮
        │ Version:           v8.0.0              │
        │ Git commit:        f810a83             │
        │ API version:       v1, v2              │
        │ Python version:    3.8.6               │
        │ Plugins:           qvote               │
        │ Built:             2021-06-30 10:37:23 │
        ╰────────────────────────────────────────╯
    :param title: version信息标题
    :param data_dict: version信息
    :return:
    """
    grid = Table.grid(expand=False)
    grid.add_column(justify="left")
    grid.add_column(width=4)
    grid.add_column(justify="left")

    for k, v in data_dict.items():
        if isinstance(v, (list, set)):
            v = ", ".join([str(item) for item in v])
        if v:
            assert isinstance(v, str), "Rendering value must be a str."

        grid.add_row(k, "", v)

    return Panel(
        grid,
        box=box,
        title=f"[bold]{title}",
        title_align="left",
        expand=False,
    )


c = Console()

c.print(format_title(title="hello"))

# for box in [
#     ROUNDED,
# ]:
#     c.print()
#     c.print(format_version_output(
#         title="[blue]Raid Controller",
#         box=box,
#         data_dict={
#             "PCIe Slot": "0",
#         }
#     ))
#     c.print(format_version_output(
#         box=box,
#         title="[blue]Basic Information",
#         data_dict={
#             "Product Name": "PERC H730P Mini",
#             "Serial No": "75A03BO",
#             "FW Package Build": "25.5.3.0005",
#             "Current Time": "7:33:44 10/12, 2021",
#             "BBU": "Yes",
#             "Memory": "Present",
#             "Memory Size": "2048MB",
#             "Auto Rebuild": "Enabled",
#             "ROC temperature": "41  degree Celsius",
#             "Controller temperature": "41  degree Celcius",
#             "Driver Name": "megaraid_sas",
#             "Driver Version": "07.703.06.00",
#         }
#     ))
#     c.print(format_version_output(
#         box=box,
#         title="[blue]BBU Properties",
#         data_dict={
#             "Voltage": "3932 mV",
#             "Current": "0 mA",
#             "Temperature": "25 C",
#             "Battery State": "Optimal",
#             "Remaining Capacity": "517 mAh",
#             "Full Charge Capacity": "520 mAh",
#             "Auto Learn Period": "90 Days",
#             "Next Learn time": "Wed Nov  3 11:35:20 2021",
#             "Learn Delay Interval": "0 Hours",
#             "Auto-Learn Mode": "Transparent",
#         }
#     ))
