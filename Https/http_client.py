#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: http_client.py
@time: 2017/7/21 11:36
@version: v1.0
"""
import requests
import json
import time
import urllib.parse


def DictFileUpdate():
    """
    wifilz字典文件上传、使用测试
    :return:
    """
    server_url = "http://192.168.2.191"
    system_status_url = "/SysResourceInfo.json"
    get_dict_url = "/Settings/crackdict/GetDict"
    update_dict_url = "/Settings/crackdict/UploadDict?name="
    change_dict_seq_url = "/Settings/crackdict/adjustDicts"
    del_dict_url = "/Settings/crackdict/DelDict?idlist="

    sys_resouce = json.loads(requests.get(url = server_url + system_status_url).content)
    print(sys_resouce)

    dicts_info_json = requests.get(url = server_url + get_dict_url).content
    print(dicts_info_json)

    # 字典上传
    # upload_dict_url = server_url + update_dict_url \
    #                   + urllib.quote("License.txt") + "&des=" \
    #                   + urllib.quote("123456789")
    # files = {"data": open("License.txt", "rb")}
    # dicts_upload = requests.post(url = upload_dict_url, files = files)
    # if json.loads(dicts_upload.content)["result"] == '0':
    #     print "dict upload success!"
    # else:
    #     print "dict upload fail!"

    # 字典次序修改
    dicts_info = json.loads(dicts_info_json)
    dicts_list = dicts_info["dict"]
    dicts_num = len(dicts_list)
    dicts_seq_list = []
    for i in range(0, dicts_num):
        id = str(input("dict_id:"))
        seq = str(input("dict_seq:"))
        dicts_seq_list.append({"id": id, "s": seq})
    dicts_seq = {"dict": dicts_seq_list}
    dicts_seq_content = requests.post(url = server_url + change_dict_seq_url,
                                      json = json.dumps(dicts_seq))
    if json.loads(dicts_seq_content.content)["result"] == '0':
        print("dict change seq success!")
    else:
        print("dict change seq fail!")

    # 删除字典
    # idlist = raw_input("idlist is :")
    # dicts_del_info = requests.get(url = server_url+ del_dict_url + urllib.quote(idlist))
    # if json.loads(dicts_del_info.content)["result"] == '0':
    #     print "del dict success!"
    # else:
    #     print "del dict fail!"

    dicts_info_json = requests.get(url = server_url + "/Settings/crackdict/GetDict").content
    print(dicts_info_json)


def SetMultipleSSID():
    """
    wifilz多SSID测试
    :return:
    """
    server_url = "http://192.168.2.182"
    start_mulSSID_url = "/Operation/Scan/StartMultipleSSIDAttack"
    get_mulSSID_status = "/Operation/Attack/MultipleSSIDAttackStatus"
    stop_mulSSID_url = "/Operation/Attack/MultipleAttackStop"

    # 发起多ssid取证
    channel = "3"
    count = "8"
    aps = [
        {
            "ssid": "LGD",
            "protype": "WPA",
            "password": "lgdforthedream"
        },
        {
            "ssid": "LGD_1",
            "protype": "WPA",
            "password": "lgdforthedream"
        },
        {
            "ssid": "LGD_2",
            "protype": "OPN",
            "password": "lgdforthedream"
        },
        {
            "ssid": "老干爹",
            "protype": "WPA",
            "password": "lgdforthedream"
        }
    ]
    param_dict = {
        "channel": channel,
        "count": len(aps),
        "aps": aps
    }

    param_json = json.dumps(param_dict)
    start_content = requests.post(url = server_url + start_mulSSID_url, json = param_json).content
    print(start_content)

    # 获取多ssid取证状态
    status_content = requests.get(url = server_url + get_mulSSID_status).content
    print(status_content)

    # 停止多ssid取证
    stop_content = requests.get(url = server_url + stop_mulSSID_url).content
    print(stop_content)
    pass


def GetSystemUpdate():
    update_url = "http://192.168.2.41:4443/Device/UpdatePack"
    body = json.dumps({"version": "fasfas", "isFully": True})
    res = requests.get(url = update_url, verify = False, data = body, stream = True)
    with open("update", "a") as f:
        for chunk in res.iter_content(chunk_size = 5):
            f.write(chunk)
            print(chunk)
    pass


def UpdateTrojanUserInfo():
    url = "http://192.168.2.67/Settings/Trojan/SetUserInfo?server={server_url}&user={user}&password={password}"
    server_url = urllib.parse.quote("http://baidu.com")
    user = urllib.parse.quote("yagoo")
    password = urllib.parse.quote("8987989949874")
    url = url.format(server_url = server_url, user = user, password = password)
    res = requests.get(url = url)
    resDict = json.loads(res)
    print(res)


if __name__ == '__main__':
    # 上传字典测试
    # DictFileUpdate()

    # 多SSID测试
    # SetMultipleSSID()

    # 获取系统更新包
    # GetSystemUpdate()

    # 上传木马的用户信息
    UpdateTrojanUserInfo()
    pass
