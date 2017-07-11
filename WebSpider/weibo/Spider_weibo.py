#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Spider_weibo.py 
@time: 2017/7/11 11:01 
@version: v1.0
"""
import urllib
import urllib2

url = "http://weibo.com/?topnav=1&mod=logo"
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}
try:
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    with open("weibo.html", "w") as f:
        f.write(response.read())
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

pass
