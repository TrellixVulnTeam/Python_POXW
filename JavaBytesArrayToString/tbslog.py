"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : tbslog_get_password.py
 @Time    : 2019/4/1 15:15
"""
import RC4
import time

pass_en = "30 31 33 17 42 22 cb 9d 8b 5e 7a fa 50 22 55 4e  "

mkey_en = bytes.fromhex("".join(pass_en.split(" ")[3:]))
mkey = RC4.decrypt(mkey_en, b"tbslog.txt")
# time_now = time.time()
# tmp = RC4.encrypt(str(int(time_now * 1000)).encode(), b"tbslog.txt")
# print(len(tmp))
pass
