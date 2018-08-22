#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : http_client_bottle.py
 @Time    : 2018/5/30 16:40
"""
import requests

files = {"file": open("0002.zip", "rb")}
values = {
    "deviceSerial": "20001180530",
    "mac": "cd:ad:21:43:45:12",
    "ssid": "杨氏",
    "lng": "12.222",
    "lat": "32.555",
    "address": "红草莓大饭店"
}
with open("./0002.zip", "rb") as f:
    content = requests.post(url="http://192.168.2.45:8080/WifiCrackYjc/task/add", files=files,  data=values)
    print(content.text)
pass
