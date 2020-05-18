#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: en_and_cn.py
@time: 2020/5/18 下午10:58
@version: v1.0 
"""
import os

src_dir = "./src_files"

file_path_list = [os.path.join(src_dir, file_name) for file_name in os.listdir(src_dir)]

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

with open("en_and_cn.txt", 'wb') as f:
    f.write('\n'.join(context_dst_list))

