#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: AES.py
@time: 2017/9/5 9:48
@version: v1.0
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import logging
import traceback

BLOCK_SIZE = 32


def AES_ECB_ENCRYPT(plain_text, key, mode = AES.MODE_ECB):
    """
    AES ECB模式 ZeroPadding 加密，块大小为32byte
    :param plain_text: 加密的字符串
    :param key: 加密密钥
    :param mode: AES模式，默认ECB模式
    :return: 成功返回加密后的hex字符串，失败返回None
    """
    if len(key) != BLOCK_SIZE:
        logging.error("AES加密参数错误：%s" % traceback.format_exc())
        return None

    cryptor = AES.new(key, mode)
    plain_text += (BLOCK_SIZE - len(plain_text) % BLOCK_SIZE) * '\0'
    cipher_text = cryptor.encrypt(plain_text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(cipher_text)


def AES_ECB_DECRYPT(cipher_text, key, mode = AES.MODE_ECB):
    """
    AES ECB模式 解密，块大小为32byte
    :param cipher_text: 解密的hex字符串
    :param key: 解密密钥
    :param mode: AES模式，默认ECB模式
    :return: 成功返回解密后的字符串，失败返回None
    """
    if len(key) != BLOCK_SIZE \
            or len(cipher_text) % BLOCK_SIZE != 0:
        logging.error("AES解密参数错误：%s" % traceback.format_exc())
        return None

    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(cipher_text))
    return plain_text.rstrip('\0')


def md5(plaintext):
    """
    md5加密
    :param plaintext: 加密的字符串
    :return: 加密后的结果
    """
    m = hashlib.md5()
    m.update(plaintext)
    return m.hexdigest()


if __name__ == "__main__":
    str = "dajidali jinwan chiji"
    key = md5(md5(str))
    print "KEY:" + key
    plaintext = "第九阿佛教"
    print "Plaintext:" + plaintext
    ciphertext = AES_ECB_ENCRYPT(plaintext, key)
    print "Ciphertext:" + ciphertext
    decodetext = AES_ECB_DECRYPT(ciphertext, key)
    print "Decodetext:" + decodetext
