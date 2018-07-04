"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : GeekBang.py
 @Time    : 2018/7/4 16:22
"""
import requests
import json

TaskDict = {"8136": "开篇词",
            "8216": "零基础启蒙",
            "8217": "正式入门",
            "8700": "程序员修养",
            "8701": "编程语言",
            "8887": "理论学科",
            "8888": "系统知识",
            "9369": "软件设计",
            "9759": "Linux系统、内存和网络(系统底层知识)"}

DownloadUrl = "https://time.geekbang.org/serv/v1/article"

Cookies = dict(GCESS="BAQEgFEBAAoEAAAAAAwBAQIEF4I8WwsCBAAFBAAAAAAJAQEDBBeCPFsHBFYCZH0GBCcueUUIAQMBBOevEQA-",
               GCID="3dd63cc-756daf0-4516feb-6f40813",
               SERVERID="fe79ab1762e8fabea8cbf989406ba8f4|1530697550|1530692063",
               orderInfo="{%22list%22:[{%22count%22:1%2C%22image%22:%22https://static001.geekbang.org/resource/image/31/32/31ebe397ff1534baf499c570775afe32.jpg%22%2C%22name%22:%22%E6%8C%81%E7%BB%AD%E4%BA%A4%E4%BB%9836%E8%AE%B2%22%2C%22sku%22:100009701%2C%22price%22:{%22sale%22:4500}}]%2C%22invoice%22:false%2C%22app_id%22:3%2C%22cid%22:104%2C%22isFromTime%22:true%2C%22detail_url%22:%22https://time.geekbang.org/column/intro/104%22}",
               _ga="GA1.2.487875186.1527216143",
               _gid="GA1.2.258140660.1530692065",
               _gat="1"
               )

headers = {"POST": "/serv/v1/article HTTP/1.1",
           "Host": "time.geekbang.org",
           "Connection": "keep-alive",
           "Content-Length": "13",
           "Accept": "application/json, text/plain, */*",
           "Origin": "https://time.geekbang.org",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
           "Content-Type": "application/json",
           "Referer": "https://time.geekbang.org/column/article/8136",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9"}

session = requests.session()
for articleId, articleName in TaskDict.items():
    payload = dict(id=articleId)
    # headers["Content-Length"] = str(len(json.dumps(payload))-1)
    result = session.post(DownloadUrl, cookies=Cookies, headers=headers, data=payload, verify=False)
    with open(articleName + ".md", "wb") as f:
        article_dict = json.loads(result.content.decode())
        article_content = article_dict["data"]["article_content"]
        f.write(article_content.encode())
