"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : EstrongsEmbed.py
 @Time    : 2018/8/22 16:05
"""
import requests
import json

TARGET_HOST = "http://172.21.33.3:59777"


def CommandRequest(**kwargs):
    command_dict = {key: value for key, value in kwargs.items()}
    headers = {"Content-Type": "application/json"}

    response = requests.post(TARGET_HOST, json=command_dict, headers=headers)
    if response.status_code == 200:
        return response.content


def ModifyResponse(response):
    return response.replace(b", },", b"},")[:-4] + b"]" if len(response) > 4 else response


if __name__ == "__main__":
    listApps = json.loads(CommandRequest(command="listApps"))
    listAppsAll = json.loads(CommandRequest(command="listAppsAll"))
    listPics = json.loads(ModifyResponse(CommandRequest(command="listPics")))
    listVideos = json.loads(ModifyResponse(CommandRequest(command="listVideos")))
    listAudios = json.loads(ModifyResponse(CommandRequest(command="listAudios")))

    getDeviceInfo = json.loads(CommandRequest(command="getDeviceInfo"))
    appLaunch = json.loads(CommandRequest(command="appLaunch", appPackageName="com.estrongs.android.pop"))

    # appPull = CommandRequest(command="appPull", appPackageName="com.tencent.mm")  # 获取目标apk
    # with open("WeChat.apk", "wb") as f:
    #     f.write(appPull)

    print(appLaunch)
    print(listApps)
    print(listAppsAll)
    print(listPics)
    print(listVideos)
    print(listAudios)

    # url = "http://172.30.166.2:42135/hostname"
    # data = "172.30.166.1"
    #
    # respone = requests.get(url, data=data)
    # print(respone.request.headers)
    # print(respone.content)
