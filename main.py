#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
import sys
print(sys.version)
print(sys.version_info)
from  enum import Enum


class ProductTypeEnum(str, Enum):
    QDATA_STANDARD = "qdata_standard"
    QDATA_SANFREE = "qdata_sanfree"
    QDATA_LONGHUAL = "qdata_longhual"
    DM_SANFREE = "dm_sanfree"
print(list(ProductTypeEnum))
a= ProductTypeEnum("dm_sanfree")
print(a)

def base_convert(num, base):
    """把十进制数字转成其他进制

    注意: base 需要  2<= `base` <= 36
    当进制数base为1时,没有1进制数,而且程序会陷入无限递归循环

    :param num: int 十进制数字
    :param base: int 要转换的进制数

    :rtype str
    :return 转换之后的进制数

    :raise FuncParamError 参数错误
    """

    def base_convert_(num_, base_):
        # 对于十进制数 0 , 它的任何进制都会是 0
        if num_ == 0:
            return "0"
        # 递归计算 `base` 进制数
        return base_convert_(num_ // base_, base_).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num_ % base_]

    # 检查参数
    return base_convert_(num, base)

print(base_convert(num=4496620, base=32).upper())

def nvme_slot(pcie_bus_address: str, ctrl_id: int, namespace_id: int):
    # print(f"{pcie_bus_address=} {ctrl_id=} {namespace_id=}")
    domain = pcie_bus_address[:pcie_bus_address.find(':')]
    bus = pcie_bus_address[pcie_bus_address.find(':') + 1:pcie_bus_address.rfind(':')]
    device = pcie_bus_address[pcie_bus_address.rfind(':') + 1:pcie_bus_address.rfind('.')]
    func = pcie_bus_address[pcie_bus_address.rfind('.') + 1:]

    domain_num = int(domain, 16)
    domain_hex = hex(domain_num % 256).replace('0x', '').rjust(2, '0')

    ctrl = hex((ctrl_id << 3) + namespace_id).replace('0x', '')
    return f"N{domain_hex}{bus}{device}{func}C{ctrl}"


print(f'{nvme_slot(pcie_bus_address="10000:01:00.0", ctrl_id=0, namespace_id=1)=}')
print(f'{nvme_slot(pcie_bus_address="10000:02:00.0", ctrl_id=0, namespace_id=1)=}')
print(f'{nvme_slot(pcie_bus_address="10001:01:00.0", ctrl_id=0, namespace_id=1)=}')
print(f'{nvme_slot(pcie_bus_address="10001:02:00.0", ctrl_id=0, namespace_id=1)=}')
print(f'{nvme_slot(pcie_bus_address="10001:02:00.0", ctrl_id=1, namespace_id=1)=}')
print(f'{nvme_slot(pcie_bus_address="10001:02:00.0", ctrl_id=1, namespace_id=2)=}')

print(f'{nvme_slot(pcie_bus_address="0000:d7:16.4", ctrl_id=0, namespace_id=1)=}')
