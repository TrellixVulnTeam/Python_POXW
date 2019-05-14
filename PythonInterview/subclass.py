"""
@author: Alfons
@contact: alfons_xh@163.com
@file: subclass.py
@time: 2019/4/6 下午9:15
@version: v1.0 
"""
from collections import UserList


class userdict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, value * 2)


user = userdict(d="100")
print(user)
user.update({'a': 200})
print(user)

user['c'] = [300]
print(user)

print(userdict.mro())
