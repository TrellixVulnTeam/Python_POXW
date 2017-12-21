#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: APKDownloadSpider.py 
@time: 2017/12/19 19:57 
@version: v1.0 
"""
import requests
import json
import threading
import re
import traceback
import time

apk_check_url_head = "https://apps.evozi.com/apk-downloader/?id="
apk_download_url = "https://api-apk.evozi.com/download"
pattern = re.compile(".*?{t:(.*?),(.*?):.*?,(.*?):.*?", re.S)

apk_find_hearder = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "connection": "keep-alive",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
}

apk_find_cookies = {
    "logglytrackingsession": "34ca665d-7808-4b2b-834f-921733c6c56b",
    "__cfduid": "d6f214cc95dab688e156829e2fb8d23431513764291",
    "evozi_session": "5dulseqdkroephufgs7v44tjq1",
    "__qca": "P0-1293332314-1513764292003",
    "_ga": "GA1.2.1413937179.1513764290",
    "_gid": "GA1.2.1878174561.1513764290"
}

apk_download_hearder = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN",
    "Connection": "	keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "api-apk.evozi.com",
    "Origin": "https://apps.evozi.com",
    "referer": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
}

def DownloadAPK(soft_dict):
    with open("APK_status.txt", "r") as f:
        soft_list = f.read().split("\n")

    soft_info_dict = {}
    for soft_rank, soft_info_list in soft_dict.items():
        try:
            google_url = soft_info_list[-1]
            soft_name = google_url[google_url.find("id=") + 3:]
            if soft_name in soft_list:
                continue

            apk_check_url = apk_check_url_head + soft_name

            # 浏览器会话
            session = requests.session()
            r = session.get(apk_check_url, headers = apk_find_hearder, timeout = 10)
            content_list = r.content.split("\n")

            # 获取到的密钥
            code_a = content_list[160].strip()
            keyworld_1 = code_a[code_a.find("'") + 1: code_a.rfind("'")]

            # 获取到的软件名key值代号
            code_b = content_list[187].strip()
            keyworld_list = re.findall(pattern, code_b)[0]

            # 构造post数据
            post_data = {
                "t": keyworld_list[0].strip(),
                keyworld_list[1].strip(): str(soft_name),
                keyworld_list[2].strip(): keyworld_1,
                "fetch": "false"
            }
            try:
                reponse = session.post(url = apk_download_url, headers = apk_find_hearder, data = post_data).content
                reponse_dict = json.loads(reponse)
            except:
                with open("except.html", "wb") as f:
                    f.write(reponse)
                print soft_name + "request post except."
                continue
            if reponse_dict["status"] == "error":
                continue

            apk_file = session.get(url = "https:" + reponse_dict["url"]).content
            with open("Top_100_aps/" + soft_name + ".apk", "wb") as f:
                f.write(apk_file)

            with open("APK_status.txt", "a") as f:
                f.write(soft_name)
                f.write("\n")

            soft_info_dict.update({soft_name: reponse_dict})

        except:
            traceback.print_exc()
            continue
    with open("soft_info.json", "a") as f:
        f.write(json.dumps(soft_info_dict))


def dict_slice(adict, start, end):
    keys = adict.keys()
    dict_slice = {}
    for k in keys[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice


if __name__ == "__main__":
    with open("Top_100_dict.json", "rb") as f:
        soft_dict = json.loads(f.read())

    DownloadAPK(soft_dict)

    # for i in range(0, 10, 1):
    #     part_dict = dict_slice(soft_dict, i * 54, (i + 1) * 54)
    #
    #     threading.Thread(target = DownloadAPK,
    #                      args = (part_dict,),
    #                      name = str(i) + "begin").start()
    pass