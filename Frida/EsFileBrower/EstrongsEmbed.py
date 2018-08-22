"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : EstrongsEmbed.py
 @Time    : 2018/8/22 16:05
"""
import requests
import json

TARGET_HOST = "http://172.19.13.2:59777"


def CommandRequest(command):
    command_dict = dict(command=command)
    headers = {"Content-Type": "application/json"}

    response = requests.post(TARGET_HOST, json=command_dict, headers=headers)
    if response.status_code == 200:
        return response.content


def ModifyResponse(response):
    return response.replace(b", },", b"},")[:-4] + b"]"


if __name__ == "__main__":
    listApps = json.loads(CommandRequest("listApps"))
    listAppsAll = json.loads(CommandRequest("listAppsAll"))
    listPics = json.loads(ModifyResponse(CommandRequest("listPics")))
    listVideos = json.loads(ModifyResponse(CommandRequest("listVideos")))
    listAudios = json.loads(ModifyResponse(CommandRequest("listAudios")))

    print(listApps)
    print(listAppsAll)
    print(listPics)
    print(listVideos)
    print(listAudios)
