#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Deflate.py 
@time: 2018/1/25 16:04 
@version: v1.0 
"""
# from gzip import GzipFile
# from StringIO import StringIO
import os
import zlib


# def loadData(url):
#     request = urllib2.Request(url)
#     request.add_header('Accept-encoding', 'gzip,deflate')
#     response = urllib2.urlopen(request)
#     content = response.read()
#     encoding = response.info().get('Content-Encoding')
#     if encoding == 'gzip':
#         content = gzip(content)
#     elif encoding == 'deflate':
#         content = deflate(content)
#     return content

# def gzip(data):
#     buf = StringIO(data)
#     f = GzipFile(fileobj=buf)
#     return f.read()

def DeflateDecompress(data):
    try:
        return zlib.decompress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.decompress(data)


def DeflateCompress(data):
    try:
        return zlib.compress(data, -zlib.MAX_WBITS)
    except zlib.error:
        return zlib.compress(data)


def main():
    # zipFileName = [zipFile for zipFile in os.listdir("./") if zipFile.endswith(".zip")][-1]
    oriName = "WeChat_Dns"
    # with open(zipFileName, "rb") as f, open(zipFileName[:-4], "wb") as f2:
    #     f2.write(DeflateDecompress(f.read()))

    with open(oriName + ".xml", "rb")as f1, open(oriName, "wb") as f2:
        f2.write(DeflateCompress(f1.read())[2:-4])


if __name__ == '__main__':
    main()
