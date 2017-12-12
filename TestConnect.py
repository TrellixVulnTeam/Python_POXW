#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: TestConnect.py 
@time: 2017/9/18 12:41 
@version: v1.0 
"""

import requests
import time
import logging
import traceback


def testConnection():
    content = requests.get(url="http://download.aircrack-ng.org/aircrack-ng-1.2-rc3.tar.gz").content
    pass
    with open("hostapd-2.4.tar.gz", "wb") as f:
        f.write(content)


if __name__ == "__main__":
    while True:
        try:
            testConnection()
        except:
            with open("log.txt", "a") as f:
                f.write("Except:%s" % traceback.format_exc())
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                f.write("\n")
        finally:
            time.sleep(30)

