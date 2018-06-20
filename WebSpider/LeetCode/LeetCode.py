#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : LeetCode.py
 @Time    : 2018/6/19 9:12
"""
import re

patten = """<tr>(.*?\n)+?.*>(\d+)</td>.*\n.*value="(.*?)"(.*?\n)+?.*?href="(.*?)"(.*?\n)+?.*?span.*?>(.*?)</span>"""

with open("./LeetCode.html", "r") as f:
    content = f.read()
    results = re.findall(patten, content)

with open("leetcode.md", "w") as f:
    f.write("|#|Title|Difficulty|C++|Python|\n|:---:|:---|:---|:---|:---|\n")
    for result in results:
        f.write("|{number}|[{title}]({url})|{diff}|||\n".format(number=result[1],
                                                                title=result[2],
                                                                url="https://leetcode.com" + result[4] + "/description/",
                                                                diff=result[6]))
pass