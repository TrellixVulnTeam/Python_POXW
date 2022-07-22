#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: new_enum.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/1/3 8:50 PM
# History:
#=============================================================================
"""
from enum import Enum


class QEnum(str, Enum):

    @classmethod
    def iter_with_value(cls):
        return (v.value for v in cls)


class QLinkBlockTypeEnum(QEnum):
    """qlink支持的块设备类型"""

    nvme = "nvme"
    raid = "raid"
    qbo = "qbo"


if __name__ == '__main__':
    print(list(QLinkBlockTypeEnum.iter_with_value()))
