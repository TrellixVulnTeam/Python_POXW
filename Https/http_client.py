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
    sys_resouce = json.loads(requests.get(url = server_url + "/SysResourceInfo.json").content)
    print sys_resouce

    dicts_info_json = requests.get(url = server_url + "/Settings/crackdict/GetDict").content
    print dicts_info_json

    # 字典上传
    upload_dict_url = server_url + "/Settings/crackdict/UploadDict?name=" \
                      + urllib.quote("最好的字典2") + "&des=" \
                      + urllib.quote("this is user dict")
    files = {"data": open("dict2", "rb")}
    dicts_upload = requests.post(url = upload_dict_url, files = files)
    if json.loads(dicts_upload.content)["result"] == '0':
        print "dict upload success!"
    else:
        print "dict upload fail!"

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
