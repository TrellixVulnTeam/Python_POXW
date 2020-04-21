#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: suds_test.py
@time: 2020/4/21
@author: alfons
"""
from suds.client import Client

url = 'https://api.profitbricks.com/1.3/wsdl'
client = Client(url)
print client