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
import time
from urllib.parse import quote, unquote, urlencode

host = "http://192.168.43.249/"
# host = "http://192.168.2.67/"
# host = "http://192.168.2.189/"
LoginUrl = host + "Login?password={password}"

GetScanStatusUrl = host + "GetScanStatus"
GetCrackHistoryUrl = host + "GetCrackHistory"

StartCloudCrackUrl = host + "StartCloudCrack?ssid={ssid}&mac={mac}&useNewCap={useNewCap}"
StopCloudCrackUrl = host + "StopCloudCrack?ssid={ssid}&mac={mac}"

StartWifiphishingUrl = host + "StartWifiPhishing?ssid={ssid}&mac={mac}&useNewCap={useNewCap}"
StopWifiPhishingUrl = host + "StopWifiPhishing"

StartOfflineCrackUrl = host + "StartOfflineCrack?ssid={ssid}"
StopOfflineCrackUrl = host + "StopOfflineCrack"
GetOfflineCrackStatusUrl = host + "GetOfflineCrackStatus"
StartCloudCrackFromOfflineUrl = host + "StartCloudCrackFromOffline"

DownloadPcapFileUrl = host + "DownloadPcapFile?ssid={ssid}&mac={mac}"
ClearCrackRecordUrl = host + "ClearCrackRecord?password={password}"

session = requests.session()


def Test_Login():
    m = hashlib.md5()
    m.update("123456".encode())
    loginUrl = LoginUrl.format(password=m.hexdigest())
    content = session.get(loginUrl).content
    print(loginUrl)
    print(content.decode("unicode-escape"))


def Test_GetScanStatus():
    content = session.get(url=GetScanStatusUrl).content
    print(content.decode())
    apsList = json.loads(content)["aps"]
    # for apInfo in apsList:
    #     Test_StartCloudCrack(ssid=apInfo["ssid"], mac=apInfo["mac"])
    pass


def Test_GetCrackHistory():
    content = session.get(url=GetCrackHistoryUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_StartCloudCrack(ssid, mac, useNewCap=True):
    url = StartCloudCrackUrl.format(ssid=quote(ssid), mac=quote(mac), useNewCap=useNewCap)
    print(url)
    content = session.get(url=url).content
    print(content.decode("unicode-escape"))
    pass


def Test_StopCloudCrack(ssid, mac):
    url = StopCloudCrackUrl.format(ssid=quote(ssid), mac=quote(mac))
    print(url)
    content = session.get(url=url).content
    print(content.decode("unicode-escape"))
    pass


def Test_StartWifiphishing(ssid, mac, useNewCap=True):
    wifiohisherUrl = StartWifiphishingUrl.format(ssid=ssid, mac=quote(mac), useNewCap=useNewCap)
    content = session.get(url=wifiohisherUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_StopWifiphishing():
    wifiohisherUrl = StopWifiPhishingUrl.format()
    content = session.get(url=wifiohisherUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_StartOfflineCrack(ssid):
    startUrl = StartOfflineCrackUrl.format(ssid=ssid)
    content = session.get(url=startUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_StopOfflineCrack():
    stopUrl = StopOfflineCrackUrl
    content = session.get(url=stopUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_GetOfflineCrackStatus():
    getStatusUrl = GetOfflineCrackStatusUrl
    content = session.get(url=getStatusUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_StartCloudCrackFromOffline():
    startCrackUrl = StartCloudCrackFromOfflineUrl
    content = session.get(url=startCrackUrl).content
    print(content.decode("unicode-escape"))
    pass


def Test_DownloadPcapFile(ssid, mac):
    downloadUrl = DownloadPcapFileUrl.format(ssid=ssid, mac=quote(mac))
    content = session.get(url=downloadUrl)
    print(downloadUrl)
    pass


def Test_ClearCrackRecord():
    url = ClearCrackRecordUrl.format(password="yg_root@9985")
    content = session.get(url=url)
    print(url)


if __name__ == "__main__":
    Test_Login()
    # Test_StartWifiphishing("Microsoft", "40:A5:EF:79:FB:61")
    Test_GetScanStatus()
    # Test_StartCloudCrack(ssid="helloworld", mac="C8:3A:35:CF:03:73")
    # Test_StartCloudCrack(ssid="helloworld", mac="C8:3A:35:CF:03:73", useNewCap=False)
    # Test_StopCloudCrack(ssid="helloworld", mac="C8:3A:35:CF:03:73")

    # Test_StartWifiphishing(ssid="helloworld", mac="C8:3A:35:CF:03:73")
    # Test_StartWifiphishing(ssid="helloworld", mac="C8:3A:35:CF:03:73", useNewCap=False)
    # Test_StopWifiphishing()

    # Test_StartOfflineCrack(ssid="helloworld")
    # Test_StopOfflineCrack()
    # time.sleep(10)
    Test_GetOfflineCrackStatus()
    # Test_StartCloudCrackFromOffline()

    Test_GetCrackHistory()
    # Test_DownloadPcapFile("Microsoft", "40:A5:EF:79:FB:61")
    # Test_ClearCrackRecord()
    pass
