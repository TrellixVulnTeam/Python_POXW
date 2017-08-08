#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: model.py 
@time: 2017/7/11 16:58 
@version: v1.0 
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import re
import os
import time
import threading
import logging
import traceback
from WebSpider import SpiderBase

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {'User-Agent': user_agent}


def GetPageByURL(url):
    try:
        response = requests.get(url = url,timeout = 0.5).content
    except:
        print traceback.format_exc()
        return ""
    return response


def SaveImages(filename, image_url):
    try:
        image = GetPageByURL(image_url)
        if not image:
            return
        with open(filename, "wb") as f:
            f.write(image)
    except:
        print "Save image error:" + filename


class Model_Spider:
    def __init__(self):
        self.__main_url = "https://mm.taobao.com/json/request_top_list.htm"
        self.__dir = "LadysImage/"

    def __GetPageByNum(self, page_num):
        single_page_url = self.__main_url + "?page=" + str(page_num)
        return GetPageByURL(single_page_url)

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
        try:
            response = GetPageByURL(image_page)
            pattern = re.compile('<img.*?style=".*?src="(.*?)"', re.S)
            items = re.findall(pattern, response)

            if not items:
                with open("taobao_model.html", "w") as f:
                    f.write(response)
                return

            if not os.path.isdir(dirname):
                os.makedirs(dirname)

            image_num = 0
            for item in items:
                if image_num % 10 == 0:
                    time.sleep(3)
                prex = item[item.rfind('.'):]
                image_url = "https:" + item.strip('\t')
                filename = dirname + '/' + str(image_num) + prex
                SaveImages(filename, image_url)
                # threading.Thread(target = SaveImages, args = (filename, image_url), name = filename).start()
                image_num = image_num + 1
        except:
            print traceback.format_exc()

    def Start(self):
        start = 1
        end = 200
        try:
            for i in range(start, end):
                page_info = self.__GetPageByNum(i)
                ladys_info = self.__GetAllInfo(page_info.decode("gbk"))

                img_num = 0
                for dirname, pages_info in ladys_info.items():
                    if img_num % 10 == 0:
                        time.sleep(5)
                    image_page = pages_info[1]
                    threading.Thread(target = self.__GetPersionalImages,
                                     args = (self.__dir + dirname, "https:" + image_page),
                                     name = self.__dir + dirname).start()
                    # self.__GetPersionalImages(self.__dir + dirname, "https:" + image_page)
                pass
        except:
            print traceback.format_exc()
        pass


spider = Model_Spider()
spider.Start()

# 判断文件夹是否有文件存在
# dirs = os.listdir("LadysImage")
# for dir in dirs:
#     dir_path = "LadysImage/" + dir
#     if SpiderBase.IsDirEmpty(dir_path):
#         os.rmdir(dir_path)
pass



# with open("taobao_model.html", "w") as f:
#     response = requests.get("https://mm.taobao.com/photo-141234233-10001069307.htm?pic_id=10007138677")
#     f.write(response.content)
