#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Spider_choubai.py 
@time: 2017/7/11 10:57 
@version: v1.0 
"""
import urllib
import urllib2
import re
import os
import requests


def SaveImg(imag_url):
    img_name = imag_url[imag_url.rfind('/'):]
    if not os.path.isdir("image"):
        os.mkdir("image")
    with open("image" + img_name, "wb") as f:
        # response = urllib.urlopen("http:" + imag_url)
        response = requests.get("http:"+imag_url)
        f.write(response.content)


url = "https://www.qiushibaike.com/"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    # request = urllib2.Request(url, headers = headers)
    # response = urllib2.urlopen(request)

    response = requests.get(url, headers=headers)
    data = response.content
    with open("choubai.html", "w") as f:
        f.write(data)

    content = data.decode('utf-8')
    pattern = re.compile('<div.*?author clearfix">.*?<a.*?<img src="(.*?)".*?' +
                         '</a>.*?<a href="/users/.*?<h2>(.*?)</h2>.*?<div.*?' +
                         'content">.*?<span>(.*?)</span>.*?<div class="' +
                         'stats.*?class="number">(.*?)</i>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        print(item[1] + u":" + item[0])
        print("")
        print(item[2])
        print(item[3] + u" 人觉得好笑")
        print("\n" * 3)
        SaveImg(item[0])
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print(e.code)
    if hasattr(e, "reason"):
        print(e.reason)

pass
