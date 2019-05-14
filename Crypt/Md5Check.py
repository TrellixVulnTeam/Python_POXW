#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Md5Check.py 
@time: 2018/2/1 11:56 
@version: v1.0 
"""
import base64
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

sh1 = "3Pr9cdVmUZIPRTa30Of5mmHqryc="
sh2 = "UJ68IKSwvnPSNiYn/hm0hfIh8eg="

sh3 = "".join(i + j for i, j in zip(sh2, sh1))
print(sh3)
if __name__ == "__main__":
    sys.argv += ["./plaint.txt"]
    for soft_name in sys.argv[1].split(','):
        print("apk name:%s" % soft_name)
        with open(soft_name, "rb") as f:
            data = f.read()
            print("%s length = %s" % (soft_name, len(data)))

            print("=" * 20 + "MD5 check" + "=" * 20)
            print("md5:%s\n" % md5(data))
            print("md5_hash:%s\n" % hex(CRC32().calculate(md5(data))))

            # print("=" * 20 + "CRC check" + "=" * 20)
            # crc32 = CRC32().calculate(data)
            # crc32_hex = hex(CRC32().calculate(data))
            # print("CRC16:%s\n" % CRC16().calculate(data))
            # print("CRC16DNP:%s\n" % CRC16DNP().calculate(data))
            # print("CRC16Kermit:%s\n" % CRC16Kermit().calculate(data))
            # print("CRC16SICK:%s\n" % CRC16SICK().calculate(data))
            # print("CRCCCITT:%s\n" % CRCCCITT().calculate(data))

            print("=" * 20 + "SHA check" + "=" * 20)
            sha1 = hashlib.sha1(data)
            sha1_hexdigest = sha1.hexdigest().encode()
            print("sha1: ", sha1_hexdigest)
            print(base64.encodebytes(sha1_hexdigest))
            print("sha224: ", hashlib.sha224(data).hexdigest())
            print("sha256: ", hashlib.sha256(data).hexdigest())
            print("sha384: ", hashlib.sha384(data).hexdigest())
            print("sha512: ", hashlib.sha512(data).hexdigest())
