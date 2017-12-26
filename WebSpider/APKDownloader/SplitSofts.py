#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: SplitSofts.py 
@time: 2017/12/26 20:53 
@version: v1.0 
"""
import os
import json
import Convert_APKs_info


with open("test_softs.txt", "r") as f:
    total_test_softs = f.read().split("\n")

with open("soft_info.json", "r") as f:
    total_softs_info = json.loads(f.read())

for soft_dir in ["ChenYuan", "ShangGong", "WuTing"]:
    soft_list = os.listdir(soft_dir)
    for soft_file in soft_list:
        soft_name = soft_file[:-4]
        if soft_file[:-4] in total_test_softs:
            continue
        else:
            os.remove(os.path.join(soft_dir, soft_file))
            pass

    soft_info_dict = {file_name[:-4]: total_softs_info[file_name[:-4]] for file_name in os.listdir(soft_dir)}
    Convert_APKs_info.SoftInfoXlwt(soft_info_dict, os.path.join(soft_dir, soft_dir + ".xls"))
    pass
