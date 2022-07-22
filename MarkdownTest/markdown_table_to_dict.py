#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: markdown_table_to_dict.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/7/20 15:31
# History:
#=============================================================================
"""
import json
import pathlib
from typing import Dict, Union, List, Optional, Any

from pydantic import BaseModel, Field, validator


class MarkdownTablePatchModel(BaseModel):
    serial: str = Field(..., alias="补丁名")
    product_type: str = Field(..., alias="关联产品类型")
    product_name_and_version: Dict[Union[str, str], List[str]] = Field(..., alias="关联产品名称和版本")
    is_reboot: bool = Field(..., alias="补丁安装后是否需要重启")
    type: str = Field(..., alias="补丁类型")
    level: str = Field(..., alias="补丁严重级别")
    short_comment: str = Field(..., alias="补丁简短说明")
    long_comment: str = Field(..., alias="补丁详细说明")
    solution: str = Field(..., alias="补丁所使用的解决方案")
    qcs_url: Optional[str] = Field(..., alias="QCS工单链接")
    jone_url: Optional[str] = Field(..., alias="Jone任务链接")
    wiki_url: Optional[str] = Field(..., alias="Wiki链接")

    @validator("product_name_and_version", pre=True)
    def convert_str_to_dict(cls, value: str) -> Dict[str, Any]:
        return json.loads(value)


def convert_markdown_table_to_dict(markdown_file: pathlib.Path) -> MarkdownTablePatchModel:
    """
    转换 markdown 中的表格至 dict
    :param markdown_file: markdown 文件路径
    :return:
    """
    line_num = 0
    table_dict = dict()
    with open(markdown_file, 'r') as f:
        for line in f.readlines():

            # 遇到特殊字符，进行处理
            #   <!-- 省略字符，遇到时为表格的末尾，退出循环
            #   | 表格字符，没有以 | 开头，继续执行
            if line.strip().startswith("<!--"):
                break

            if not line.strip().startswith('|'):
                continue
            else:
                line_num += 1

            if line_num > 2:
                zh_key, value = [v.strip() for v in line.strip()[1:-1].split('|')]

                # 必填字段如果内容为空，需要停止后续所有内容
                if zh_key.startswith("*") and not value:
                    raise ValueError("字段（{field}）为必填字段！！".format(field=zh_key))

                table_dict.update({zh_key.replace('*', '').strip(): value})

    return MarkdownTablePatchModel(**table_dict)


if __name__ == '__main__':
    print(convert_markdown_table_to_dict(pathlib.Path("./README.md")).json(indent=4, ensure_ascii=False))
