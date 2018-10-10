"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : WifiKeyCompress.py
 @Time    : 2018/9/29 16:59
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

# AES_KEY = b"!I50#LSSciCx&q6E"
# AES_IV = b"$t%s%12#2b474pXF"

# AES_KEY = b"FciCx&q6E!I50#LSSC"
# AES_IV = b"C474pXF$t%s%12#2bB"

AES_KEY = b"6E!I50#LSSciCx&q"
AES_IV = b"XF$t%s%12#2b474p"

plainText = b"705ADF23041F33EEB2991F7DD3A02E61855C022EB69858881A4088FD47645F7C"
plaintext_len = len(plainText)
srcBytes = a2b_hex(plainText)
srcBytesLen = len(srcBytes)

cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
encodeBytes = cipher.decrypt(srcBytes)
print(encodeBytes)

dstBytes = b"009apple78991538104786684"
dstBytesLen = len(dstBytes)
dstBytes += (16 - dstBytesLen % 16) * b'\0'
dstBytesLen = len(dstBytes)

cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
# offset = int(len(srcBytes)/2)
encodeBytes = b2a_hex(cipher.encrypt(dstBytes))
# selfBytes = cipher.decrypt(encodeBytes)

print({a: plainText.count(a) for a in set(plainText.replace(b' ', b''))})
# print(srcBytes)
# print(dstBytes)
print({a: encodeBytes.upper().count(a) for a in set(encodeBytes.upper().replace(b' ', b''))})

# print(selfBytes)

# if selfBytes == dstBytes:
#     print(True)
# else:
#     print(False)
