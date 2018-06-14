#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: GzipDemo.py 
@time: 2018/2/6 18:17 
@version: v1.0 
"""
import gzip

petso = b"""HTTP/1.1 200 OK\r
Server: 3Gdown_DK\r
Connection: close\r
Cache-Control: max-age=600\r
Last-Modified: Wed, 13 Dec 2017 12:06:24 GMT\r
Content-Type: application/zip\r
Content-Length: ###contentlen###\r
\r
###content###"""

with open("PetSozip", "wb") as f, open("PetSo_7_3_1.zip", "rb") as f1:
    content = f1.read()
    length = str(len(content)).encode()
    tmp = petso.replace(b"###contentlen###", length)
    tmp = tmp.replace(b"###content###", content)
    f.write(tmp)

    # encode = gzip.compress(content)
    # header = header.replace(b'\n', b'\r\n')
    # f.write(header)
    # f.write(b"\r\n\r\n")
    # f.write(str(hex(len(encode))).encode()[2:])
    # f.write(b"\r\n")
    # f.write(encode)
    # f.write(b"\r\n0\r\n\r\n")
