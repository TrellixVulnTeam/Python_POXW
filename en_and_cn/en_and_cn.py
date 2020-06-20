#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: en_and_cn.py
@time: 2020/5/18 下午10:58
@version: v1.0 
"""
from __future__ import unicode_literals

import sys
from prompt_toolkit import prompt

text = prompt('Give me some input: ')
print('You said: %s' % text)

def translate(file_path_list):
    context_list = list()
    for file_path in file_path_list:
        with open(file_path, 'rb') as f:
            context_list.append([s.strip() for s in f.readlines() if s.strip()])

    context_dst_list = list()
    if context_list:
        for j in range(len(context_list[0])):
            for i in range(len(context_list)):
                context_dst_list.append(context_list[i][j])
            context_dst_list.append("\n")

    with open("./vv.txt", 'wb') as f:
        f.write('\n'.join(context_dst_list))


if __name__ == '__main__':
    translate(sys.argv[1:])
