"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ipLocationThread.py
 @Time    : 2018/8/15 17:33
"""
import requests
import json
import traceback
import threading


def lookup(ip):
    URL = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    try:
        result = requests.get(URL)
        if result.status_code == 200:
            data = result.content
            json_data = json.loads(data)
            if json_data[u'code'] == 0:
                print("\nIP -> ", ip)
                print('所在国家： ' + json_data[u'data'][u'country'])
                print('所在地区： ' + json_data[u'data'][u'area'])
                print('所在省份： ' + json_data[u'data'][u'region'])
                print('所在城市： ' + json_data[u'data'][u'city'])
                print('所属运营商：' + json_data[u'data'][u'isp'])
    except:
        print("\n\nSomething error")
        traceback.print_exc()


with open("ip.txt", "r") as f:
    ipList = json.load(f).keys()

threadList = list()
for ip in ipList:
    ipThread = threading.Thread(target=lookup, args=(ip,))
    ipThread.start()
    threadList.append(ipThread)

for thread in threadList:
    thread.join()
