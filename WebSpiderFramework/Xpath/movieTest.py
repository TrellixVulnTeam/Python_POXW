"""
@author: Alfons
@contact: alfons_xh@163.com
@file: movieTest.py
@time: 18-12-26 下午11:52
@version: v1.0 
"""
from lxml import etree

movie_html = "./movie_info_html.html"

with open(movie_html, 'r') as f:
    root_node_parse = etree.HTML(f.read())

script = root_node_parse.xpath("//script[@type='application/ld+json']")
pass