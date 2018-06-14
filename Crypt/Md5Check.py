#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Md5Check.py 
@time: 2018/2/1 11:56 
@version: v1.0 
"""
import hashlib
from PyCRC.CRC32 import CRC32
from PyCRC.CRC16 import CRC16
from PyCRC.CRC16DNP import CRC16DNP
from PyCRC.CRC16Kermit import CRC16Kermit
from PyCRC.CRC16SICK import CRC16SICK
from PyCRC.CRCCCITT import CRCCCITT
import sys
import time


def md5(plaintext, time=1):
    """
    md5加密
    :param plaintext: 加密的字符串
    :param time: 加密迭代次数
    :return: 加密后的结果
    """
    tmp_time = 1
    m = hashlib.md5()
    m.update(plaintext)
    while tmp_time < time:
        # print m.hexdigest()
        m.update(m.hexdigest())
        tmp_time += 1
    return m.hexdigest()


for soft_name in sys.argv[1].split(','):
    print("apk name:%s" % soft_name)
    with open(soft_name, "rb") as f:
        data = f.read()
        print("%s length = %s" % (soft_name, len(data)))
        print("md5:%s\n" % md5(data))
        print("crc32:%s\n" % CRC32().calculate(data))
        print("CRC16:%s\n" % CRC16().calculate(data))
        print("CRC16DNP:%s\n" % CRC16DNP().calculate(data))
        print("CRC16Kermit:%s\n" % CRC16Kermit().calculate(data))
        print("CRC16SICK:%s\n" % CRC16SICK().calculate(data))
        print("CRCCCITT:%s\n" % CRCCCITT().calculate(data))
input()
