#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: CloudTrojanServer.py 
@time: 2018/4/11 15:54 
@version: v1.0 
"""
from bottle import run, route, static_file, request, Bottle
import json

server = Bottle()


@server.route("/website/home")
def WebsiteHome():
    resDict = dict()
    resDict.update({u'isSuccess': True})
    resDict.setdefault("data", {u"sessionkey": u"86331CA8454FDC16C71629C0813D9DBC"})
    resDict["data"].update({"user": {"userId": 62}})
    return json.dumps(resDict)


@server.route("/RcsViewSys/transfer//RcsDataSys/client/aos/phantom-list")
def PhantomList():
    resDict = dict()
    resDict.update({
        u"data":
            {
                u"rows": [
                    {
                        u"id": 132,
                        u"clientType": 1,
                        u"wifilz-file":
                            {
                                u"file-name": u"wifilz.apk"
                            },
                        u"md5": u"7007659a88d8a7e3080354d9eb5fa354",
                        u"create-time": u"2018-03-12 08:01:20",
                        u"effectiveTime": u"1D2H0M0S"
                    },
                    {
                        u"id": 133,
                        u"clientType": 2,
                        u"wifilz-file":
                            {
                                u"file-name": u"0002.zip"
                            },
                        u"md5": u"0825dddf4238bd55a75da84c086cdb54",
                        u"create-time": u"2018-03-12 08:01:20",
                        u"effectiveTime": u"1D2H0M0S"
                    }
                ]
            }
    })
    return json.dumps(resDict)


@server.route("/RcsDataSys/client/aos/client-download")
def Download():
    clientId = request.query.get("client-id")

    if clientId == 132:
        fileName = "./wifi.apk"
    elif clientId == 133:
        fileName = "./0002.zip"
    else:
        fileName = ""

    with open(fileName, "rb") as f:
        return f.read()


@server.route("/website/logout")
def Logout():
    return "sucesss"


if __name__ == "__main__":
    server.run(host='127.0.0.1', port=8081)
