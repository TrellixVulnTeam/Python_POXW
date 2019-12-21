"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : zip_read.py
 @Time    : 2019/4/1 17:29
"""
import zipfile

i = 0 ^ 1
j = 1 ^ 2

dict_a = {1: 2}
print(dict_a.get(None, "nod"))

f = zipfile.ZipFile("./test.zip")
name_info = f.NameToInfo
# file_info = f.getinfo("libmupdf.so2")
# print("\n".join(f.filelist))
pass
