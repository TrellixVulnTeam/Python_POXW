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

def md5(plaintext, time = 1):
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
        print m.hexdigest()
        m.update(m.hexdigest())
        tmp_time += 1
    return m.hexdigest()


if __name__ == "__main__":
    str = "dajidali jinwan chiji"
    key1 = md5(md5(str))
    print key1
    key2 = md5(str, time = 2)
    print key2
    print key1 == key2
    print "KEY:" + key1
    plaintext = "第九阿佛教"
    print "Plaintext:" + plaintext
    # ciphertext = AES_ECB_ENCRYPT(plaintext, key)
    key1 = "bc0ef838ed0acd1a31ce55b043a1c14c"
    ciphertext = "55c781e86644e99aed984ad12a53a0a2fcc7b4bea42f2a7ee0cd384ba6e33d41df1d1034645130984d199243cc4e9643cea2be30c07a4c851b7092a02c8c98526d4dde88e7c73832dd7348771700530207937d5b986864c7ca56b4cfaff6e78a427e3841a660bca306c22f267033d2f2f659fa01529d329e3287a1999a104b17229bc22476d1dd8fb609f804fcec489504207c2119d0730223851ae7a3fb34ad6b4b942573892c96b64b2372be552fc91eccea5fba818f6cdc1990c7f3f1eac0b364651413be0159eb741d465ad00e23fd9c1e1f6e5482f7930c4145a96f295e "
    print "Ciphertext:" + ciphertext
    decodetext = AES_ECB_DECRYPT(ciphertext, key1).decode("unicode-escape")
    print "Decodetext:" + decodetext

