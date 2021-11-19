#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
from typing import Dict, List
from pydantic import BaseModel, Field

import json

max_target_id = 4
set_a = set(range(1, max_target_id + 1))
set_b = {1, 2, 4}

print(set_a)
print(set_b)
print(set_a - set_b)

inquiry_data = b"000006128b01100253454147415445205354313230304d4d30303939202020205354333357464b375a4a4a4b000000000000000000000000000000a20c6020e0046004c00000000000000000000000000000000000000000000000000000000000436f70797269676874202863292032303138205365616761746520416c6c20"
with open("1", "wb") as f:
    f.write(inquiry_data)


class RaidPhysicalDiskInfoModel(object):
    slot = "N/A"  # 磁盘的slot号，用于快速识别磁盘在物理机上的位置
    real_path = "N/A"  # 磁盘真实路径

    parts = list()  # 磁盘的分区信息

    # 虚拟磁盘信息
    raid_level = "N/A"  # raid等级
    virtual_drive_id = None  # 物理磁盘所在的逻辑磁盘的virtual_drive
    cache_policy = "N/A"  # 磁盘对应的VD所使用的的cache策略
    firmware_state = "N/A"  # 物理磁盘状态

    # -------------------------- 物理磁盘信息 --------------------------
    # 插槽信息
    pci_id = -1  # slot号中对应的raid所在的pci插槽所在主板的插槽号
    pci_bus_address = "N/A"  # slot号中对应的raid所在的pci插槽总线地址

    enclosure_id = None  # 物理磁盘对应的背板所在的raid卡上的 enclosure_id, 通过MegaCli -EncInfo -aall结果映射得到
    enclosure_device_id = -1  # 物理磁盘对应的背板所在的raid卡上的 enclosure_device_id

    slot_number = -1  # 物理磁盘所在的背板上的slot_number

    # 硬件信息
    interface = "N/A"  # 磁盘接口类型，如SAS、SATA
    media_type = "N/A"  # 磁盘介质类型，如HDD、SSD
    wwn = "N/A"  # 磁盘的wwn号
    vendor = "N/A"  # 磁盘厂商
    inquiry_data = "N/A"  # 磁盘序列号
    foreign_state = "N/A"  # 对外的状态
    temperature = "N/A"  # 磁盘温度

    # 磁盘大小信息
    sector_size = -1  # 扇区大小，单位byte
    raw_size_str = "N/A"  # 裸盘出厂大小，字符串类型
    raw_size_byte = -1  # 裸盘出厂大小，单位byte
    non_coerced_size_str = "N/A"  # raid卡管理下的大小，字符串类型
    non_coerced_size_byte = -1  # raid卡管理下的大小，单位byte
    coerced_size_str = "N/A"  # 实际磁盘可使用大小，lsblk展示值，字符串类型
    coerced_size_byte = -1  # 实际磁盘可使用大小，lsblk展示值，单位byte

raid_a = RaidPhysicalDiskInfoModel()
raid_a.interface = "SAS"

raid_b = RaidPhysicalDiskInfoModel()
print(raid_b.interface)

# class CephOsd(BaseModel):
#     name: str
#     size: str
#     path: str
#
#
# class CephCluster(BaseModel):
#     replications: int = Field(3)
#
#     original_nodes: List[str]
#     redundancy_nodes: List[str]
#
#     nodes: Dict[str, List[CephOsd]]
#
#
# if __name__ == '__main__':
#     ceph = CephCluster(replications=3,
#                        original_nodes=["node_a", "node_b", "node_c"],
#                        redundancy_nodes=["node_x"],
#                        nodes=dict(node_a=[CephOsd(name="osd0", size="10GB", path="/dev/sda"),
#                                           CephOsd(name="osd1", size="10GB", path="/dev/sdb"), ],
#                                   node_b=[CephOsd(name="osd2", size="10GB", path="/dev/sda"),
#                                           CephOsd(name="osd3", size="10GB", path="/dev/sdb"), ],
#                                   node_c=[CephOsd(name="osd4", size="10GB", path="/dev/sda"),
#                                           CephOsd(name="osd5", size="10GB", path="/dev/sdb"), ],
#                                   ), )
#     print(json.dumps(ceph.dict(), indent=4))
