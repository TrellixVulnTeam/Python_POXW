#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
attr = {
    "hca": {
        "0x98039b0300c87c90L": {
            "name": None,
            "ports": [
                {
                    "bond": True,
                    "name": "mlx5_0",
                    "port": 1,
                    "status": "Active",
                    "ib_port": "ib0",
                    "switch_id": "0xb8599f0300a60a10L",
                    "switch_port": "9"
                }
            ],
            "ca_type": "MT4119",
            "port_count": 1
        },
        "0x98039b0300c87e80L": {
            "name": None,
            "ports": [
                {
                    "bond": True,
                    "name": "mlx5_1",
                    "port": 1,
                    "status": "Active",
                    "ib_port": "ib1",
                    "switch_id": "0xb8599f0300a609b0L",
                    "switch_port": "9"
                }
            ],
            "ca_type": "MT4119",
            "port_count": 1
        }
    },
}


def get_ibcard_ips():
    """返回该结点下的ib网卡连接信息"""
    ibcard_ip_list = attr.get("ibcard_ip", list())
    if ibcard_ip_list:
        return ibcard_ip_list

    hca_info = attr.get("hca", dict())
    for hca_value_info in hca_info.values():
        ib_info_list = hca_value_info.get("ports", list())
        ib_ip_list = [ib_info.get("ip", "") for ib_info in ib_info_list]
        ib_ip_list = [ib_str[:ib_str.rfind('/')] for ib_str in ib_ip_list if ib_str]
        ibcard_ip_list.extend(ib_ip_list)

    return list(set(ibcard_ip_list))


get_ibcard_ips()
# disk_name = "/dev/VolGroup/voting"
# print(disk_name[disk_name.rfind('/'):])
#
# d_a = {}
# d_a.update({'a': 1, 'b': 2})
# d_a.update({})
#
# print(d_a)
#
# part_list = [p[p.find('/') + 1:].strip() for p in "".split(' ')]
# print("part_list -> {}".format(part_list))
#
# print("""select path,state,os_mb,free_mb,reads,writes from v$asm_disk;""".upper())


def convert_capacity_bytes_auto(size, start_unit="B", is_iec=False):
    """
    单位自动转换
    :param size: 待转换的大小
    :param start_unit: 开始时size对应的大小
    :param is_iec: 是否使用IEC标准，默认不使用，进制是1000
    :return:
    """
    system = 1024 if is_iec else 1000
    multiplier = {
        5: 'PB',
        4: 'TB',
        3: 'GB',
        2: 'MB',
        1: 'KB',
        0: 'B',
        'PB': 5,
        'TB': 4,
        'GB': 3,
        'MB': 2,
        'KB': 1,
        'B': 0,
    }

    unit = multiplier[start_unit.upper()]
    while size // system:
        if unit == 5:
            break

        unit += 1
        size /= system

    return "{size:.2f}{unit}".format(size=size, unit=multiplier.get(unit))


print(convert_capacity_bytes_auto(size=1024, is_iec=True))
print(convert_capacity_bytes_auto(size=1025, start_unit="PB", is_iec=True))
print(convert_capacity_bytes_auto(size=10244, start_unit="MB", is_iec=True))
print(convert_capacity_bytes_auto(size=1996, start_unit="TB", is_iec=True))
print(convert_capacity_bytes_auto(size=0, start_unit="MB", is_iec=True))

set_a = set()
set_a.add('a')
set_a.add('b')

print('a' in set_a)

version_str = "QDataMgr(7.0.0)"
prefix = "QDataMgr"
if version_str and version_str.startswith(prefix):
    print(version_str.strip()[len(prefix) + 1:-1])

dict_a = dict(a=1, b=2)
print(dict_a)
dict_a.pop('a')
print(dict_a)

ssh_str = "OpenSSH_7.6p1 Ubuntu-4ubuntu0.3, OpenSSL 1.0.2n  7 Dec 2017"
res = ssh_str[8:ssh_str.find('.')]
print(res)