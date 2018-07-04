"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : AndroidAesDecode.py
 @Time    : 2018/6/28 20:14
"""
from Crypto.Cipher import AES
from Crypt import Encipher

with open("./AES", "rb") as f:
    content = f.read()
    keys = content[:16]
    print("keys:", len(keys))
    cipherText = content[16:]
    print("cipherText:", len(cipherText))
    plaintText = Encipher.AES_DECRYPT(cipherText, keys, AES.MODE_CBC, 16)
    print(plaintText)
    with open("plaint.txt", "wb") as f2:
        f2.write(plaintText)
    pass
