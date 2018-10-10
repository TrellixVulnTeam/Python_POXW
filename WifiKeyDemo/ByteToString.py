"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ByteToString.py
 @Time    : 2018/9/28 16:54
"""

with open("./retCode", "rb") as f:
    oriByteArray = bytes([int(c) % 256 for c in f.read().splitlines()])

with open("./retCode", "wb") as f:
    f.write(oriByteArray)

print(oriByteArray)
pass
