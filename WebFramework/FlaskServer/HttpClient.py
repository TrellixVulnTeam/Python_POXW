"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : HttpClient.py
 @Time    : 2018/8/7 9:45
"""
import requests
from lxml import etree

resp = requests.get(url="http://127.0.0.1:5000/xml")
content = resp.content.decode()
with open("xm.xml", "w") as f:
    f.write(content)
# xmlData = etree.parse("xm.xml", etree.XMLParser(resolve_entities=False))
xmlData = etree.parse("xm.xml")
pass