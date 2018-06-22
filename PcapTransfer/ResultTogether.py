#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ResultTogether.py 
@time: 2018/4/9 16:54 
@version: v1.0 
"""
import os
import json

threshold = 1      # 文件出现的临界值，大于等于此值需要记录

resultDir = "C:/Users/xiaohui/Desktop/南京pcap文件处理结果"
pcapSaveDir = "E:/SignatureAnalysis/pcapSave"

resultList = list()
subDir = [dir for dir in os.listdir(resultDir) if not os.path.isfile(os.path.join(resultDir, dir))]
for dir in subDir:
    resultList += [os.path.join(resultDir, dir, f) for f in os.listdir(os.path.join(resultDir, dir)) if f.endswith(".json")]

countList = list()  # 记录文件出现的数量
resultDict = dict()         # 记录文件的基本信息
for resultFile in resultList:
    resultJsonName = os.path.basename(resultFile)
    with open(resultFile, "r") as f:
        singleResult = json.loads(f.read())

    for fileName, fileInfo in singleResult.items():
        # if not fileInfo.get("files"):
        #     continue

        if fileName in countList:
            resultDict[fileName]["count"] += 1
            resultDict[fileName]["pcap"].update({resultJsonName[:resultJsonName.rfind('.')] + ".pcap": fileInfo.get("pduNumber")})
            resultDict[fileName]["host"].add(fileInfo.get("host"))
            resultDict[fileName]["url"].add(fileInfo.get("url"))
            resultDict[fileName]["file"] |= {f for f in fileInfo.get("files")}
        else:
            resultDict.update({fileName: {
                "count": 1,
                "file": {f for f in fileInfo.get("files")},
                "host": {fileInfo.get("host")},
                "url": {fileInfo.get("url")},
                "pcap": {resultJsonName[:resultJsonName.rfind('.')] + ".pcap": fileInfo.get("pduNumber")}
            }})
            countList.append(fileName)

key_list = list(resultDict.keys())
for key in key_list:
    if resultDict[key]["count"] < threshold:
        del resultDict[key]
        continue
    resultDict[key]["host"] = list(resultDict[key]["host"])
    resultDict[key]["url"] = list(resultDict[key]["url"])
    resultDict[key]["file"] = list(resultDict[key]["file"])

# 过滤非apk后缀的信息
resultDict = {key: value for key, value in resultDict.items() if not key.endswith(".apk")}

from collections import OrderedDict

orderResult = OrderedDict(sorted(resultDict.items(), key=lambda t: t[1]["count"], reverse=True))

with open(os.path.join(resultDir, "SummaryResult.json"), "w") as f:
    f.write(json.dumps(orderResult))

# for key, value in result_dict.items():
#     pcapName = os.path.join(pcap_dir, key[:key.rfind('.json')] + ".pcap")
#     dstPath = os.path.join(pcap_analysis_dir, os.path.basename(pcapName))
#     shutil.copy(pcapName, dstPath)
pass
