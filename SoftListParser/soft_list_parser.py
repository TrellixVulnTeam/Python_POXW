"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : soft_list_parser.py
 @Time    : 2019/3/26 10:01
"""
import json

soft_sum = dict()

with open("./soft_list.txt", 'r', encoding="utf-8") as f:
    for soft in f.readlines():
        soft_name = soft.split('-', maxsplit=2)[0]
        if soft_name in soft_sum:
            soft_sum[soft_name] += 1
        else:
            soft_sum[soft_name] = 0
soft_sum = sorted(soft_sum.items(), key=lambda item: item[1])

with open("soft_res.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(soft_sum))
