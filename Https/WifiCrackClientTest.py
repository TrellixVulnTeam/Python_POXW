#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : WifiCrackClientTest.py
 @Time    : 2018/6/4 10:40
"""
import requests
import hashlib
import json
from urllib.parse import quote, unquote, urlencode

host = "http://192.168.2.67/"
LoginUrl = host + "Login?password={password}"
GetScanStatusUrl = host + "GetScanStatus"
StartCloudCrackUrl = host + "StartCloudCrack?ssid={ssid}&mac={mac}"
GetCrackHistoryUrl = host + "GetCrackHistory"
DownloadPcapFileUrl = host + "DownloadPcapFile?ssid={ssid}&mac={mac}"
StartWifiphishingUrl = host + "StartWifiPhishing?ssid={ssid}&mac={mac}"
ClearCrackRecordUrl = host + "ClearCrackRecord?password={password}"

session = requests.session()


def Test_Login():
    m = hashlib.md5()
    m.update("123456".encode())
    loginUrl = LoginUrl.format(password=m.hexdigest())
    content = session.get(loginUrl).content
    print(loginUrl)
    print(content)


def Test_GetScanStatus():
    content = session.get(url=GetScanStatusUrl).content
    print(content)
    apsList = json.loads(content)["aps"]
    # for apInfo in apsList:
    #     Test_StartCloudCrack(ssid=apInfo["ssid"], mac=apInfo["mac"])
    pass


def Test_StartCloudCrack(ssid, mac):
    url = StartCloudCrackUrl.format(ssid=quote(ssid), mac=quote(mac))
    print(url)
    content = session.get(url=url).content
    print(content)
    pass


def Test_GetCrackHistory():
    content = session.get(url=GetCrackHistoryUrl).content
    print(content)
    pass


def Test_DownloadPcapFile(ssid, mac):
    downloadUrl = DownloadPcapFileUrl.format(ssid=ssid, mac=quote(mac))
    content = session.get(url=downloadUrl)
    print(downloadUrl)
    pass


def Test_StartWifiphishing(ssid, mac):
    wifiohisherUrl = StartWifiphishingUrl.format(ssid=ssid, mac=quote(mac))
    content = session.get(url=wifiohisherUrl)
    print(wifiohisherUrl)

    pass


def Test_ClearCrackRecord():
    url = ClearCrackRecordUrl.format(password="yg_root@9985")
    content = session.get(url=url)
    print(url)


if __name__ == "__main__":
    # Test_Login()
    # Test_StartWifiphishing("Microsoft", "40:A5:EF:79:FB:61")
    # Test_GetScanStatus()
    # Test_StartCloudCrack(ssid="LgdGod", mac="00:0c:43:a6:29:77")
    # Test_GetCrackHistory()
    # Test_DownloadPcapFile("Microsoft", "40:A5:EF:79:FB:61")
    Test_ClearCrackRecord()
    pass
