#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: http_client.py 
@time: 2017/7/21 11:36 
@version: v1.0 
"""
import requests
import json
import urllib

server_url = "http://192.168.2.191"

if __name__ == '__main__':
    zr_content = requests.get(url = "http://192.168.2.191/Settings/zr/SetSetting?cfg=%7B%22zrall%22%3A%220%22%2C%22os%22%3A%5B%7B%22id%22%3A0%2C%22cve%22%3A1%2C%22down%22%3A%7B%22enable%22%3A0%7D%2C%22web%22%3A%7B%22enable%22%3A0%7D%2C%22jump%22%3A%7B%22enable%22%3A1%2C%22hosts%22%3A%5B%7B%22from%22%3A%22qq.com%22%2C%22to%22%3A%22sohu.com%22%7D%2C%7B%22from%22%3A%22sdfasfdsa%22%2C%22to%22%3A%22ssssss%22%7D%5D%7D%7D%2C%7B%22id%22%3A1%2C%22cve%22%3A1%2C%22down%22%3A%7B%22enable%22%3A0%7D%2C%22web%22%3A%7B%22enable%22%3A1%2C%22interval%22%3A%22300%22%2C%22pageid%22%3A0%7D%2C%22jump%22%3A%7B%22enable%22%3A1%2C%22hosts%22%3A%5B%7B%22from%22%3A%22qq.com%22%2C%22to%22%3A%22sohu.com%22%7D%2C%7B%22from%22%3A%22baidu.com%22%2C%22to%22%3A%22sohu.com%22%7D%5D%7D%7D%5D%7D")
    print zr_content.content

    sys_resouce = json.loads(requests.get(url = server_url + "/SysResourceInfo.json").content)
    print sys_resouce

    dicts_info_json = requests.get(url = server_url + "/Settings/crackdict/GetDict").content
    print dicts_info_json

    # 字典上传
    # upload_dict_url = server_url + "/Settings/crackdict/UploadDict?name=" \
    #                   + urllib.quote("最好的字典2") + "&des=" \
    #                   + urllib.quote("this is user dict")
    # files = {"data": open("dict2", "rb")}
    # dicts_upload = requests.post(url = upload_dict_url, files = files)
    # if json.loads(dicts_upload.content)["result"] == '0':
    #     print "dict upload success!"
    # else:
    #     print "dict upload fail!"

    # 字典次序修改
    # dicts_info = json.loads(dicts_info_json)
    # dicts_list = dicts_info["dict"]
    # dicts_num = len(dicts_list)
    # dicts_seq_list = []
    # for i in range(0, dicts_num):
    #     id = str(input("dict_id:"))
    #     seq = str(input("dict_seq:"))
    #     dicts_seq_list.append({"id": id, "s": seq})
    # dicts_seq = {"dict": dicts_seq_list}
    # dicts_seq_content = requests.post(url = server_url + "/Settings/crackdict/adjustDicts",
    #                                   json = json.dumps(dicts_seq))
    # if json.loads(dicts_seq_content.content)["result"] == '0':
    #     print "dict change seq success!"
    # else:
    #     print "dict change seq fail!"

    # 删除字典
    # idlist = raw_input("idlist is :")
    # dicts_del_info = requests.get(url = server_url+"/Settings/crackdict/DelDict?idlist="+ urllib.quote(idlist))
    # if json.loads(dicts_del_info.content)["result"] == '0':
    #     print "del dict success!"
    # else:
    #     print "del dict fail!"

    dicts_info_json = requests.get(url = server_url + "/Settings/crackdict/GetDict").content
    print dicts_info_json
    pass
