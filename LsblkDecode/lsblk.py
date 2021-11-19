"""
@file: lsblk.py
@time: 2019/12/26
@author: alfons
"""

import os
from string import ascii_letters, digits
from typing import Dict

from pydantic import BaseModel, Field


class LsblkRowModel(BaseModel):
    block_device: str = Field(..., description="块设备绝对路径")
    physical_device: str = Field(..., description="块设备对应的物理磁盘的绝对路径")
    maj_min: str = Field(..., description="块设备的设备号")
    rm: int = Field(..., description="removable_device")
    size_bytes: int = Field(..., description="块设备大小，单位为bytes")
    size_str: str = Field(..., description="块设备大小，字符串方式显示")
    ro: int = Field(..., description="read_only_device")
    type: str = Field(..., description="块设备类型，disk、part等")
    mount_point: str = Field(..., description="挂载的文件系统目录")


def get_info() -> Dict[str, LsblkRowModel]:
    """
    执行lsblk命令，返回lsblk序列化后的结果
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
    with open("./blkid_output.txt", "r") as f:
        blkid_str = f.read()
        blk_name_path_dict = {os.path.basename(b): b for b in blkid_str.splitlines()}

    with open("./lsblk_output.txt", "r") as f:
        lsblk_str = f.read()

    lsblk_info = dict()
    physical_device = ""
    for line in lsblk_str.splitlines():
        if not line:
            continue

        try:
            temp_arr = line.split()
            temp_arr.append("")  # 防止最后挂载点抛异常
            if len(temp_arr) > 2 and "dm" in temp_arr[1]:
                temp_arr[1:] = temp_arr[2:]

            block_name, maj_min, removable_device, size_bytes, read_only_device, device_type, mount_point, *_ = temp_arr

            # 第一个元素如果不以特殊字符开头，则作为物理盘记录
            if block_name and block_name[0] in list(ascii_letters + digits + '/'):
                physical_device = blk_name_path_dict.get(block_name, f"/dev/{block_name}")

            # 获取路径前需要替换特殊字符串
            block_name = block_name.replace('└─', '').replace('├─', '')
            block_device = blk_name_path_dict.get(block_name, f"/dev/{block_name}")

            lsblk_info.update({
                block_device: LsblkRowModel(block_device=block_device,
                                            physical_device=physical_device,
                                            maj_min=maj_min,
                                            rm=int(removable_device),
                                            size_bytes=int(size_bytes),
                                            size_str=size_bytes,
                                            ro=int(read_only_device),
                                            type=device_type,
                                            mount_point=mount_point, )
            })
        except Exception as e:
            print(e)

    return lsblk_info



if __name__ == '__main__':
    res = get_info()
    pass