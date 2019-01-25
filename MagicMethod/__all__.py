"""
@author: Alfons
@contact: alfons_xh@163.com
@file: slots_and_all.py
@time: 19-1-25 下午8:56
@version: v1.0 
"""
from struct import *

p = pack("I2s", 2, b"he")
print(p)

u_p = unpack("I2s", p)
print(u_p)

import struct

p_2 = struct.pack("I2s", 2, b"he")
print(p_2)

u_p_2 = struct.unpack("I2s", p_2)
print(u_p_2)
