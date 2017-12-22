#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: IM_soft_top_100.py 
@time: 2017/12/7 15:18 
@version: v1.0 
"""
import requests
import re
import json
from collections import OrderedDict

Similarweb_URL = "https://pro.similarweb.com/#/appcategory/leaderboard/Google/840/Communication/AndroidPhone/Top%20Grossing"

if __name__ == "__main__":
    # content = requests.get(Similarweb_URL).content
    with open("similarweb_top_free.html", "r") as f:
        content = f.read()

    soft_name = re.compile('<div class="swTable-content">(.*?)</div>', re.S)
    soft_name_list = re.findall(soft_name, content)
    soft_name_len = len(soft_name_list)

    download_url = re.compile('<a class="swTable-linkOut sw-icon-bounce-rate" href="(.*?)" target="_blank"></a>', re.S)
    download_url_list = re.findall(download_url, content)
    download_url_len = len(download_url_list)

    company_name = re.compile('<div class="cell-innerText">(.*?)</div>', re.S)
    company_name_list = re.findall(company_name, content)
    company_name_len = len(company_name_list)

    soft_dict = {}
    for i in range(0, len(soft_name_list)):
        soft_dict.update({i: (soft_name_list[i], company_name_list[i], download_url_list[i])})

    with open("Top_free.md", "wb") as f:
        f.write("| ID   | 软件名    |  开发公司  | 下载地址 |\n")
        f.write("| --------   | --------   | -----:   | :----: |\n")
        for key, value in soft_dict.items():
            f.write("| %s | %s | %s | %s |\n" % (key+1, value[0], value[1], value[2]))
            pass

    with open("Top_free_dict.json", "wb") as f:
        f.write(json.dumps(soft_dict))

    pass