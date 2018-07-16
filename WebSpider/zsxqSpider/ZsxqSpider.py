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

ZsxqUrl1 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20"
ZsxqUrl2 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2018-03-17T17%3A22%3A04.942%2B0800"
ZsxqUrl3 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2018-01-16T20%3A05%3A21.286%2B0800"
ZsxqUrl4 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-12-20T20%3A19%3A18.707%2B0800"
ZsxqUrl5 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-12-04T17%3A28%3A16.428%2B0800"
ZsxqUrl6 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-11-19T10%3A27%3A55.452%2B0800"
ZsxqUrl7 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-11-08T09%3A39%3A05.633%2B0800"
ZsxqUrl8 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-10-29T19%3A31%3A04.691%2B0800"

ZsxqUrlList = [ZsxqUrl1, ZsxqUrl2, ZsxqUrl3, ZsxqUrl4, ZsxqUrl5, ZsxqUrl6, ZsxqUrl7, ZsxqUrl8]

ZsxqHearders = {
    "Connection": "keep-alive",
    "X-Version": "1.10.0",
    "Origin": "https://wx.zsxq.com",
    "Authorization": "3793782B-5B9C-DC8E-BCAD-F2F989A0A3FC",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "X-Request-Id": "11fef5df-03f0-68d7-0f43-cff1f411bd8b",
    "Referer": "https://wx.zsxq.com/dweb-alpha/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def ReadVideoInfo(url, headers=ZsxqHearders):
    response = requests.get(url=url, headers=headers)
    responseDict = json.loads(response.content.decode())

    topics = responseDict["resp_data"]["topics"]
    for topic in topics:
        if "talk" not in topic.keys():
            continue
        text = topic["talk"]["text"]
        if "第" not in text or "讲" not in text or "href=" not in text:
            continue

        title = text[text.find("第") + 1:text.find("讲")]
        videoUrl = unquote(text[text.find("href=") + len("href=") + 1:text.find("\" title", text.find("href="))])
        code = text[text.find("密码") + len("密码"):].strip() if "密码" in text else ""
        videoStoreDict.update({title: {"videoUrl": videoUrl, "code": code[:10]}})


for url in ZsxqUrlList:
    ReadVideoInfo(url)

with open("AlgorithmSpace.json", "w") as f:
    content = json.dumps(videoStoreDict)
    f.write(content)

# for video in videoStoreDict.values():
#     videoUrl = video["videoUrl"]
#     code = video["code"]
#     response = requests.get(url=videoUrl)
#     with open("youku.html", "wb") as f:
#         f.write(response.content)
#     pass
pass
