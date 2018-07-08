"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ZsxqSpider.py
@time: 18-7-8 下午3:05
@version: v1.0 
"""
import requests
import json
import re
from urllib.parse import unquote

videoStoreDict = dict()

ZsxqUrl = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20"

ZsxqHearders = {
    "Connection": "keep-alive",
    "X-Version": "1.10.0",
    "Origin": "https://wx.zsxq.com",
    "Authorization": "3793782B-5B9C-DC8E-BCAD-F2F989A0A3FC",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "X-Request-Id": "3ac1f2ba-8600-a944-67a2-31b23600ce5c",
    "Referer": "https://wx.zsxq.com/dweb-alpha/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

response = requests.get(url=ZsxqUrl, headers=ZsxqHearders)
responseDict = json.loads(response.content.decode())

topics = responseDict["resp_data"]["topics"]
for topic in topics:
    text = topic["talk"]["text"]
    if "第" not in text or "讲" not in text or "href=" not in text:
        continue

    title = text[text.find("第") + 1:text.find("讲")]
    videoUrl = unquote(text[text.find("href=") + len("href=") + 1:text.find("\" title", text.find("href="))])
    code = text[text.find("密码") + len("密码"):].strip() if "密码" in text else ""
    videoStoreDict.update({title: {"videoUrl": videoUrl, "code": code[:10]}})

with open("AlgorithmSpace.json", "w") as f:
    content = json.dumps(videoStoreDict)
    f.write(content)

for video in videoStoreDict.values():
    videoUrl = video["videoUrl"]
    code = video["code"]
    response = requests.get(url=videoUrl)
    with open("youku.html", "wb") as f:
        f.write(response.content)
    pass
pass
