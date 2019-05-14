"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ConvertAscii.py
 @Time    : 2019/4/30 14:50
"""
import time
import json

file_list = list()
file_list.append("CallLog")
file_list.append("SmsLog")
file_list.append("Photos")

print(time.time())
for file in file_list:
    with open(file, "rb") as f:
        json_data = json.loads(f.read())

    for i in range(0, len(json_data), 1000):
        new_data = json_data[i:i + 1000]
        with open(file + "_{start}_{end}".format(start=i, end=i + len(new_data)), "wb") as f:
            f.write(json.dumps(new_data, ensure_ascii=False, indent=4).encode())
