#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ResultTogether.py 
@time: 2018/4/9 16:54 
@version: v1.0 
"""

import os
import json

# dir_name = "E:/SignatureAnalysis/result"
# result_list = [os.path.join(dir_name, f) for f in os.listdir(dir_name) if f[f.rfind(".") + 1:] == "json"]
#
# result_dict = dict()
# for result_file in result_list:
#     result_name = os.path.basename(result_file)
#     with open(result_file, "r") as f:
#         result_dict.update({result_name: json.loads(f.read())})
#
# with open(os.path.join(os.path.dirname(dir_name), "result.json"), "w") as f:
#     f.write(json.dumps(result_dict))
# pass

import shutil

dir_name = "E:/SignatureAnalysis/pcap"

file_list = [os.path.join(dir_name, f) for f in os.listdir(dir_name) if f[f.find("."):] == ".pcap.pcap"]
for file in file_list:
    tmp_name = file[:file.rfind('.')]
    shutil.move(file, tmp_name)
pass
