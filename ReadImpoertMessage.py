"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ReadImpoertMessage.py
 @Time    : 2018/6/29 15:21
"""
from Crypt import Md5Check, AES
import json
import os

import traceback
from queue import Queue
import binascii

with open("C:\\Users\\xiaohui\\Desktop\\working\\lantern_分析(2018-10-08)\\Fabric\\.lantern\\proxies.yaml", "rb") as f:
    content = f.read()

hexList = [hex(char)[1:] for char in content]
hexstr = "\\".join(hexList)

with open("text.txt", "w") as f:
    f.write(hexstr)

qu = Queue(maxsize=3)
qu.put(1)
qu.put(2)
qu.put(3)
print(qu.full())
try:
    qu.put(4, False)
    qu.put(5)
except:
    traceback.print_exc()

name = dict(name="hell")
print("hello {name}".format(name=name))

defaultRuleList = [
    "-1 1 -2 345789 ?1?2?d?d?d?d?d?d?d?d?d",
    "?l?l?l?d?d?d?d?d?d",
    "?l?l?d?d?d?d?d?d"
]


def GetDefaultRules():
    file = "rules"
    otherRules = list()
    if os.path.isfile(file):
        with open(file, "r") as f:
            otherRules = f.read().splitlines()

    otherRules = [rule for rule in otherRules if rule and rule.count("?") >= 8]

    for rule in defaultRuleList:
        if rule in otherRules or not rule:
            continue
        otherRules.append(rule)
    return otherRules


rules = GetDefaultRules()

wifi_name = b"Wifi_111"

password = Md5Check.md5(wifi_name)[::2]
print(password)

app_id = "2882303761517147566"
app_key = "5481714735566"
device_id = "B73ACC1AD5DEE474D38738668C319D8E0D8DB160"
seed = "seed:{}-{}-{}".format(app_id, app_key, device_id)

AES_key = Md5Check.md5(seed.encode()).upper()[0:16].encode()
print("AES_key:", AES_key)

cipher_text = "db52ad58e8d5d682e868fa58a0bba0ed8dc790a1c99aa05f402ed86fa136905c3db90aba041c8f4a29fa3485bef4dcb896df5a042c5d5fd7e463c9adca8cc35c771caec299ef8fc2ae929eb9fffd42ec00659996aea5a596c12c9efcfe1c898cc31aaf274eb61f074ee14fed7404a3c4fac6cae257fdbfa58c68b254b1cef17d525eac558c7e0a9a213b92e31f00be014e47d8ab5900bd10c7bc33ebf3eb95d7c96c60e37ced341849a65d084b483f5efeba4797aecb831416bace2a7a905b127d16d11bf5e89bffda789d25a9e8f0e7b6037bff6f4d6db7338b092e6463d84f76cd6996923de487dbda5b3ff14794ea5a1a68dca3031b7083246f3357b4406c71308dc3c83ac15a7d5545c0618aa8af791277d43ee9ba25c14217766e04db29f5496e813d70f3cbb3652ba79c159aef55b8e70b9e4e76e49044ace23b4a5fa7844f684b0d75cb93699915f38b73d361649de8a5fa5fdf8f503fbe35770b84bf3e3492b855d2cfa403dfe0d5a47cd0a3c31aaf274eb61f074ee14fed7404a3c4c0372705b458675253deac181db6bc2d3bc88dfd462b4c4285ec386ee4365b4688db324c61acc7bd4722ff18d5b8202a0c9b35ed8b5923cba2b461dab24dad39a90281acd3d58723af34ac3b6ff46556eaaaf75090fc5d23597f18d67afda7b905a00bc8bf899ba1132f39f0a72e5938a807448ec892b86403848dbe4dc7531794de4c5ec8bdcba651818a227a89be1e8f7695b82d60133f1e522162ffef71fc8c81008af7c56f135c530c884f78035a43849953ecd539492d8ba07253796dd77fe29fdcd7afa9e196de9250bbdaaaa82f7401c23bfb861419eca2989004e9212cd79ed017a7d13b00f45adc78fbb7a91ef3e9be4c472259c82aee161f7d4a55a91f2315e7b144795fb6a716ee56f028c588c8f29493155dc2423e96e548ef77c31aaf274eb61f074ee14fed7404a3c41bb29f91ec68b7f6f45e5060b241af3697cd7e2a9c863524b244d111cd1ca95a1819108efc9ffb086c3fe35db9fbeceb46055cceeb9147f62484f6edfeca4333a6e6062285686f0c9c2add8f3a813b0230c9eacfe9a9016eba2b1d0c3568a68e464c0a9b2e73be8b253955e4366c34e22ebd57df46383a97edc8e10fd2d2daa9f8b797144ea2dd7d910526efc9a5401a61097d90e1eded382b2d698e1fd3095c275820460c1f9b58a7a8e224b8014fb7853ee93841332b0b1c7d696b8d68c49fb6fd7498f51fed4cae9426cd3c53b944dceacf108c39aa220d13367a8d39e84f12ba8e1064fffa11035ad044e1dcd392e27fc3bc83f491f14bd375e64d62d8a61874ea9730f6134d3e6079e06ac3103a94de4c5ec8bdcba651818a227a89be1ecdec42d957733e636f4a6be05a81a0fd6f6030f4c1049f7d28faa76b1075c57132f8ab60da38d64d63016d990823b35319e76d7b1d22fb57709db4f58413355a6f38a0c90bf94f0380d360b9d3a448cf571bd65c8cd757503c7abf1ae89b7e2af7720b3f98def6477fbd2b6a9dbe2c8bae194285c2a9956af8ceb0bc2e4fba3f5bb8dd8114029297c7176578760e4241683d17c6717167370e118db950f2c852b9d486c9d6defeac28750cf87addd9d9d4df131efa8ca04affbe9a82997ead9877b1eb1e2a6d0e2ad50b0c722d7f8f0103f5975f450b5b2e74696c659d96e20bc42477c60a4fbafac9fbd5a0e1434016ae9c37ef0c52020b4cf75a5764f450f28602089a1a87d5be1d8135bf1e9ef9c1af8e38b6e4997ee619ff066ffae4ea1a13b4db7459ee681e411625a8b35709ca8e6a0ac2a18bb3920a966c5a6c1653b41ef3b553a37cc137de9c19d4257313c94f2dfc6c064618c68ff5d117431235bbc6a963ee334c50c5cda4ee39192d16fb0364a1058eda8b32329b09b71ea4357e0377222290590cd6d42f3c3829d7ace6fe7ace9d37cde02227eade69fe9d4f0d2ca9f6e99b125662072e2b54f36cad9f1bc4f580d1c32b7a2cd82d5166fd02aa218d52b0cd94108be87c24f3f8b12b32"

cipher_text2 = AES.AES_ECB_ENCRYPT("package_name".encode(), AES_key)
print(cipher_text2)

plain_text = AES.AES_ECB_DECRYPT(cipher_text=cipher_text.encode(), key=AES_key)
# plain_text = AES.AES_ECB_DECRYPT(cipher_text=cipher_text2, key=AES_key)
# plain_text_json = json.loads(plain_text)
print(plain_text)
pass


def func(data=[]):
    datatmp = list(data)
    datatmp.append(0)
    return datatmp


print(func())
print(func([1]))
print(func())
print(func([1]))
print(func())

pass
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


# if __name__ == '__main__':
# with open("WeChat.html", "rb") as fRead, open("Tmp.html", "w") as fWrite:
#     fWrite.write(fRead.read().decode(encoding="utf-8"))
#
# import struct
#
# hearder = struct.pack(">I", 1024 + 16)
# print(hearder)
#
# i = b'\\u6d59\\u6c5f\\u7701'.decode("unicode_escape")
# print(i)
# import xmltodict
# import dicttoxml
#
# with open("Config2.xml", "r", encoding="utf-8") as f1:
#     config_dict = xmltodict.parse(f1.read())
#
# print(config_dict)
#
# with open("Config3.xml", "w") as f2:
#     f2.write(xmltodict.unparse(config_dict, pretty=True))
# cipher = 225
# D = 29
# N = 323
#
# plaintxt = cipher ** 10 % N
#
# h = int(
#     "E161DA03D0B6AAD21F9A4FB27C32A3208AF25A707BB0E8ECE79506FBBAF97519D9794B7E1B44D2C6F2588495C4E040303B4C915F172DD558A49552762CB28AB309C08152A8C55A4DFC6EA80D1F4D860190A8EE251DF8DECB9B083674D56CD956FF652C3C724B9F02BE5C7CBC63FC0124AA260D889A73E91292B6A02121D25AAA7C1A87752575C181FFB25A6282725B0C38A2AD57676E0884FE20CF56256E14529BC7E82CD1F4A1155984512BD273D68F769AF46E1B0E3053816D39EB1F0588384F2F4B286E5CFAFB4D0435BDF7D3AA8D3E0C45716EAD190FDC66884B275BA08D8ED94B1F84E7729C25BD014E7FA3A23123E10D3A93B4154452DDB9EE5F8DAB67",
#     16)
# print(h)
#
# spinner = multiprocessing.Process(None, spinner_func, args=('Please wait ... ', ''))
# spinner.start()
# try:
#     long_computation()
#     print('Computation done')
# finally:
#     spinner.terminate()

s_1 = [1, 2, 3, 4]
s_2 = [5, 6, 7]

s_1[len(s_1):len(s_1)] = s_2
print(s_1)

d_1 = {'apple': 1, 'egg': 2}
print(2 in d_1)
