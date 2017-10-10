#!/usr/bin/env python  
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: main.py 
@time: 2017/4/25 11:40 
@version: v1.0 
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

print("hell sa")
i = 4 + 1
print(i)
print("{name} is find {client}".format(name = 'Alfons', client = "dota2"))
print("{0:.3}".format(10.0 / 3))
print("{0:.^13}".format('hello'))
print(not 0)

# NEW LINE,Function Logic()
print("NEW Function----Logic:")
from Function import Logic_Function

Logic_Function.Logic()
print("")

# NEW LINE,Function print_max()
print("NEW Function----print_max:")
from Function import print_max

print_max.print_max(4, 5)
print_max.print_max(5, 4)
print_max.print_max(4, 4)
print("")

# NEW LINE,Function tuple
from Function.Tuple import print_tuple

print(print_tuple(3, 1, 2, 3, alfons = 12, aal = 32))
print print_tuple.__name__
print print_tuple.__doc__
print('')

# NEW LINE,Function DataStruct
from Function import DataStructers

print ("{0:_^64}".format("DataStructers.list_func()"))
DataStructers.list_func()
print ("\n{0:_^64}".format("DataStructers.tuple_func()"))
DataStructers.tuple_func()
print ("\n{0:_^64}".format("DataStructers.dictionary_func()"))
DataStructers.dictionary_func()
print ("\n{0:_^64}".format("DataStructers.seq_function()"))
DataStructers.seq_function()

# NEW LINE,Class iPhone
from iPhone.CiPhone import iPhone_v

print ("\n{0:_^64}".format("class iPhone_v"))
iPhone_3G = iPhone_v("iPhone_3G")
iPhone_3G.say_hi()
iPhone_v.how_many()
print ""

iPhone_4s = iPhone_v("iPhone_4s")
iPhone_4s.say_hi()
iPhone_v.how_many()
print ""

iPhone_3G.recycle()
iPhone_4s.recycle()
iPhone_v.how_many()

# NEW LINE,Class Animal
from Animal.animal import *

print ("\n{0:_^64}".format("class Animal"))
dog = Dog("meat")
cat = Cat("fish")
dog.run()
cat.run()
dog.eat()
cat.eat()

# NEW LINE,File_func
from Function.io import io_using_file

print ("\n{0:_^64}".format("File_func"))
io_using_file.file_w_r()
print ""

# NEW LINE,Produce List
print ("{0:_^64}".format("列表生成式"))
list_a = [x * x for x in range(1, 11)]
print list_a
list_a = [x * x for x in range(1, 11) if x % 2 == 0]
print list_a
n_list = ['X', 4, 'Y', 'Z']
print ("\n{0:_^64}".format("通过[for...in...for...in...]完成"))
list_a = [m + n.lower() for m in "ABC" for n in n_list if isinstance(n, str)]
print list_a

import os

print [d for d in os.listdir("..")]


# NEW LINE,generator 生成器
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1


print [i for i in fib(10)]

# NEW LINE,map()/reduce()
print ("\n{0:_^64}".format("map()/reduce()"))


# map(f,[x1, x2, x3, x4])) = [f(x1),f(x2),f(x3),f(x4)] // map()的f()只能接受一个参数
def func_map(name):
    if not isinstance(name, str):
        return ""
    return name.capitalize()


print map(func_map, [43, 'LISA', 'barT'])


# reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4) // reduce()的f()需要两个参数
def func_mul(x, y):
    return x * y


print reduce(func_mul, [1, 2, 3, 4, 5, 6])

# NEW LINE,filter()
print ("\n{0:_^64}".format("filter()"))


# filter(f, [x1, x2, x3, x4])  // filter()的f()只能接收1个参数
def judge_prime(n):
    if n == 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True


print filter(judge_prime, range(100, 1000))

# NEW LINE,sorted()
print ("\n{0:_^64}".format("sorted()"))
print sorted([34, 23, 4, 2, 1, 65, 77])[::-1]


def com_string(str1, str2):
    str1 = str1.upper()
    str2 = str2.upper()
    if str1 < str2:
        return -1
    elif str1 > str2:
        return 1
    else:
        return 0


print sorted(['bob', 'about', 'Zoo', 'Credit'], com_string)

# NEW LINE,lambda
print ("\n{0:_^64}".format("lambda"))
# 求阶乘
print reduce(lambda x, y: x * y, range(1, 6))
print sorted(map(lambda name: name.capitalize(), ["sdsdfs", 'LISA', 'barT']))[::-1]

str_zfill_test = "hds"
print "dsfsdfdsfsdds".zfill(200)
print "sds".zfill(200)

from collections import namedtuple

cricle = namedtuple('cricle', ['x', 'y', 'r'])
cricleA = cricle(1, 2, 3)
print cricleA

import logging
import traceback


def func1():
    raise Exception("helsd")


try:
    func1()
