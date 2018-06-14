#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: main36.py
@time: 2017/12/28 17:28
@version: v1.0
"""
import json
import time

list_a = ["sd", 43, 65]
list_json = json.dumps(list_a)

set_a = {(254, "2018.03.29 11-12-30", "123456789", "wifi.apk"),
         (255, "2018.03.27 11-12-30", "1234567823", "lib.so")}

set_b = {(254, "2018.03.29 11-12-30", "123456789", "wifi.apk"),
         (255, "2018.03.27 11-12-30", "1234567823", "lib.so")}

diffSet = set_a - set_b
print(diffSet)

set_json = json.dumps(list(diffSet))
diffSet2 = {tuple(e) for e in json.loads(set_json)}

lastUpdateTime = max(set_a, key=lambda p: p[1])[1]

from collections import namedtuple

trojanFile = namedtuple("Trojan", "id,type,filename,md5,createtime,expiredtime")
file_1 = trojanFile(123, 1, "wifi.apk", "fsddfasfasfasdfdsafadsf", "2018-03-31 07:09:10", "2018-04-30 07:09:10")
trojansDict = {file_1.id: file_1}
with open("trojan.json", "w") as f:
    f.write(json.dumps(trojansDict))

with open("trojan.json", "r") as f:
    file_2 = json.loads(f.read())

trojansDict_2 = {key: trojanFile._make(value) for key, value in file_2.items()}

Cloud = 1


class TEST:
    def hello(self):
        global Cloud
        print(Cloud)


test = TEST()
test.hello()

from datetime import datetime
from datetime import timedelta


def SetExpiredtime(expiredtime):
    try:
        days = float(expiredtime[:expiredtime.find('d')])
        hours = float(expiredtime[expiredtime.find('d') + 1:expiredtime.find('h')])
        mins = float(expiredtime[expiredtime.find('h') + 1:expiredtime.find('m')])

        expiredDateStr = (datetime.now() + timedelta(days=days, hours=hours, minutes=mins)).strftime(
            "%Y-%m-%d %H:%M:%S")
        pass
    except:
        return ""


SetExpiredtime("25645d2h30m")

# import os
# import shutil
# file_src_dir = "E:\SignatureAnalysis\pcapSave"
# file_list = os.listdir("E:\SignatureAnalysis\pcapSave")
# for file in file_list:
#     file_src_path = os.path.join(file_src_dir, file)
#     file_dst_path = file_src_path + ".pcap"
#     shutil.move(file_src_path, file_dst_path)
time_a = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

recorde = [("foo", "1", "2"), ("bar", 12, 3)]
for res, *argv in recorde:
    print(res)
pass

import threading


def printHello(name):
    print("hello: %s" % name)


threading.Timer(3, printHello, ["xiaohui"]).start()

expiredtime = "2018-04-10 17:00:00"
expireddate = datetime.strptime(expiredtime, "%Y-%m-%d %H:%M:%S")
if expireddate < datetime.now():
    sec = (expireddate - datetime.now()).total_seconds()
    day = (expireddate - datetime.now()).days
    print(sec, day)

str_a = "1234"
str_b = str_a[-1]

import os

# os.remove("./1.txt")
pass

time_a = str(int(time.time()))

expiredtime = datetime.strptime("2018-04-10 08:05:02", "%Y-%m-%d %H:%M:%S")
if not isinstance(expiredtime, timedelta):
    pass

import base64

# with open("libadd.so", "rb") as f:
#     encodedZip = base64.b64encode(f.read())
#     with open("tmp.txt", "w") as f2:
#         f2.write(encodedZip.decode())
encodeZip = "90m74mD7r2qZQQoTA6G97Q=="
with open("libadd2.so", "wb") as f:
    f.write(base64.b64decode(encodeZip))
pass

list_a = [1, 2, 3, 4]
list_b = [4, 5, 6, 7]
list_a.extend(list_b)
pass

a = 5
b = 2
print("a / b=", a / b)
print("type(a)", type(a))

import threading

i = "dsafa".upper()
j = "".lower()


def OperationSuccess(**kwargs):
    """
    web接口返回处理成功信息
    :param kwargs: 其他字段
    :return:
    """
    successDict = dict(result=True)
    successDict.update({key: value for key, value in kwargs.items()})
    return json.dumps(successDict)


print(OperationSuccess())


def FindLast(srcList):
    dstList = list()
    for i in srcList[::-1]:
        if i not in dstList:
            dstList.append(i)
    return dstList[::-1]


if __name__ == "__main__":
    # os.removedirs("./1a")
    srcList = [1, 8, 7, 3, 8, 3, 1]
    tmpList = list()
    dstList = [tmpList.append(i) for i in srcList if i not in tmpList]
    print(dstList)
    print(FindLast(srcList))
    list_a = list()
    list_a.append(1)
    list_a.append(2)
    list_a.append(3)
    list_a.append(4)
    list_a.append(5)

pass
