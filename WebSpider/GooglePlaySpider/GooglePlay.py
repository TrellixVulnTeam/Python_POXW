#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: GooglePlay.py 
@time: 2017/12/26 17:29 
@version: v1.0 
"""
import requests

url = "https://play.google.com/store/apps/details?id=com.imo.android.imoim"

session = requests.session()
result = session.get(url = url)
content = result.content
with open("GooglePlay.html", "w") as f:
    f.write(content)
pass