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

ZsxqUrl0 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20"
ZsxqUrl1 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2018-05-28T02%3A55%3A41.644%2B0800"
ZsxqUrl2 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2018-02-17T11%3A34%3A23.856%2B0800"
ZsxqUrl3 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2018-01-04T12%3A52%3A23.050%2B0800"
ZsxqUrl4 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-12-14T20%3A52%3A42.373%2B0800"
ZsxqUrl5 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-11-27T18%3A01%3A27.247%2B0800"
ZsxqUrl6 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-11-15T13%3A28%3A52.456%2B0800"
ZsxqUrl7 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-11-04T17%3A27%3A54.307%2B0800"
ZsxqUrl8 = "https://api.zsxq.com/v1.10/groups/881142514122/topics?count=20&end_time=2017-10-23T14%3A52%3A47.216%2B0800"
ZsxqUrlList = [ZsxqUrl0, ZsxqUrl1, ZsxqUrl2, ZsxqUrl3, ZsxqUrl4, ZsxqUrl5, ZsxqUrl6, ZsxqUrl7, ZsxqUrl8]

ZsxqHearders = {
    "Connection": "keep-alive",
    "X-Version": "1.10.7",
    "Origin": "https://wx.zsxq.com",
    "Authorization": "70A52A39-EE87-40E4-9AAE-1F5079009294",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "X-Request-Id": "39ee9da6-5bce-5f5a-1c6d-d4bdd4ea7f69",
    "Referer": "https://wx.zsxq.com/dweb/",
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

        num = text[text.find("第") + 1:text.find("讲")]
        try:
            num = int(num)
        except:
            continue

        title = text[text.rfind("/>", 0, text.find('<e type="web"')) + 2:text.find('<e type="web"')].strip().replace("\n", " ")
        videoUrl = unquote(text[text.find("href=") + len("href=") + 1:text.find("\" title", text.find("href="))])

        code = text if "密码" in text else ""
        if '密码：' in code:
            code = code[code.find("密码：") + len("密码："):].strip()
        elif '密码' in code:
            code = code[code.find("密码") + + len("密码"):].strip()

        if '见评论' in code:
            code = topic["show_comments"][0]["text"]
            code = code[code.find("密码") + len("密码"):].strip()

        videoStoreDict.update({num: {"title": title, "videoUrl": videoUrl, "code": code[:10]}})


for url in ZsxqUrlList:
    ReadVideoInfo(url)

with open("AlgorithmSpace.json", "w") as f:
    content = json.dumps(videoStoreDict).encode().decode("unicode_escape")
    f.write(content)

# for video in videoStoreDict.values():
#     videoUrl = video["videoUrl"]
#     code = video["code"]
#     response = requests.get(url=videoUrl)
#     with open("youku.html", "wb") as f:
#         f.write(response.content)
#     pass
pass
