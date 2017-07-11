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
import os


class Model_Spider:
    def __init__(self):
        self.__main_url = "https://mm.taobao.com/json/request_top_list.htm"

    def __GetSinglePage(self, page_num):
        single_page_url = self.__main_url + "?page=" + str(page_num)
        response = requests.get(single_page_url)
        return response.content

    def __GetAllInfo(self, page_data):
        pattern = re.compile('<div class="list-item">.*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>'
                             + '(.*?)</strong>.*?<span>(.*?)</span>.*? <div class="pic w610">.*?<a href="(.*?)" '
                             + 'target="_blank">', re.S)
        items = re.findall(pattern, page_data)

        ladys_info = {}
        for item in items:
            info_page = item[0]
            name = item[1]
            age = item[2]
            address = item[3]
            img_page = item[4]
            ladys_info.update({name + '_' + age + '_' + address: (info_page, img_page)})
        return ladys_info

    def __GetPersonalInfo(self, personal_url):
        pass

    def __GetAllImage(self):
        pass

    def __SaveImages(self, dirname, filename, image):
        try:
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            with open(filename, "wb") as f:
                f.write(image)
        except:
            print "Save image error:" + dirname + "\t" + filename

    def Start(self):
        start = 1
        end = 10
        for i in range(start, end):
            page_info = self.__GetSinglePage(i)
            ladys_info = self.__GetAllInfo(page_info.decode("gbk"))
            pass
        pass


spider = Model_Spider( )
spider.Start()

with open("taobao_model.html", "w") as f:
    response = requests.get("https://mm.taobao.com/json/request_top_list.htm?page=1")
    f.write(response.content)
