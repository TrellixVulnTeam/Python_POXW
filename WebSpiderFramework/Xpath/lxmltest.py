"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : lxmltest.py
 @Time    : 2018/11/29 9:49
"""
from lxml import etree

html_name = "test.html"

html_content = """
<html>
    <head>
        <title>The Dormouse's story</title>
    </head>
    <body>
        <p class="title story" name="dromouse story">The Dormouse's story</p>
        <p class="story">
            Once upon a time there were three little sisters; and their names were
            <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
            <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> 
            and
            <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>
            ;and they lived at the bottom of a well.
        </p>
        <p class="story">...</p>
    </body>
</html>
"""

root_node_fromstring = etree.fromstring(html_content)
print(root_node_fromstring.tag)
print(root_node_fromstring.values())

root_node_HTML = etree.HTML(html_content)  # 处理string类型
print(root_node_HTML.tag)

root_node_parse = etree.parse(html_name)
print(root_node_parse.docinfo)

a_node_list = root_node_parse.xpath("//p/a")
for a_node in a_node_list:
    print('{a_base} {a_line}: <{a_tag} href="{a_href}" class="{a_class}" id="{a_id}">{a_text}</{a_tag}>'.format(
        a_base = a_node.base,
        a_line = a_node.sourceline,
        a_tag = a_node.tag,
        a_href = a_node.attrib["href"],
        a_class = a_node.attrib["class"],
        a_id = a_node.attrib["id"],
        a_text = a_node.text))

p_node_list = root_node_parse.xpath("//p")
for p_node in p_node_list:
    a_node_list = p_node.xpath("./a")
    for a_node in a_node_list:
        print('{a_base} {a_line}: <{a_tag} href="{a_href}" class="{a_class}" id="{a_id}">{a_text}</{a_tag}>'.format(
            a_base = a_node.base,
            a_line = a_node.sourceline,
            a_tag = a_node.tag,
            a_href = a_node.attrib["href"],
            a_class = a_node.attrib["class"],
            a_id = a_node.attrib["id"],
            a_text = a_node.text))

p = root_node_parse.xpath("//p[@class='title story']")[0].text
pass