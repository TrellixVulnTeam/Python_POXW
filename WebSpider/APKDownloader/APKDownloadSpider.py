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

def DownloadAPK(soft_dict):
    with open("APK_status.txt", "r") as f:
        soft_list = f.read().split("\n")

    for soft_rank, soft_info_list in soft_dict.items():
        time.sleep(15)
        try:
            google_url = soft_info_list[-1]
            soft_name = google_url[google_url.find("id=") + 3:]
            if soft_name in soft_list:
                continue

            apk_check_url = apk_check_url_head + soft_name
            content_list = requests.get(url = apk_check_url).content.split("\n")

            code_a = content_list[160].strip()
            keyworld_1 = code_a[code_a.find("'") + 1: code_a.rfind("'")]

            code_b = content_list[187].strip()
            keyworld_list = re.findall(pattern, code_b)[0]
            post_data = {"t": keyworld_list[0].strip(), keyworld_list[1].strip(): str(soft_name), keyworld_list[2].strip(): keyworld_1, "fetch": "false"}

            try:
                reponse = requests.post(url = apk_download_url, data = post_data).content
                reponse_dict = json.loads(reponse)
            except:
                with open("except.html", "wb") as f:
                    f.write(reponse)
                print soft_name + "request post except."
                continue
            if reponse_dict["status"] == "error":
                continue

            apk_file = requests.get(url = "https:" + reponse_dict["url"]).content
            with open("Top_100_aps/" + soft_name + ".apk", "wb") as f:
                f.write(apk_file)

            with open("APK_status.txt", "a") as f:
                f.write(soft_name)
                f.write("\n")
        except:
            traceback.print_exc()
            continue

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