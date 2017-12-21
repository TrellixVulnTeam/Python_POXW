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
import random

apk_check_url_head = "https://apps.evozi.com/apk-downloader/?id="
apk_download_url = "https://api-apk.evozi.com/download"
pattern = re.compile(".*?{t:(.*?),(.*?):.*?,(.*?):.*?", re.S)

apk_find_hearder = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
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
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "api-apk.evozi.com",
    "Origin": "https://apps.evozi.com",
    "referer": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
}


def get_proxy():
    while True:
        proxy = {"http": "{}".format(requests.get("http://192.168.2.67:5010/get/").content)}
        try:
            reponse = requests.get("http://httpbin.org/ip", proxies = proxy, timeout = 3)
        except:
            # traceback.print_exc()
            continue
        return proxy


def DownloadAPK(soft_dict):
    with open("APK_status.txt", "r") as f:
        soft_list = f.read().split("\n")

    proxies = get_proxy()
    session = requests.session()
    while True:
        download_num = 0
        for soft_rank, soft_info_list in soft_dict.items():
            try:
                google_url = soft_info_list[-1]
                soft_name = google_url[google_url.find("id=") + 3:]
                if soft_name in soft_list:
                    download_num += 1
                    if download_num == len(soft_dict):
                        return
                    continue

                apk_check_url = apk_check_url_head + soft_name

                # 浏览器会话
                session.proxies = proxies
                session.headers = apk_find_hearder
                r = session.get(apk_check_url, timeout = 10)
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
                    apk_download_hearder["referer"] = apk_check_url
                    # session.headers = apk_download_hearder
                    reponse = session.post(url = apk_download_url, data = post_data, timeout = 10).content
                    reponse_dict = json.loads(reponse)
                except:
                    print soft_name + " request post except."
                    proxies = get_proxy()
                    session.proxies = proxies
                    continue
                if reponse_dict["status"] == "error":
                    print soft_name + ' reponse_dict["status"] == "error" %s' % reponse_dict["data"]
                    time.sleep(random.randint(60, 70))
                    continue

                print "Download %s begining......" % soft_name
                apk_file = session.get(url = "https:" + reponse_dict["url"]).content
                with open("Top_100_aps/" + soft_name + ".apk", "wb") as f:
                    f.write(apk_file)

                with open("APK_status.txt", "a") as f:
                    f.write(soft_name)
                    f.write("\n")

                soft_info_dict = dict({soft_name: reponse_dict})
                with open("soft_info.json", "a") as f:
                    f.write(json.dumps(soft_info_dict))
                print "Download %s end......" % soft_name

                time.sleep(10)
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
    #
    # DownloadAPK(soft_dict)

    thread_num = 20
    part_num = 540 / thread_num
    for i in range(0, thread_num, 1):
        part_dict = dict_slice(soft_dict, i * part_num, (i + 1) * part_num)

        threading.Thread(target = DownloadAPK,
                         args = (part_dict,),
                         name = str(i) + "begin").start()
    pass