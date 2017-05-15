#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ReadXml.py 
@time: 2017/5/15 15:01 
@version: v1.0 
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xml.dom.minidom

dom = xml.dom.minidom.parse("C:\Users\shangchenhui\Desktop\SoftParserCfg.xml")
root = dom.documentElement
f = open("C:\Users\shangchenhui\Desktop\softName.csv","w")
for soft in root.getElementsByTagName("Software"):
    stringA = ""
    softID = str(soft.getElementsByTagName("SoftID")[0].firstChild.data)
    softname = soft.getElementsByTagName("Name")[0].firstChild.data
    version = soft.getElementsByTagName("Version")[0].firstChild.data
    stringA = softID + "," + softname + "," + version + "\n"
    f.write(stringA)
f.close()