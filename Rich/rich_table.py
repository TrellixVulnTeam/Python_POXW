#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: rich_table.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/12/29 2:42 PM
# History:
#=============================================================================
"""
from typing import List,Optional

from rich.console import (
    Console,
    ConsoleOptions,
    JustifyMethod,
    OverflowMethod,
    RenderableType,
    RenderResult,
)
from rich.highlighter import ReprHighlighter
from rich.table import Table
from rich.segment import Segment
from rich.text import TextType
from rich.style import StyleType, Style


class MyTable(Table):


    def set_subtitle(
            self,
            subtitle: str,
            subtitle_style:Optional[StyleType] = None,
            subtitle_justify:"JustifyMethod" = "left",
    ) -> None:
        self.subtitle = subtitle
        self.subtitle_style = subtitle_style
        self.subtitle_justify = subtitle_justify

    def __rich_console__(
            self, console: "Console", options: "ConsoleOptions"
    ) -> "RenderResult":

        if not self.columns:
            yield Segment("\n")
            return

        max_width = options.max_width
        if self.width is not None:
            max_width = self.width

        extra_width = self._extra_width
        widths = self._calculate_column_widths(
            console, options.update_width(max_width - extra_width)
        )
        table_width = sum(widths) + extra_width

        render_options = options.update(
            width=table_width, highlight=self.highlight, height=None
        )

        def render_annotation(
                text: TextType, style: StyleType, justify: "JustifyMethod" = "center"
        ) -> "RenderResult":
            render_text = (
                console.render_str(text, style=style, highlight=False)
                if isinstance(text, str)
                else text
            )
            return console.render(
                render_text, options=render_options.update(justify=justify)
            )

        if self.title:
            yield from render_annotation(
                self.title,
                style=Style.pick_first(self.title_style, "table.title"),
                justify=self.title_justify,
            )
        if hasattr(self, "subtitle"):
            yield from render_annotation(
                self.subtitle,
                style=Style.pick_first(self.subtitle_style,"table.caption"),
                justify=self.subtitle_justify,
            )
        yield from self._render(console, render_options, widths)
        if self.caption:
            yield from render_annotation(
                self.caption,
                style=Style.pick_first(self.caption_style, "table.caption"),
                justify=self.caption_justify,
            )


table = MyTable(
    title="Star Wars Movies",
    caption="Rich example table",
    caption_justify="right",
    show_footer=True,
)

table.set_subtitle(subtitle="SN: fadsafas-201-321312")
table.add_column("Released", header_style="bright_cyan", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row(
    "Dec 20, 2019",
    "Star Wars: The Rise of Skywalker",
    "$952,110,690",
)
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. V111: The Last Jedi",
    "$1,332,539,889",
    style="on black",
    end_section=True,
)
table.add_row(
    "Dec 16, 2016",
    "Rogue One: A Star Wars Story",
    "$1,332,439,889",
)

c = Console()
highlight = ReprHighlighter()
c.print(table, justify="center")
