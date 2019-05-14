"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Bigfile.py
 @Time    : 2019/5/13 10:51
"""
import os

file_list = sorted([f for f in os.listdir("./") if f.startswith("Xiaomi")])
with open("xiami.zip", "wb") as f_big:
    for f in file_list:
        with open(f, "rb") as f_small:
            f_big.write(f_small.read())
