"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : BSTest.py
 @Time    : 2018/11/27 17:32
"""
from bs4 import BeautifulSoup

config_name = "DataCfgWifi.xml"

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

soup = BeautifulSoup(html_content, "lxml")

# ------------------------------------Tag----------------------------------------------
p_tag = soup.p
print("type(p_tag) -> ", type(p_tag))  # <class 'bs4.element.Tag'>
print("p_tag.name -> ", p_tag.name)  # p
print("p_tag.attrs -> ", p_tag.attrs)  # {'class': ['title', 'story'], 'name': 'dromouse story'}
print("p_tag['class'] -> ", p_tag["class"])  # ['title', 'story']
print("p_tag['name'] -> ", p_tag["name"])  # dromouse story
print("\n")

p_tag["newer"] = "new story name not know"
print("p_tag -> ",
      p_tag)  # <p class="title story" name="dromouse story" newer="new story name not know">The Dormouse's story</p>
print("\n")

del p_tag["newer"]
print("p_tag -> ", p_tag)  # <p class="title story" name="dromouse story">The Dormouse's story</p>
print("\n")

# ------------------------------------NavigableString ----------------------------------------------
print("p_tag.string -> ", p_tag.string)  # The Dormouse's story
print("type(p_tag.string) -> ", type(p_tag.string))  # <class 'bs4.element.NavigableString'>

p_tag.string = "helloword"
print("p_tag -> ", p_tag)  # 文档中说不能这么用，但是......
p_tag.string.replace_with("No longer bold")
print("p_tag -> ", p_tag)  # <p class="title story" name="dromouse story">No longer bold</p>
print("\n")

# ------------------------------------BeautifulSoup----------------------------------------------
print("type(soup) -> ", type(soup))  # <class 'bs4.BeautifulSoup'>
print("soup.name - > ", soup.name)  # [document]
print("\n")

# ------------------------------------Comment----------------------------------------------
# from bs4.element import Comment
# markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
# soup = BeautifulSoup(markup, 'lxml')
# comment = soup.b.string
# print(type(comment))        # <class 'bs4.element.Comment'>
# if type(comment) == Comment:
#     print(comment)          # Hey, buddy. Want to buy a used parser?

# ------------------------------------遍历文档树----------------------------------------------

print("soup.head -> ", soup.head)  # <head><title>The Dormouse's story</title></head>
print("soup.title -> ", soup.title)  # <title>The Dormouse's story</title>
print("soup.head.title -> ", soup.head.title)  # <title>The Dormouse's story</title>
print("\n")

# 获取子节点
body_tag = soup.body
contents = body_tag.contents
print("type(contents) -> ", type(contents))  # <class 'list'>
for content in contents:
    if content != "\n":
        print(content)
print("\n")

children = body_tag.children
print("type(children) -> ", type(children))  # <class 'list_iterator'>
for child in children:
    if child != "\n":
        print(child)
print("\n")

# 获取子孙节点
descendants = body_tag.descendants
print("type(descendants) -> ", type(descendants))  # <class 'generator'>
for child in descendants:
    if child != "\n":
        print(child)
print("\n")

# .strings 和 .stripped_strings

print("soup.html.string -> ", soup.html.string)  # None
html_strings = soup.html.strings
print("type(html_strings) -> ", type(html_strings))  # <class 'generator'>
for string in html_strings:
    print(string)
print("\n")

html_stripped_strings = soup.html.stripped_strings
print("type(html_stripped_strings) -> ", type(html_stripped_strings))  # <class 'generator'>
for string in html_stripped_strings:
    print(string)
print("\n")

# 获取父节点
p_tag = soup.p
p_parent = p_tag.parent
print("type(p_parent) -> ", type(p_parent))  # <class 'bs4.element.Tag'>
print("type(soup.parent) -> ", type(soup.parent))  # <class 'NoneType'>

for parent in p_tag.parents:
    if parent is None:
        print("None")
    else:
        print(parent.name)
print("\n")

# 获取兄弟节点
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>", "lxml")
print("sibling_soup.b.previous_sibling -> ", sibling_soup.b.previous_sibling)  # None
print("sibling_soup.b.next_sibling -> ", sibling_soup.b.next_sibling)  # <c>text2</c>
print("sibling_soup.c.previous_sibling -> ", sibling_soup.c.previous_sibling)  # <b>text1</b>
print("sibling_soup.c.next_sibling -> ", sibling_soup.c.next_sibling)  # None

print("p_tag.next_sibling -> ", p_tag.next_sibling)  # \n
print("p_tag.next_sibling.next_sibling -> ", p_tag.next_sibling.next_sibling)
print("p_tag.next_sibling.next_sibling.next_sibling -> ", p_tag.next_sibling.next_sibling.next_sibling)  # \n
print("p_tag.next_sibling.next_sibling.next_sibling.next_sibling -> ",
      p_tag.next_sibling.next_sibling.next_sibling.next_sibling)  # <p class="story">...</p>
print("\n")

print("type(p_tag.previous_siblings) -> ", type(p_tag.previous_siblings))  # <class 'generator'>
print("type(p_tag.next_siblings) -> ", type(p_tag.next_siblings))  # <class 'generator'>
for next_siling in p_tag.next_siblings:
    if next_siling == "\n":
        continue
    print(next_siling)
print("\n")

# 元素
last_a_tag = soup.find("a", id="link3")
print("last_a_tag -> ", last_a_tag)  # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
print("last_a_tag.next_sibling -> ", last_a_tag.next_sibling)  # ;and they lived at the bottom of a well.
print("last_a_tag.next_element -> ", last_a_tag.next_element)  # Tillie
print("\n")

# ------------------------------------搜索文档树----------------------------------------------
import re

print('soup.find_all("title") -> ', soup.find_all("title"))
print('soup.find_all(re.compile("tit")) -> ', soup.find_all(re.compile("tit")))
print('soup.find_all(["a", "title"]) -> ', soup.find_all(["a", "title"]))

for tag in soup.find_all(True):
    print(tag.name)


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


print('soup.find_all(has_class_but_no_id) -> ', soup.find_all(has_class_but_no_id))
print("\n")

print('soup.find_all(id="link2") -> ', soup.find_all(id="link2"))

data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', "lxml")
# data_soup.find_all(data-foo="value")
print('data_soup.find_all(attrs={"data-foo": "value"}) -> ', data_soup.find_all(attrs={"data-foo": "value"}))

print('soup.find_all("a", class_="body")) -> ', soup.find_all("a", class_="sister"))
