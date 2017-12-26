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


def ExceptKey(soft_name):
    for key_world in ["browser", "sms", "emoji", "vpn", "email", "wifi", "mail", "phone", "voip",
                      "number", "mobile", "internet", "bluetooth", "dial", "caller", "firefox", "international call",
                      "calling", "shar"]:
        if key_world in soft_name.lower():
            return True
    return False


if __name__ == "__main__":
    with open("soft_info.json", "r") as f:
        soft_pool = json.loads(f.read()).keys()

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

    test_soft_list = list()
    with open("Test_softs_infomation.md", "wb") as f:
        f.write("| ID   | 软件名    |  开发公司  | 下载地址 |\n")
        f.write("| --------   | --------   | -----:   | :----: |\n")
        for key, value in soft_dict.items():
            if ExceptKey(value[0]):
                continue
            if value[2][value[2].find("id=") + 3:] not in soft_pool:
                continue
            f.write("| %s | %s | %s | %s |\n" % (key+1, value[0], value[1], value[2]))
            test_soft_list.append(value[2][value[2].find("id=") + 3:])

    with open("Top_free_dict.json", "wb") as f:
        f.write(json.dumps(soft_dict))

    with open("test_softs.txt", "w") as f:
        f.write("\n".join(test_soft_list))
    pass