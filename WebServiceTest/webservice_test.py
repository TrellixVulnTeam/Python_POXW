#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: suds_test.py
@time: 2020/4/21
@author: alfons
"""

from suds.client import Client
from suds.xsd.doctor import ImportDoctor, Import

imp = Import('http://www.w3.org/2001/XMLSchema',
             location='http://www.w3.org/2001/XMLSchema.xsd')
imp.filter.add('http://WebXml.com.cn/')

doctor = ImportDoctor(imp)
url = 'http://ws.webxml.com.cn/WebServices/WeatherWS.asmx?wsdl'
# c = Client(url)
c = Client(url, doctor=doctor)
print c

getRegionCountry = c.service.getRegionCountry()

print "c.service.getRegionCountry() -> ", c.service.getRegionCountry()
# print "c.service.getRegionDataset() -> ", c.service.getRegionDataset()
# print "c.service.getRegionProvince() -> ", c.service.getRegionProvince()
# print c.service.getSupportCityDataset("上海")
# print c.service.getSupportCityString("上海")
