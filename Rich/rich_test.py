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
from typing import Optional, List, Any

from rich import box
from rich.style import Style
from rich.prompt import Confirm
from rich.console import Console
from rich.table import Table


def print_table(title: str, cols: List[str], rows: List[List[Any]], ) -> None:
    """

    :param title:
    :param cols:
    :param rows:
    :return:
    """
    table = Table(
        title=title,
        show_lines=True,
        box=box.ASCII,
        header_style=Style(color="blue", bold=True),
        title_style=Style(bgcolor="deep_sky_blue3", bold=True, frame=True),
    )

    for col in cols:
        table.add_column(col, justify='center', overflow='fold')

    for row in rows:
        table.add_row(*row)

    Console().print(table)


print_table(title="Test Title",
            cols=["col_1", "col_2", "col_3", ],
            rows=[
                ["1", "2", '3'],
                ["4", "5", '6'],
                ["7", "8", '9']
            ])

from rich import print
from rich.console import RenderGroup
from rich.panel import Panel

Console().print(RenderGroup(
    Panel("Hello", style="on blue"),
    Panel("World", style="on red"),
))
