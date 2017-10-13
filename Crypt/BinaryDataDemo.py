#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii,struct,ctypes

# 示例如何使用pack, unpack, calcsize, pack_into, unpack_from函数
def TestPackFunctions():
    format = '!H4si'            # 其中!放在第一个字符，表示不作对齐，并使用网络字节序
    format_loose = '! H 4s i'   # 当然format可以在中间添加空格，也可以不添加
    data = struct.pack(format, 10, "abc", 30)
    data_loose = struct.pack(format_loose, 10, "abc", 30)
    my_tuple = (10, 'abc', 30)
    data_tuple = struct.pack(format, *my_tuple) # 如果使用tuple为pack的参数，需要加 * 号。
    # 接下来看pack_into
    format2 = '!i6sH'
    prebuf = ctypes.create_string_buffer(struct.calcsize(format) + struct.calcsize(format2))
    struct.pack_into(format, prebuf, 0, *my_tuple)
    struct.pack_into(format2, prebuf, struct.calcsize(format), *my_tuple);
    # 可以发现两种format都得到一样的结果，使用tuple时也是一样的结果
    print 'struct format:', format,',size:', struct.calcsize(format), ",data:", my_tuple
    print 'pack normal data:', binascii.hexlify(data)
    print 'pack loose  data:', binascii.hexlify(data_loose)
    print 'pack tuple  data:', binascii.hexlify(data_tuple)
    print 'pack into prebuf:', binascii.hexlify(prebuf)
    # unpack 和 unpack_from
    a, b, c = struct.unpack(format, data)
    print "three variable unpack from data:", a, b, c
    unpacked_data = struct.unpack(format, data)
    print 'unpack from data:', unpacked_data
    unpacked_data = struct.unpack_from(format, prebuf)
    print 'unpack first three from prebuf:', unpacked_data
    unpacked_data = struct.unpack_from(format2, prebuf, struct.calcsize(format))
    print 'unpack second three from prebuf:', unpacked_data

# Struct类也提供普通的四pack、unpack个方法，而格式化字符串放到了对象构造时传入，不用在函数中传入。
# 注意的是，普通的calcsize函数在类中被简化为size成员。
def TestPackClass():
    fmt = struct.Struct('!H4si')
    fmt2 = struct.Struct('!i6sH')
    my_tuple = (10, 'abc', 30)
    data = fmt.pack(*my_tuple)
    prebuf = ctypes.create_string_buffer(fmt.size + fmt2.size)
    fmt.pack_into(prebuf, 0, *my_tuple)
    fmt2.pack_into(prebuf, fmt.size, *my_tuple)
    print 'pack       data:', binascii.hexlify(data)
    print 'pack int prebuf:', binascii.hexlify(prebuf)
    unpacked_data = fmt.unpack(data)
    print 'unpack from data:', unpacked_data
    unpacked_data = fmt.unpack_from(prebuf, 0);
    print 'unpack first three from prebuf:', unpacked_data
    unpacked_data = fmt2.unpack_from(prebuf, fmt.size)
    print 'unpack second three from prebuf:', unpacked_data

def unPackBinary():
    proto_hdr = struct.Struct('< I c I H H c c')
    data_hdr = struct.Struct('< H H')
    data = binascii.unhexlify("5700000003000000002800910b220018005000343630303131383537363136393231000000000018005100383632303936303331333632323230000000000018005d0045522062617272696e6700000000000000000000")
    hdr = data[0:15]
    obj = proto_hdr.unpack(hdr)
    print ord(obj[5])
    obj2 = data_hdr.unpack(data[15:19])
    print obj2[0], obj2[1]
    print data[19:39], len(str(data[19:39]))
    strimsi = ""
    for i in range(19, 39):
        if ord(data[i]) != 0x00:
            strimsi = strimsi + data[i]
        else:
            break
    print len(strimsi), strimsi


if __name__ == '__main__':
    unPackBinary()