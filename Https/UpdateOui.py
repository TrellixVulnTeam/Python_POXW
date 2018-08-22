#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : UpdateOui.py
 @Time    : 2018/6/6 9:49
"""
import requests

OuiUpdateUrl = "http://standards-oui.ieee.org/oui.txt"

content = requests.get(url=OuiUpdateUrl).content.decode()

hexOuiList = [oui for oui in content.split("\n") if "(hex)" in oui]

pass
