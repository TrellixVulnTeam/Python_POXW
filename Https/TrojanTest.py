#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: TrojanTest.py 
@time: 2018/3/28 16:51 
@version: v1.0 
"""
import requests
import json
import time
import urllib.parse
import hashlib


def Test_GetTrojanStat():
    trojanStatUrl = "http://192.168.2.67/Settings/Trojan/TrojanStat"
    statResponse = requests.get(trojanStatUrl)
    statContentDict = json.loads(statResponse.content)
    pass

def Test_RememberUserInfo():
    # 记住密码
    setUserInfoUrl = "http://192.168.2.67/Settings/Trojan/SetUserInfo?server={server_url}&user={user}&password={password}&save=0"
    server_url = urllib.parse.quote("https://192.168.2.223")
    user = urllib.parse.quote("admin")
    password = urllib.parse.quote("123456")
    setUserInfoUrl = setUserInfoUrl.format(server_url = server_url, user = user, password = password)
    setUserInfoResponse = requests.get(url = setUserInfoUrl)
    setUserInfoContentDict = setUserInfoResponse.content


    trojanStatUrl = "http://192.168.2.67/Settings/Trojan/TrojanStat"
    statResponse = requests.get(trojanStatUrl)
    statContentDict = json.loads(statResponse.content)
    pass

def Test_ForgetUserInfo():
    # 不记住密码
    setUserInfoUrl = "http://192.168.2.67/Settings/Trojan/SetUserInfo?server={server_url}&user={user}&password={password}&save=1"
    server_url = urllib.parse.quote("https://192.168.2.223")
    user = urllib.parse.quote("admin")
    password = urllib.parse.quote("123456")
    setUserInfoUrl = setUserInfoUrl.format(server_url = server_url, user = user, password = password)
    setUserInfoResponse = requests.get(url = setUserInfoUrl)
    setUserInfoContentDict = setUserInfoResponse.content

    trojanStatUrl = "http://192.168.2.67/Settings/Trojan/TrojanStat"
    statResponse = requests.get(trojanStatUrl)
    statContentDict = json.loads(statResponse.content)
    pass

def Test_Download():
    # 测试下载
    downloadUrl = "http://192.168.2.67/Settings/Trojan/UpdateCloudTrojan?server={server_url}&user={user}&password={password}"
    server_url = urllib.parse.quote("https://192.168.2.223")
    user = urllib.parse.quote("admin")
    password = urllib.parse.quote("123456")
    downloadUrl = downloadUrl.format(server_url = server_url, user = user, password = password)
    downloadResponse = requests.get(downloadUrl)
    statContentDict = json.loads(downloadResponse.content)
    print(statContentDict)
    pass

def Test_DeleteTrojan():
    # 测试删除
    delUrl = "http://192.168.2.67/Settings/Trojan/Del?type=apkcloud"
    delResponse = requests.get(delUrl)
    delContent = delResponse.content
    pass


def Test_User():
    # 登陆
    loginUrl = "https://192.168.2.223/website/home"
    session = requests.session()

    myMd5 = hashlib.md5()
    myMd5.update("123456".encode())
    myMd5_Digest = myMd5.hexdigest()
    params = {"userName": "admin", "password": myMd5_Digest.upper()}
    loginResponse = session.post(url = loginUrl, data = params, verify = False)
    loginResponseDict = json.loads(loginResponse.content.decode())

    sk = loginResponseDict["data"]["sessionkey"]
    userID = loginResponseDict["data"]["user"]["userId"]

    # 更新列表
    listUrl = "https://192.168.2.223/RcsViewSys/transfer//RcsDataSys/client/aos/phantom-list?SK={sk}&page=1&size=5&sort=id&order=DESC&phone-system-type=1&user-id={userID}".format(sk=sk, userID=userID)
    listResponse = session.get(url = listUrl, verify = False)
    listContentDict = json.loads(listResponse.content)
    clientID = str(listContentDict["data"]["rows"][1]["id"])
    createTime = listContentDict["data"]["rows"][1]["create-time"]
    fileName = listContentDict["data"]["rows"][1]["wifilz-file"]["file-name"]

    # 下载
    downloadUrl = "https://192.168.2.223/RcsDataSys/client/aos/client-download?client-id={clientID}&file-name={fileName}&SK={sk}"
    downloadUrl = downloadUrl.format(clientID = urllib.parse.quote(clientID),
                                     fileName = urllib.parse.quote(fileName),
                                     sk = urllib.parse.quote(sk))
    downloadResponse = session.get(url = downloadUrl, verify = False)
    fileTmp = downloadResponse.content
    with open(fileName, "wb") as f:
        f.write(fileTmp)

    #登出
    logoutUrl = "https://192.168.2.223/website/logout"
    logoutResponse = session.get(url = logoutUrl, verify = False)
    contentDict = json.loads(logoutResponse.content.decode())
    print("~~~~~~~~~~Logout~~~~~~~~~~~~")
    print(contentDict)

    time.sleep(3)

    # 获取列表2
    listResponse2 = session.get(url = listUrl, verify = False)
    trojanList = json.loads(listResponse2.content.decode())
    pass

    # 下载2
    downloadResponse2 = session.get(url = downloadUrl, verify = False)
    fileTmp2 = downloadResponse2.content
    with open(fileName + "2", "wb") as f:
        f.write(fileTmp2)
    pass


if __name__ == '__main__':
    # Test_GetTrojanStat()
    # Test_RememberUserInfo()
    # Test_ForgetUserInfo()
    Test_DeleteTrojan()
    Test_Download()

    # 测试用户登陆
    # Test_User()
    print("over")
    pass
