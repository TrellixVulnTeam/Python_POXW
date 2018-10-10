"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : CrackCenterTest.py
 @Time    : 2018/9/17 9:30
"""
import requests
import json

host = "http://192.168.2.68:5000"
# host = "http://112.86.129.67:5000"
UploadCrackTaskUrl = host + "/UploadCrackTask"
GetCrackStatusUrl = host + "/GetCrackStatus?taskId={taskId}"
GetCrackDeviceStatusUrl = host + "/GetCrackDeviceStatus"
CrackPauseUrl = host + "/CrackPause?taskId={taskId}"
CrackResumeUrl = host + "/CrackResume?taskId={taskId}"


def Test_UploadCrackTask(taskId, ssid, mac, rules=None):
    form = dict(taskId=taskId, ssid=ssid, mac=mac, rules=rules)
    file = dict(capFile=open("./wpa.hccapx", "rb"))

    content = requests.post(UploadCrackTaskUrl, files=file, data=form).content
    print("UploadCrackTask:", content.decode("unicode-escape"))


def Test_GetCrackStatus(taskId):
    content = requests.get(GetCrackStatusUrl.format(taskId=taskId)).content
    print("GetCrackStatus:", content.decode("unicode-escape"))


def Test_GetCrackDeviceStatus():
    content = requests.get(GetCrackDeviceStatusUrl).content
    print("CrackPause:", content.decode("unicode-escape"))


def Test_CrackPause(taskId):
    content = requests.get(CrackPauseUrl.format(taskId=taskId)).content
    print("CrackPause:", content.decode("unicode-escape"))


def Test_CrackResume(taskId):
    content = requests.get(CrackResumeUrl.format(taskId=taskId)).content
    print("CrackResume:", content.decode("unicode-escape"))


if __name__ == "__main__":
    import time

    test = list(range(19)) or list()

    taskId = "15"
    Test_UploadCrackTask(taskId, "helloworld", "12:34:12:12:34:12")
    # Test_UploadCrackTask(taskId, "helloworld", "12:34:12:12:34:12", json.dumps(["?1?2?d", "?l?h?d"]))
    # Test_UploadCrackTask(taskId, "helloworld", "12:34:12:12:34:12", json.dumps(["?d?d?d?d?d?d?d?d?d?d?d"]))
    # Test_GetCrackStatus(taskId)
    #
    # time.sleep(3)
    Test_CrackPause(taskId)
    Test_GetCrackStatus(taskId)
    #
    # Test_CrackResume(taskId)
    # Test_GetCrackStatus(taskId)

    Test_GetCrackDeviceStatus()