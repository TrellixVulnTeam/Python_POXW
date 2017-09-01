#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: CentosSpider.py 
@time: 2017/8/28 9:11 
@version: v1.0 
"""
import requests
import re
import urllib

url = "https://mirrors.aliyun.com/epel/7/"

reponse = requests.get(url = url).content
pattern = re.compile('<a href="(.*?)">.*?</a>', re.S)
items = re.findall(pattern, reponse)

for item in items[1:]:
    second_url = url + item
    second_reponse = requests.get(url = second_url).content
    second_items = re.findall(pattern, second_reponse)
    for second_item in second_items[1:]:
        thr_url = second_url + second_item
        thr_reponse = requests.get(url = thr_url).content
        thr_items = re.findall(pattern, thr_reponse)
        for thr_item in thr_items[1:]:
            soft_url = thr_url + thr_item
            soft_name = thr_item
            str_line = soft_name + ":" + (80 - len(urllib.unquote(soft_name))) * " " + soft_url + "\n"
            # str_line = urllib.unquote(soft_name + "," + soft_url + "\n")
            with open("Epel_Soft_name.txt", "a+") as f:
                f.write(urllib.unquote(str_line))
            pass
