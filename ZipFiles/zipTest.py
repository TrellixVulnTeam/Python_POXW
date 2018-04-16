#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: zipTest.py
@time: 2018/4/16 10:22 
@version: v1.0 
"""
import zipfile

if __name__ == "__main__":
    f = zipfile.ZipFile('filename.zip', 'w', zipfile.ZIP_DEFLATED)
    f.write("./Trojan/fhc", "fhc")
    f.write("./Trojan/wifi.json", "wifi.json")
    f.close()

    f = zipfile.ZipFile('filename.zip')
    print(f.namelist())
    print(f.infolist())
    f.printdir()
    f.extractall()
    f.close()