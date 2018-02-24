#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: AddImportPersons.py 
@time: 2017/12/29 17:28 
@version: v1.0 
"""
import requests

proxies = {
    'http': 'socks5h://root:yg_root\@9985@218.2.173.188:8888',
    'https': 'socks5h://root:yg_root\@9985@218.2.173.188:8888'
}

one_in = "192.168.7.103"
one_out = "192.168.7.105"
two_in = "192.168.7.102"
two_out = "192.168.7.118"
thrid_in = "192.168.7.101"
thrid_out = "192.168.7.115"
ele_room = "192.168.7.114"

device_room = [one_in, one_out, two_in, two_out, thrid_in, thrid_out, ele_room]

mac_list = ["9C:FB:D5:EA:FF:47", "1C:DA:27:6C:DB:E6", "00:0C:E7:80:39:9F", "08:23:B2:57:7B:F6",
            "18:E2:9F:1F:43:D6", "34:78:D7:9F:73:45", "EC:5A:86:A2:9E:42", "EC:DF:3A:75:A0:9C",
            "E8:BB:A8:A0:0F:D5", "38:A4:ED:AB:38:16", "C4:0B:CB:87:C0:61", "14:36:C6:E8:68:82",
            "DC:6D:CD:9A:95:EC", "3C:F5:91:75:A7:B1", "A4:44:D1:D0:FF:A9"]

url = "http://%s/Task/TaskNewObj?taskid=2&name=%s&description=%s&keytype=0&key=%s"
for ip in device_room:
    for mac_a in mac_list:
        uri = url % (ip, mac_list.index(mac_a) + 10, mac_list.index(mac_a) + 10, mac_a)
        content = requests.get(uri, proxies = proxies).content
