"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : AndroidAesDecode.py
 @Time    : 2018/6/28 20:14
"""
from Crypto.Cipher import AES
from Crypt import Encipher

v_length = 16
with open("./1", "rb") as f:
    content = f.read()
    keys = content[-v_length:]
    print("keys:", len(keys))
    cipherText = content[:-v_length]
    print("cipherText:", len(cipherText))
    plaintText = Encipher.AES_DECRYPT(cipherText, keys, AES.MODE_CBC, v_length)
    print(plaintText)
    with open("plaint.txt", "wb") as f2:
        f2.write(plaintText)
    pass
