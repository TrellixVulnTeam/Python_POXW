"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : lxmltest.py
 @Time    : 2018/11/29 9:49
"""
from lxml import etree

xml_name = "books.xml"

# root_node = etree.XML(xml_contents)       # 处理string类型
root_node = etree.parse(xml_name)

book_node_list = root_node.xpath("//book")
for book_node in book_node_list:
    book_title = book_node.xpath("//title")
    for book in book_title:
        print(book.text)
