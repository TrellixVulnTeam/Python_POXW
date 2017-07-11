#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: model.py 
@time: 2017/7/11 16:58 
@version: v1.0 
"""
import requests
import re


class Model_Spider:
    def __init__(self):
        self.__main_url = "https://mm.taobao.com/json/request_top_list.htm"

    def __GetSinglePage(self, page_num):
        single_page_url = self.__main_url + "?page=" + str(page_num)
        response = requests.get(single_page_url)
        return response.content

    def __GetAllPersonalInfo(self,page_data):
        pattern = re.compile('<div class="list-item">.*?<div class="personal-info">.*?')
        pass

    def __GetPersonalInfo(self,personal_url):
        pass

    def __GetAllImage(self):
        pass

    def __SaveImages(self):
        pass

    def Start(self):



spider = Model_Spider()
with open("taobao_model.html","w") as f:
    pass