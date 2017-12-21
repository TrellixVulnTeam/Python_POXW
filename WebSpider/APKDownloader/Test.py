#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Test.py
@time: 2017/12/21 21:43
@version: v1.0 
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import re

pattern = re.compile("var version_desc = '';.*?var.*?= '(.*?)';.*?{t:(.*?),(.*?):.*?,(.*?):.*?", re.S)
pattern2 = re.compile("", re.S)

first_requests_header = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip",
    "accept-language": "zh-CN,zh;q=0.9",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"
}

session = requests.session()
session.headers = first_requests_header
content = session.get(url = "https://apps.evozi.com/apk-downloader/?id=org.telegram.messenger").content
content = content.replace("\n", "")
result = re.findall(pattern, content)[0]

with open("test1.html", "w") as f:
    f.write(content)


pass