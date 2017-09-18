#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: TestConnect.py 
@time: 2017/9/18 12:41 
@version: v1.0 
"""

import socket


def testConnection(ipAddr, portNum):
    s = socket.socket()
    s.settimeout(1.0)
    try:
        s.connect((ipAddr, portNum))
        s.close()
        return True
    except:
        return False


if __name__ == "__main__":
    ports = {42203: "1栋里", 42205: "1栋外", 42202: "2栋里", 42218: "2栋外", 42201: "3栋里", 42215: "3栋外", 42214: "配电房"}
    # get IP addr：cat *.log | awk '{print $9}' | sort | uniq -c | awk '{print $2}'
    IpAddrs = ["58.212.246.126   "
,"58.212.246.126    "
,"114.221.180.38    "
,"121.229.156.248  "
,"121.229.156.248  "
,"121.229.156.248  "
,"180.110.166.24    "
,"180.110.166.24    "]
    connect_port_list = []
    for i in IpAddrs:
        for p, q in ports.items():
            if p in connect_port_list:
                continue
            if testConnection(i.strip(), p):
                connect_port_list.append(p)
                print 'SUCCESS:', i, p, q

