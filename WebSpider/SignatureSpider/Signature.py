#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Signature.py 
@time: 2018/1/23 18:59 
@version: v1.0 
"""
import re
import requests

url = "https://filesignatures.net/index.php?page=all&currentpage=%s&order=EXT"

session = requests.session()
content = session.get(url = url % 1).content
with open("signature.html", "wb") as f:
    f.write(content)

pass

