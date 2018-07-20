#!/usr/bin/env python
# encoding: utf-8
"""
@author: ShangChenHui
@file: WifiLZ_Encipher.py
@time: 17-9-6 下午3:22
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import logging
import traceback
import random
import string
import os

BLOCK_SIZE = 16


def AES_ENCRYPT(plain_text, keyWord, mode=AES.MODE_ECB, blockSize = BLOCK_SIZE):
    """
    AES ECB模式 ZeroPadding 加密，块大小为32byte
    :param plain_text: 加密的字符串
    :param keyWord: 加密密钥
    :param mode: AES模式，默认ECB模式
    :param blockSize: 最小块大小
    :return: 成功返回加密后的hex字符串，失败返回None
    """
    if not isinstance(keyWord, bytes):
        keyWord = keyWord.encode()

    if not isinstance(plain_text, bytes):
        plain_text = plain_text.encode()

    if len(keyWord) != blockSize:
        logging.error("\nAES加密参数错误：%s" % traceback.format_exc())
        return None

    cryptor = AES.new(keyWord, mode)
    plain_text += (blockSize - len(plain_text) % blockSize) * b'\n'
    cipher_text = cryptor.encrypt(plain_text)
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(cipher_text)


def AES_DECRYPT(cipher_text, keyWord, mode=AES.MODE_ECB, blockSize=BLOCK_SIZE):
    """
    AES ECB模式 解密，块大小为32byte
    :param cipher_text: 解密的hex字符串
    :param keyWord: 解密密钥
    :param mode: AES模式，默认ECB模式
    :param blockSize: 最小块大小
    :return: 成功返回解密后的字符串，失败返回None
    """
    if not isinstance(keyWord, bytes):
        keyWord = keyWord.encode()

    if not isinstance(cipher_text, bytes):
        cipher_text = cipher_text.encode()

    if len(keyWord) != blockSize or len(cipher_text) % blockSize != 0:
        logging.error("AES解密参数错误keyWord:{keyWord}\ncipher_text:{cipher_text}\n error：{error}".format(keyWord=keyWord,
                                                                                                     cipher_text=cipher_text,
                                                                                                     error=traceback.format_exc()))
        return None

    cryptor = AES.new(keyWord, mode)
    plain_text = cryptor.decrypt(cipher_text)

    return plain_text.rstrip(b'\n')


def md5(plaintext):
    """
    md5加密
    :param plaintext: 加密的字符串
    :return: 加密后的结果
    """
    m = hashlib.md5()
    if not isinstance(plaintext, bytes):
        plaintext = plaintext.encode()
    m.update(plaintext)  # 须为bytes
    return m.hexdigest()


def FileMd5(filePath):
    """
    计算文件的md5（文件字符串形式）
    :param filePath: 文件路径
    :return:
    """
    if os.path.isfile(filePath):
        with open(filePath, "rb") as f:
            return md5(f.read())
    else:
        return None


def BinFileMd5(filePath):
    """
    计算文件的md5（文件字符串形式）
    :param filePath: 文件路径
    :return:
    """
    if os.path.isfile(filePath):
        with open(filePath, "rb") as f:
            return md5(f.read())
    else:
        return None


def RandomSrting(num, seed=string.ascii_letters + string.digits + string.punctuation):
    """
    随机字符串生成器，默认种子为：大小写字母、数字、特殊字符
    :param num: 需要生成的字符串长度
    :param seed: 随即字符种子
    :return: 成功返回特定长度的随机字符串，失败返回“”
    """
    if num > 0 and len(seed) > 0:
        return ''.join(random.sample(seed, num))
    return ''


if __name__ == "__main__":
    str = "dajidali jinwan chiji"
    key = md5(md5(str))
    print("KEY:", key)

    plaintext = "100"
    print("Plaintext:", plaintext)

    ciphertext = AES_ENCRYPT(plaintext, key[:16])
    print("Ciphertext:", ciphertext.decode())

    # plaintext = "大吉大利，晚上吃鸡！"
    # print("Plaintext:", plaintext)
    # ciphertext = AES_ENCRYPT(plaintext, key)
    # print("Ciphertext:", ciphertext.decode())
    # decodetext = AES_DECRYPT(ciphertext, key)
    # print("Decodetext:", decodetext.decode('gb2312', 'replace'))
    #
    # WeChat = "866184028560766-458746054"
    # print("WeChat SQL password:", md5(WeChat)[:7])
