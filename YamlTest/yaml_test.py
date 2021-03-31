"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : yaml_test.py
 @Time    : 2019/3/21 11:31
"""
import yaml
from pprint import pprint

data = yaml.load(open("./test.yml", 'r'))
print("data's type is -> ", type(data))
print("data info -> ")
pprint(data)

