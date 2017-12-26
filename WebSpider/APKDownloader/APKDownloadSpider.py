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
import os
import Convert_APKs_info

apk_check_url = "https://apps.evozi.com/apk-downloader/?id="
apk_download_url = "https://api-apk.evozi.com/download"
pattern = re.compile("var version_desc = '';.*?var.*?= '(.*?)';.*?{t:(.*?),(.*?):.*?,(.*?):.*?", re.S)

apk_check_hearder = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip",
    "accept-language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
}

apk_download_hearder = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://apps.evozi.com",
    "referer": "",                        # https://apps.evozi.com/apk-downloader/?id=org.telegram.messenger,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
}


def get_proxy():
    """
    获取代理IP
    :return:  返回代理IP
    """
    while True:
        proxy = {"http": "{}".format(requests.get("http://192.168.2.67:5010/get/").content)}
        try:
            reponse = requests.get("http://httpbin.org/ip", proxies = proxy, timeout = 3)
        except:
            # traceback.print_exc()
            continue
        return proxy


def DownloadAPK(download_soft_dict):
    """
    下载APK
    :param download_soft_dict: 需要下载的APK列表
    :return:
    """
    while True:
        with open("APK_status.txt", "r") as f :
            finish_soft_list = f.read().split("\n")

        with open("APK_error.txt", "r") as f :
            error_soft_list = f.read().split("\n")

        proxies = get_proxy()
        for soft_rank, soft_info_list in download_soft_dict.items():
            try:
                # 获取软件名
                google_play_url = soft_info_list[-1]
                soft_name = google_play_url[google_play_url.find("id=") + 3:]

                # 如果软件在完成列表中，则继续
                if soft_name in finish_soft_list or soft_name in error_soft_list:
                    continue

                # 创建evozi网站的url
                evozi_url = apk_check_url + soft_name

                # 浏览器会话
                session = requests.session()
                session.proxies = proxies
                session.headers = apk_check_hearder

                # 正则获取post数据元素
                content = session.get(evozi_url, timeout = 10).content.replace("\n", "")
                re_list = re.findall(pattern, content)[0]

                # 构造post数据
                post_data = {
                    "t": re_list[1].strip(),
                    re_list[2].strip(): str(soft_name),
                    re_list[3].strip(): re_list[0],
                    "fetch": "false"
                }

                # 尝试获取下载链接，异常则换代理IP再次尝试
                try:
                    # 获取下载链接时，改变会话头
                    apk_download_hearder["referer"] = evozi_url
                    session.headers = apk_download_hearder
                    reponse = session.post(url = apk_download_url, data = post_data, timeout = 10).content
                    reponse_dict = json.loads(reponse)
                except:
                    print soft_name + " request post except."
                    proxies = get_proxy()
                    # session = requests.session()
                    time.sleep(30)
                    continue

                # 如果返回状态为失败，则打印失败信息，休息1分钟左右再次尝试
                if reponse_dict["status"] == "error":
                    with open("APK_error.txt", "a") as f:
                        f.write(soft_name)
                        f.write("\n")

                    print soft_name + ' reponse_dict["status"] == "error" %s' % reponse_dict["data"]
                    # 如果需要休息一段时间，则休息一段时间。
                    time_str = str(reponse_dict["data"])
                    if "again in" in time_str and "minute" in time_str:
                        sleep_time = time_str[time_str.find("again in ") + len("again in "): time_str.find("minute")].strip()
                        if sleep_time:
                            time.sleep(float(sleep_time) * 60)
                    time.sleep(20)

                    proxies = get_proxy()
                    # session = requests.session()
                    continue

                # 如果成功，则开始下载
                time.sleep(5)
                print "Download %s begining......" % soft_name
                apk_file = session.get(url = "https:" + reponse_dict["url"]).content
                if not os.path.exists("Top_100_aps/"):
                    os.mkdir("Top_100_aps")

                with open("Top_100_aps/" + soft_name + ".apk", "wb") as f:
                    f.write(apk_file)

                # 将成功的软件名记录
                with open("APK_status.txt", "a") as f:
                    f.write(soft_name)
                    f.write("\n")

                # 记录软件的详细信息
                soft_info_dict = dict({soft_name: reponse_dict})
                with open("soft_info.json", "a") as f:
                    f.write(json.dumps(soft_info_dict))
                print "Download %s end......" % soft_name

                time.sleep(10)
            except:
                traceback.print_exc()
                continue


def dict_slice(adict, start, end):
    """
    字典切片
    :param adict: 需切片的字典
    :param start: 开始点
    :param end: 结束点
    :return: 切片
    """
    keys = adict.keys()
    dict_slice = {}
    for k in keys[start:end]:
        dict_slice[k] = adict[k]
    return dict_slice


if __name__ == "__main__":

    # apk_files = "".join(os.listdir("Top_100_aps/")).replace(".apk", "\n")
    # with open("APK_status.txt", "w") as f:
    #     f.write(apk_files)
    #
    # with open("Top_100_dict.json", "rb") as f:
    #     soft_dict = json.loads(f.read())
    # DownloadAPK(soft_dict)
    #
    # with open("Top_free_dict.json", "rb") as f:
    #     soft_dict = json.loads(f.read())
    # DownloadAPK(soft_dict)

    # with open("soft_info.json", "r") as f:
    #     soft_dict = json.loads(f.read())
    # thread_num = 3
    # part_num = len(soft_dict) / thread_num
    # for i in range(0, thread_num, 1):
    #     part_dict = dict_slice(soft_dict, i * part_num, (i + 1) * part_num)
    #     for soft_name, soft_info in part_dict.items():
    #         src_apk_name = os.path.join("Top_100_aps", soft_name + ".apk")
    #         dst_apk_name = os.path.join(str(i), soft_name + ".apk")
    #         if not os.path.exists(str(i)):
    #             os.mkdir(str(i))
    #         os.rename(src_apk_name, dst_apk_name)
    #     Convert_APKs_info.SoftInfoXlwt(part_dict, str(i) + ".xls")
    #     pass
    #     with open("Top_free_dict_" + str(i) + ".json", "w") as f:
    #         f.write(json.dumps(part_dict))
    #
    #     threading.Thread(target = DownloadAPK,
    #                      args = (part_dict,),
    #                      name = str(i) + "begin").start()

    # i = 2
    # apk_list = os.listdir("Top_100_aps")
    # soft_list = [soft_name[: -4] for soft_name in apk_list]
    # new_soft_dict = {key: soft_dict[key] for key in soft_list if key in soft_dict.keys()}
    # for soft_name, soft_info in new_soft_dict.items():
    #     src_apk_name = os.path.join("Top_100_aps", soft_name + ".apk")
    #     dst_apk_name = os.path.join(str(i), soft_name + ".apk")
    #     if not os.path.exists(str(i)):
    #         os.mkdir(str(i))
    #     os.rename(src_apk_name, dst_apk_name)
    # Convert_APKs_info.SoftInfoXlwt(new_soft_dict, str(i) + ".xls")
    pass