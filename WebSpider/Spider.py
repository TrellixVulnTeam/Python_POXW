#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Spider.py 
@time: 2017/7/10 15:39 
@version: v1.0 
"""
import urllib2

# 1、直接访问
# response = urllib2.urlopen("http://192.168.2.183")
# print response.read()

# 2、先request再访问
# request = urllib2.Request("http://www.baidu.com")
# response = urllib2.urlopen(request)
# print response.read()

# 3、使用代理服务器访问
proxy_handler = urllib2.ProxyHandler({"http": "192.168.2.40:8787"})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

request = urllib2.Request("https://www.cnblogs.com")
response = urllib2.urlopen(request)
print response.read()
pass
