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
import logging
import traceback


class Model_Spider:
    def __init__(self):
        self.__main_url = "https://mm.taobao.com/json/request_top_list.htm"
        self.__dir = "LadysImage/"

    def __GetPageByURL(self, url):
        try:
            response = requests.get(url).content
        except:
            print traceback.format_exc()
            return ""
        return response

    def __GetPageByNum(self, page_num):
        single_page_url = self.__main_url + "?page=" + str(page_num)
        return self.__GetPageByURL(single_page_url)

    def __GetAllInfo(self, page_data):
        pattern = re.compile('<div class="list-item".*?pic s60.*?href="(.*?)".*?<img src="(.*?)".*?class' +
                             '="lady-name".*?href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?' +
                             '<span>(.*?)</span>', re.S)
        items = re.findall(pattern, page_data)

        ladys_info = {}
        for item in items:
            img_page = item[0]
            icon = item[1]
            info_page = item[2]
            name = item[3]
            age = item[4]
            address = item[5]
            ladys_info.update({name + '_' + age + '_' + address: (info_page, img_page)})
        return ladys_info

    def __GetPersonalInfo(self, personal_url):
        pass

    def __GetPersionalImages(self, dirname, image_page):
        response = self.__GetPageByURL(image_page)
        pattern = re.compile('<img.*?style=".*?src="(.*?)"', re.S)
        items = re.findall(pattern, response)

        if not items:
            return

        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        image_num = 0
        for item in items:
            prex = item[item.rfind('.'):]
            image_url = "http:" + item.strip('\t')
            filename = dirname + '/' + str(image_num) + prex
            self.__SaveImages(filename, image_url)
            image_num = image_num + 1

    def __SaveImages(self, filename, image_url):
        try:
            image = self.__GetPageByURL(image_url)
            if not image:
                return
            with open(filename, "wb") as f:
                f.write(image)
        except:
            print "Save image error:" + filename

    def Start(self):
        start = 1
        end = 10
        try:
            for i in range(start, end):
                page_info = self.__GetPageByNum(i)
                ladys_info = self.__GetAllInfo(page_info.decode("gbk"))

                for dirname, pages_info in ladys_info.items():
                    image_page = pages_info[1]
                    self.__GetPersionalImages(self.__dir + dirname, "http:" + image_page)
                pass
        except:
            print traceback.format_exc()
        pass


spider = Model_Spider()
spider.Start()

with open("taobao_model.html", "w") as f:
    response = requests.get("https://mm.taobao.com/photo-141234233-10001069307.htm?pic_id=10007138677")
    f.write(response.content)
