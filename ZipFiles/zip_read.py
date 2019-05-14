"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : zip_read.py
 @Time    : 2019/4/1 17:29
"""
import zipfile

f = zipfile.ZipFile("./test.zip")
print("\n".join(f.filelist))
pass