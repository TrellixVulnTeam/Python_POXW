#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: pydantic_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/7/31 3:17 下午
# History:
#=============================================================================
"""
from enum import Enum

from typing import Optional
from pydantic import BaseModel, Field, validator


class FilterEnum(str, Enum):
    DISK_PATH = "disk_path"
    DISK_STATUS = "mode_status"
    STO_NODE = "storage_node"


print("disk_path" in list(FilterEnum))
print(list(v.value for v in list(FilterEnum)))
assert "disk_path" == FilterEnum.DISK_PATH


# class test_a(BaseModel):
#     a: int = Field(..., alias="Is_a")
#     b: Optional[bool] = Field(..., alias="Is_b")
#
#     @validator("a")
#     def convent(cls, v):
#         return [v]
#
#
# a = test_a(Is_a="10", Is_b=" no")
# print(a.dict())
# print("".split())
