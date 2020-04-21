#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: re_replace.py
@time: 2020/4/15
@author: alfons
"""
import re
print "get_raid_ctrl_cli -> {}".format(None)
with open("./cmd.json", "r") as f:
    res = f.read()


def replace(match_obj):
    """

    :param re. match_obj:
    :return:
    """
    m_tuple = match_obj.groups()
    return "[{}]".format(''.join([m.strip() for m in m_tuple]))


res = re.sub("\[(\n.*)\]", replace, res)
res = re.sub("\[(\n.*)(\n.*)\]", replace, res)
res = re.sub("\[(\n.*)(\n.*)(\n.*)\]", replace, res)
res = re.sub("\[(\n.*)(\n.*)(\n.*)(\n.*)\]", replace, res)
res = re.sub("\[(\n.*)(\n.*)(\n.*)(\n.*)(\n.*)\n\]", replace, res)
with open("mcd_new.json", "w") as f:
    f.write(res)
pass
