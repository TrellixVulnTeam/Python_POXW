"""
@author: Alfons
@contact: alfons_xh@163.com
@file: LRU.py
@time: 2019/4/3 下午8:55
@version: v1.0 
"""
import collections


class LRU:
    def __init__(self, num):
        self.__len = num
        self.__cache = collections.OrderedDict()

    def get(self, key):
        """
        读取
        :param key: 待读取的key
        :return: 存在返回结果，不存在返回None
        """
        if key in self.__cache:
            value = self.__cache.pop(key)
            self.__cache[key] = value
            return value
        else:
            return None

    def put(self, key, value):
        """
        插入
        :param key: 待插入的key
        :param value: 带插入的value
        """
        if key in self.__cache:
            value = self.__cache.pop(key)
            self.__cache[key] = value
        else:
            if len(self.__cache) >= self.__len:
                self.__cache.popitem(last=False)

            self.__cache[key] = value


c = LRU(5)
