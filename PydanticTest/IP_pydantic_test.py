#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: IP_pydantic_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/4/26 11:27 上午
# History:
#=============================================================================
"""
from typing import Union

from ipaddress import IPv4Address, IPv6Address
from pydantic import BaseModel, Field
from pydantic.schema import schema, model_process_schema


class IPTestModel(BaseModel):
    rac_id: int = Field(..., description="主机的rac_id，用于脑裂处理")
    hostname: str = Field(..., description="主机名")
    ip: Union[IPv4Address, IPv6Address] = Field(..., description="主机的以太网ip")
    drbd_ip: Union[IPv4Address, IPv6Address] = Field(..., description="主机drbd设备数据同步ip")
    drbd_port: int = Field(..., description="主机drbd设备数据同步port")

    @property
    def drbd_ip_2(self) -> Union[IPv4Address, IPv6Address]:
        return self.drbd_ip


if __name__ == '__main__':
    ip = "fe80::f652:1403:93:1ed1"
    drbd_ip = "fe80::f652:1403:93:1ed1"

    test = IPTestModel(
        rac_id=1,
        hostname="test1",
        ip=ip,
        drbd_ip=drbd_ip,
        drbd_port=3306
    )
    print(test)

    print(f"{IPTestModel.__fields__}")

    res = schema([IPTestModel])
    pass
