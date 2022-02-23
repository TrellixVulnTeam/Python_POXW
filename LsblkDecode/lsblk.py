"""
@file: lsblk.py
@time: 2019/12/26
@author: alfons
"""
import logging
import pathlib
from string import ascii_letters, digits
from typing import AsyncGenerator, Dict, List, Optional

from string import ascii_letters, digits
from typing import Dict

from pydantic import BaseModel, Field


class LsblkRowModel(BaseModel):
    block_device: Optional[pathlib.Path] = Field(..., description="块设备绝对路径")
    physical_device: Optional[pathlib.Path] = Field(..., description="块设备对应的物理磁盘的绝对路径")
    maj_min: str = Field(..., description="块设备的设备号")
    rm: int = Field(..., description="removable_device")
    size_bytes: int = Field(..., description="块设备大小，单位为bytes")
    size_str: str = Field(..., description="块设备大小，字符串方式显示")
    ro: int = Field(..., description="read_only_device")
    type: str = Field(..., description="块设备类型，disk、part等")
    mount_point: Optional[pathlib.Path] = Field(..., description="挂载的文件系统目录")


def lsblk_info(blkid_result_out, lsblk_result_out, show_real_path: bool = False) -> List[LsblkRowModel]:
    """
    执行lsblk命令，返回lsblk序列化后的结果

    :param show_real_path: 是否展示设备的真实路径
    :return:
    {
        '/dev/sdh': {
           'maj_min': '8:112',
           'mount_point': '',
           'physical_device': '/dev/sdh',
           'rm': '0',
           'ro': '0',
           'size_bytes': '1799792623616',
           'size_str': '1.64TB',
           'type': 'disk'
        },
        '/dev/sdh1': {
            'maj_min': '8:113',
            'mount_point': '',
            'physical_device': '/dev/sdh',
            'rm': '0',
            'ro': '0',
            'size_bytes': '1048576',
            'size_str': '1.00MB',
            'type': 'part'
        },
        ...
    }
    """
    # 获取kernel name 与 磁盘路径的映射关系
    # blkid_result = await run_cmd(cmd="blkid -o device")
    blk_name_path_dict: Dict[str, pathlib.Path] = {pathlib.Path(b).name: pathlib.Path(b) for b in blkid_result_out.splitlines()}

    # 解析 lsblk 结果
    # lsblk_result = await run_cmd(cmd="lsblk -nb")
    lsblk_info_list = list()
    physical_device = None  # 需要放置在for循环外部
    for line in lsblk_result_out.splitlines():
        if not line:
            continue

        try:
            temp_attr = line.split()
            temp_attr.append("")  # 防止最后挂载点抛异常
            if len(temp_attr) > 2 and "dm" in temp_attr[1]:
                temp_attr[1:] = temp_attr[2:]
            elif len(temp_attr) > 2 and temp_attr[0] == '│':
                temp_attr = temp_attr[1:]

            # 解析参数
            block_name, maj_min, removable_device, size_bytes, read_only_device, device_type, mount_point, *_ = temp_attr

            # 第一个元素如果不以特殊字符开头，则作为物理盘记录
            if block_name and block_name[0] in list(ascii_letters + digits + '/'):
                physical_device = blk_name_path_dict.get(block_name, pathlib.Path(f"/dev/{block_name}"))

            # 获取路径前需要替换特殊字符串
            block_name = block_name.replace('└─', '').replace('├─', '')
            block_device = blk_name_path_dict.get(block_name, pathlib.Path(f"/dev/{block_name}"))

            lsblk_info_list.append(
                LsblkRowModel(
                    block_device=block_device,
                    physical_device=physical_device,
                    maj_min=maj_min,
                    rm=int(removable_device),
                    size_bytes=int(size_bytes),
                    size_str=size_bytes,
                    ro=int(read_only_device),
                    type=device_type,
                    mount_point=pathlib.Path(mount_point) if mount_point else None,
                )
            )

        except Exception as e:
            logging.exception(e)

    return lsblk_info_list


if __name__ == '__main__':
    blkid_result_out = """
/dev/nvme6n1
/dev/nvme5n1
/dev/sda1
/dev/sda2
/dev/sda3
/dev/mapper/rhel-root
/dev/mapper/rhel-swap
/dev/mapper/rhel-oswbb
    """.strip()
    lsblk_result_out = """
sda                   8:0    0 1199638052864  0 disk
├─sda1                8:1    0    1073741824  0 part /boot
├─sda2                8:2    0  541169025024  0 part
│ ├─rhel-root       253:0    0  536870912000  0 lvm  /
│ └─rhel-swap       253:1    0    4294967296  0 lvm  [SWAP]
└─sda3                8:3    0  657394237440  0 part
  ├─rhel-oswbb      253:2    0   21474836480  0 lvm  /oswbb
  ├─rhel-db0_voting 253:3    0    4294967296  0 lvm
  ├─rhel-db0_dcr    253:4    0    1073741824  0 lvm
  ├─rhel-db1_voting 253:5    0    4294967296  0 lvm
  ├─rhel-db1_dcr    253:6    0    1073741824  0 lvm
  ├─rhel-db2_voting 253:7    0    4294967296  0 lvm
  ├─rhel-db2_dcr    253:8    0    1073741824  0 lvm
  ├─rhel-db3_voting 253:9    0    4294967296  0 lvm
  ├─rhel-db3_dcr    253:10   0    1073741824  0 lvm
  ├─rhel-db4_voting 253:11   0    4294967296  0 lvm
  ├─rhel-db4_dcr    253:12   0    1073741824  0 lvm
  ├─rhel-db5_voting 253:13   0    4294967296  0 lvm
  ├─rhel-db5_dcr    253:14   0    1073741824  0 lvm
  ├─rhel-db6_voting 253:15   0    4294967296  0 lvm
  ├─rhel-db6_dcr    253:16   0    1073741824  0 lvm
  ├─rhel-db7_voting 253:17   0    4294967296  0 lvm
  ├─rhel-db7_dcr    253:18   0    1073741824  0 lvm
  ├─rhel-db8_voting 253:19   0    4294967296  0 lvm
  ├─rhel-db8_dcr    253:20   0    1073741824  0 lvm
  ├─rhel-db9_voting 253:21   0    4294967296  0 lvm
  └─rhel-db9_dcr    253:22   0    1073741824  0 lvm
nvme0n1             259:0    0 1600321314816  0 disk
nvme1n1             259:2    0 1600321314816  0 disk
nvme2n1             259:1    0 1600321314816  0 disk
nvme3n1             259:6    0  800166076416  0 disk
nvme4n1             259:4    0  800166076416  0 disk
nvme5n1             259:5    0  800166076416  0 disk
nvme6n1             259:3    0  800166076416  0 disk
    """.strip()

    res = lsblk_info(blkid_result_out=blkid_result_out, lsblk_result_out=lsblk_result_out)
    pass
