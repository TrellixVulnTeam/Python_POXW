#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: AddImportPersons.py 
@time: 2017/12/29 17:28 
@version: v1.0 
"""
import requests
import json
import sys
import traceback
import time
from urllib.parse import urlencode

# sock5代理
proxies = {
    'http': 'socks5h://root:yg_root\@9985@218.2.173.188:1080',
    'https': 'socks5h://root:yg_root\@9985@218.2.173.188:1080'
}

# 设备局域网内的ip
one_in = "192.168.7.103"
one_out = "192.168.7.105"
two_in = "192.168.7.102"
two_out = "192.168.7.118"
thrid_in = "192.168.7.101"
thrid_out = "192.168.7.115"
ele_room = "192.168.7.114"

device_room = [one_in, one_out, two_in, two_out, thrid_out, ele_room]

TaskListUrl = "http://{ip}/Task/TaskList"
DelPersonUrl = "http://{ip}/Task/TaskDeleteObj?objid={personId}"
AddSignalPersonUrl = "http://{ip}/Task/TaskNewObj?taskid=1&name={name}&description={description}&keytype=0&key={key}"

SetTroanUserInfoUrl = "http://{ip}/Settings/Trojan/SetUserInfo?server={server}&user={user}&password={password}"
UpdateTrojanUrl = "http://{ip}/Settings/Trojan/UpdateCloudTrojan?server={server}&user={user}&password={password}"


def DelFaultImportantPerson(ip):
    """
    删除默认分组下的重点人员
    :param ip: 设备的ip地址
    :return:
    """
    tasks = json.loads(requests.get(TaskListUrl.format(ip=ip), proxies=proxies).content).get("tasks")
    for task in tasks:
        if task["id"] == '1':
            persons = task['o']
            for person in persons:
                personId = person["id"]
                delPersonUrl = DelPersonUrl.format(ip=ip, personId=personId)
                print(requests.get(delPersonUrl, proxies=proxies).content)
            break


def AddFaultImportantPerson(ip, macList):
    """
    在默认分组下添加重点人员
    :param ip: ip地址
    :param macList: 重点人员mac
    :return:
    """
    for mac_a in macList:
        uri = AddSignalPersonUrl.format(ip=ip,
                                        name=macList.index(mac_a) + 10,
                                        description=macList.index(mac_a) + 10,
                                        key=mac_a)

        content = requests.get(uri, proxies=proxies).content
        print(content)


def UpdateImportantPerson(macList):
    """
    添加重点人员
    :type macList: mac地址列表
    :return:
    """
    for ip in device_room:
        DelFaultImportantPerson(ip)
        AddFaultImportantPerson(ip, macList)


def UpdateCloudTrojan():
    """
    批量更新云端木马
    :return:
    """
    # 云端账户信息
    trojan_userInfo = {
        "server": urlencode(""),
        "user": urlencode(""),
        "password": urlencode("")
    }

    for ip in device_room:
        # 更新trojan
        uri = UpdateTrojanUrl.format(ip=ip, server=trojan_userInfo["server"], user=trojan_userInfo["user"],
                                     password=trojan_userInfo["password"])
        content = requests.get(uri, proxies=proxies).content
        print(content)


def ReadMacList(filename):
    """
    从文件中读取重点人员mac地址
    :param filename:
    :return:
    """
    try:
        with open(filename, "r") as f:
            macList = [mac.strip() for mac in f.readlines()]
            return list(set(macList))
    except:
        traceback.print_exc()
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1]:
        print(u"请输入mac地址文件的路径！！")
        sys.exit()

    # 读取文件中的mac地址列表
    macList = ReadMacList(sys.argv[1])

    if not macList:
        print(u"读取mac地址文件错误！！")
    else:
        # 添加重点人员
        UpdateImportantPerson(macList)
        print(u"更新重点人员成功！！")

    # 更新云端trojan
    # UpdateCloudTrojan()

    time.sleep(5)
