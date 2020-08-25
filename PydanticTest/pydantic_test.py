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

from pydantic import BaseModel, Field, validator


class test_a(BaseModel):
    a: str = Field(..., alias="Is_a")

    @validator("a")
    def convent(cls, v):
        return [v]


a = test_a(Is_a="10")
print(a.dict())
print("".split())
