"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : tbslog_get_password.py
 @Time    : 2019/4/1 15:15
"""
import RC4
import os

key_of_mkey = b"tbslog.txt"
len_of_mkey = 16
log_decode_file = "tbs.log"

log_data_list = list()

with open("tbslog.txt", "rb") as tbslog:
    log_data = b""
    mkey = b""

    for line in tbslog.readlines():
        line = line.strip()
        if not line:
            continue

        flag = line[:len_of_mkey][:3]
        if flag != b"013":
            log_data += line
            continue
        else:
            log_data_list.append((mkey, log_data))

            log_data = line[len_of_mkey:]
            mkey = RC4.decrypt(line[:len_of_mkey][3:], key_of_mkey)
            if len(mkey) != 13:
                mkey = b""
                continue
    if mkey and log_data:
        log_data_list.append((mkey, log_data))

    for key, value in log_data_list:
        if not key or not value:
            continue
        log = RC4.decrypt(value, key)
        pass

    log_list = [RC4.decrypt(value, key) for key, value in log_data_list if key and value]
    # log_list = [b"[" + str(line_num).encode() + b"] " + RC4.decrypt(value, key) for key, value in log_data_list]

with open(log_decode_file, "wb") as logfile:
    logfile.write(b"\n".join(log_list))
