#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: AES.py 
@time: 2017/9/5 9:48 
@version: v1.0 
"""
import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

AES_SECRET_KEY = 'f1$s(m@q^9*r%#y-iz=l!k$vu%7@vc7+'
IV = 16 * '\x00'


class AES_ENCRYPT(object):
    def __init__(self):
        self.key = AES_SECRET_KEY
        self.mode = AES.MODE_CBC

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encrypt(self, text):
        # cryptor = AES.new(self.key, self.mode, self.key)
        cryptor = AES.new(self.key, self.mode, IV = IV)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)
        add = length - (count % length)
        text = text + ('\0' * add)
        print len(text)
        self.ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(self.ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        # cryptor = AES.new(self.key, self.mode, self.key)
        print len(AES_SECRET_KEY)
        cryptor = AES.new(self.key, self.mode, IV = IV)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')


if __name__ == '__main__':
    aes_encrypt = AES_ENCRYPT()  # 初始化密钥
    customer_id = "7fd76d1e-3e72-3e12-a1f8-8f666be7e3a6"
    e = aes_encrypt.encrypt(customer_id)
    d = aes_encrypt.decrypt(e)
    print customer_id
    print e
    print d
    a_new = "69201690a6e184e4e2d0cd0781c895efed612135e40a9ea016acee4087fc06af7088d60d5d97589e82432f3bb54caae0"
    print aes_encrypt.decrypt(a_new)