"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : RC4.py
 @Time    : 2019/4/1 15:48
"""

from Crypto.Cipher import ARC4


def encrypt(message, key):
    des = ARC4.new(key)
    cipher_text = des.encrypt(message)
    return cipher_text


def decrypt(cipher_text, key):
    des3 = ARC4.new(key)
    message = des3.decrypt(cipher_text)
    return message
