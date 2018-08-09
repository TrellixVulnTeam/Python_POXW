"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ReadImpoertMessage.py
 @Time    : 2018/6/29 15:21
"""
import os

# dir_a = "C:\\Users\\xiaohui\\Desktop\\Android远程植入调研（2018-06-25）\\植入测试\\download"
# keyword = b"5b1d21092c8c45"
#
#
# list_a = list()
# for fileinfo in os.walk(dir_a):
#     for file in (os.path.join(fileinfo[0], file) for file in fileinfo[2]):
#         if os.path.isfile(file):
#             with open(file, "rb") as f:
#                 content = f.read()
#                 if keyword in content:
#                     print("keyword find in {targetFile}".format(targetFile=file))
pass

# print(os.cpu_count())
# import time
# from tqdm import tqdm
#
# for i in tqdm(range(1000)):
#     time.sleep(.01)

import sys, time
import multiprocessing

flush = sys.stdout.flush
DELAY = 0.1
DISPLAY = ['|', '/', '-', '\\']


def spinner_func(before='', after=''):
    write, flush = sys.stdout.write, sys.stdout.flush
    pos = -1
    while True:
        pos = (pos + 1) % len(DISPLAY)
        msg = before + DISPLAY[pos] + after
        write(msg)
        flush()
        write('\x08' * len(msg))
        time.sleep(DELAY)


def long_computation():
    # emulate a long computation
    time.sleep(3)


if __name__ == '__main__':
    with open("WeChat.html", "rb") as fRead, open("Tmp.html", "w") as fWrite:
        fWrite.write(fRead.read().decode(encoding="utf-8"))

    import struct

    hearder = struct.pack(">I", 1024 + 16)
    print(hearder)

    i = b'\\u6d59\\u6c5f\\u7701'.decode("unicode_escape")
    print(i)
    import xmltodict
    import dicttoxml

    with open("Config2.xml", "r", encoding="utf-8") as f1:
        config_dict = xmltodict.parse(f1.read())

    print(config_dict)

    with open("Config3.xml", "w") as f2:
        f2.write(xmltodict.unparse(config_dict, pretty=True))
    cipher = 225
    D = 29
    N = 323

    plaintxt = cipher ** 10 % N

    h = int(
        "E161DA03D0B6AAD21F9A4FB27C32A3208AF25A707BB0E8ECE79506FBBAF97519D9794B7E1B44D2C6F2588495C4E040303B4C915F172DD558A49552762CB28AB309C08152A8C55A4DFC6EA80D1F4D860190A8EE251DF8DECB9B083674D56CD956FF652C3C724B9F02BE5C7CBC63FC0124AA260D889A73E91292B6A02121D25AAA7C1A87752575C181FFB25A6282725B0C38A2AD57676E0884FE20CF56256E14529BC7E82CD1F4A1155984512BD273D68F769AF46E1B0E3053816D39EB1F0588384F2F4B286E5CFAFB4D0435BDF7D3AA8D3E0C45716EAD190FDC66884B275BA08D8ED94B1F84E7729C25BD014E7FA3A23123E10D3A93B4154452DDB9EE5F8DAB67",
        16)
    print(h)

    spinner = multiprocessing.Process(None, spinner_func, args=('Please wait ... ', ''))
    spinner.start()
    try:
        long_computation()
        print('Computation done')
    finally:
        spinner.terminate()

from threading import Thread

# import asyncio
#
# @asyncio.coroutine
