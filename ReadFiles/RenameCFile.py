#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: RenameCFile.py 
@time: 2017/10/18 11:01 
@version: v1.0 
"""
import os

for rt, dirs, files in os.walk("""D://svn//Wifi//trunk//Codes//Xplico"""):
    # 修改.c 后缀为.cpp
    for file in files:
        # pre = file[-2:]
        if file[-2:] == ".c":
            file_path = rt + "/" + file
            os.rename(file_path, file_path + "pp")

    # 修改.h 文件扩展为c++
    for file in files:
        # pre = file[-2:]
        if file[-2:] == ".h":
            file_path = rt + "/" + file
            text_line = []
            with open(file_path, "r") as f:
                text_line = f.readlines()

                for i in range(len(text_line)):
                    line = text_line[i]
                    if "#ifndef" in line:
                        next_line = text_line[i + 1]
                        if "#define" in next_line:
                            text_line.insert(i + 2, '\n#ifdef __cplusplus\n')
                            text_line.insert(i + 3, 'extern "C"\n')
                            text_line.insert(i + 4, '{\n')
                            text_line.insert(i + 5, '#endif\n')
                            break

                for i in range(len(text_line))[::-1]:
                    line = text_line[i]
                    if "#endif" in line:
                        text_line.insert(i, "#endif\n")
                        text_line.insert(i, "}\n")
                        text_line.insert(i, "\n#ifdef __cplusplus\n")
                        break
            str = ""
            for line in text_line:
                str += line
            with open(file_path, "w") as f:
                f.write(str)
    print(rt, dirs, files)

pass
