"""
@author: Alfons
@contact: alfons_xh@163.com
@file: JsonParserDoubleSlash.py
@time: 2019/5/24 上午7:04
@version: v1.0 
"""

import json

test_str = {"name": "alfons", "city": "杭州"}

json_dumps = json.dumps(test_str, ensure_ascii=False)

test_str_2 = json_dumps.encode("unicode_escape")
print(test_str_2)

json_loads = json.loads(test_str_2, )
print(json_loads)

wait_str = '{"name": "alfons", "city": "\\\\u676d\\\\u5dde"}'
print(json.loads(wait_str.encode("unicode_escape")))

unicode_str = u"\u6211"
str_str = unicode_str.encode("unicode_escape")
print(unicode_str, ' -> ', str_str)

assert isinstance(unicode_str, str), "one"
assert isinstance(unicode_str, int), "two"