except:
    logging.error("Error : %s" % traceback.format_exc())
    pass

str_find = "find_first_second_thresa"
sub_str = str_find[str_find.find("qqq") + len("qqq"):]

print "begin"
import time
import datetime

time_now = datetime.datetime.now()
# time_str = time.mktime(time_now.strptime)
time_str = time.mktime(time_now.utctimetuple())

time_i = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time_str)))
print time_i

str_tmp = "1|2|3|4"
str_tmp_2 = "1"
st_list_1 = []
st_list_2 = str_tmp_2.split('|')

st_list_1.extend(st_list_2)

# path = r"C:\Users\shangchenhui\Downloads\2007-02-06-xyq\2007-02-06-xyq\Files\xyq"
# filelist = os.listdir(path)
# for file in filelist:
#     if 'Fixed' in file:
#         continue
#     os.rename(path + '/' + file,path + '/' + file + '.gif')

list_s = ["23", "32", "1", "6"]
list_s.append("4")

time_s = time.mktime(time.localtime())
time_s = time.time()
print type(time_s)
print time_s

print type(time_s)

for i in range(1):
    print i

results_row = 2 ** 15
sheet_num = results_row / 65535 + 1 if results_row % 65535 else 0

tuple

import socket
import struct

ip_4 = struct.unpack("=I", socket.inet_aton("192.168.2.1"))
print ip_4

dict_s = {"channel": "2",
          "count": "4",
          "aps": [
              {
                  "ssid": "ssssssssssssssssflasjfladsjlkfjl",
                  "opn": "wpa",
                  "password": "12345678"
              },
              {
                  "ssid": "mulwifi2",
                  "opn": "wpa",
                  "password": "12345678"
              }
          ]}
aps = dict_s.get("aps")
print len(aps)

time_s = datetime.datetime.now()
print time_s

ap_mac = "dd:ac:3d:c5:aa:9a"
ap_mac = "02" + ap_mac[2:16] + "0"

config = (
             'interface=%s\n'
             'driver=nl80211\n'
             'ssid=%s\n'
             'hw_mode=g\n'
             'channel=%s\n'
             'macaddr_acl=0\n'
             'ignore_broadcast_ssid=0\n'
         ) % ("sdfa", "asdfa", "ss")
print config

# keyperson_list = ["lgd", "eg", "vg"]
keyperson_list = []
keyperson_str = ','.join(keyperson_list)

u_type = type(u"fdsaf")
print u_type

list_a = []
list_a.append("sa")
list_a.append("sa")
print list_a

str_a = "sd:cd:12:ed:fa:13"
print str_a.upper()

str_1 = ["1", "2", "3"]
str_2 = ["fds", "21"]
str_2 += ["fassss", "gfd"]
print str_2
pass

expiredate = "20092071"
a = expiredate[::2]
b = expiredate[1::2]

hostname = socket.gethostname()
ip_a = socket.gethostbyname(hostname)
ipList = socket.gethostbyname_ex(hostname)
print ip_a
print ipList

import pickle

# with open("txt", "wb") as f:
#     pickle.dump(dict_s, f)

with open("LastAttack.record", "rb") as f2:
    aps__s = pickle.load(f2)
    print aps__s

import random

import string

ran_str = ''.join(random.sample(string.ascii_letters + string.digits+ string.punctuation, 24))

print ran_str

if -1 == True:
    print "2 is Tru"
pass

ap_info = {}
ap_info.update({"ssid": 1, "protect":2, "password": 3})
pass

with open("text.txt","a") as f:
    f.write("dafas")

import xml.dom.minidom

dom = xml.dom.minidom.parse("./FeedbackConfig.xml")
root = dom.documentElement
try:
    root.removeChild(root.getElementsByTagName('FeedbackDeviceStatus')[0])
    root.removeChild(root.getElementsByTagName('FeedbackDB')[0])
except:
    print "nothing"

docCreater = xml.dom.minidom.Document()
root.appendChild(docCreater.createTextNode("\t"))
version = docCreater.createElement("Version")
version.appendChild(docCreater.createTextNode("32.2"))
root.appendChild(version)
root.appendChild(docCreater.createComment("设备版本信息"))
root.appendChild(docCreater.createTextNode("\n\t"))
expireDate = docCreater.createElement("ExpireDate")
expireDate.appendChild(docCreater.createTextNode("32.2"))
root.appendChild(expireDate)
root.appendChild(docCreater.createComment("设备过期日期"))
root.appendChild(docCreater.createTextNode("\n"))

with open("./FeedbackConfig.xml", "w") as f:
    dom.writexml(f, encoding = "utf-8")
pass


def getip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('www.baidu.com', 0))
        sock_name = s.getsockname()
        ip = sock_name[0]
    except:
        ip = "x.x.x.x"
    finally:
        s.close()
    return ip

ip = getip()
if not "":
    print "heolo"
pass