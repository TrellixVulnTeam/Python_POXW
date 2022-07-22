#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: patch_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/7/19 09:52
# History:
#=============================================================================
"""
import datetime
import pathlib
from enum import Enum
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List, Union


class PatchLevelEnum(str, Enum):
    """
    补丁严重等级
    """
    IMPORTANT = "Important"  # 必须打
    NORMAL = "Normal"  # 可以选择打


class PatchTypeEnum(str, Enum):
    """
    补丁类型
    """
    BUGFIX = "Bugfix"  # bug修复类型
    UPGRADE = "Upgrade"  # 升级类型


class ProductTypeEnum(str, Enum):
    """
    产品类型
    """
    CLUSTER = "一体机"  # 一体机产品
    MANAGER = "Cloud"  # cloud产品


class ProductClusterNameTypeEnum(str, Enum):
    """
    一体机产品名
    """
    QDATA_STANDARD = "Standard"
    QDATA_SANFREE = "QOne"
    QDATA_LONGHUAL = "Infinite"
    DM_SANFREE = "QDM"
    QPLUS = "QPlus"
    QFUSION = "QFusion"


class ProductCloudNameTypeEnum(str, Enum):
    """
    Cloud产品名
    """
    WEB_SERVER = "WebServer"
    CLOUD_MANAGER = "CloudManager"
    HULK = "Hulk"
    QCP = "QCP"


class PatchVersionModel(BaseModel):
    """
    补丁包中的 .version 文件数据结构
    """

    attr: Dict[str, Any] = Field(dict(), description="预留字段")

    serial: str = Field(..., example="Q-20220713-001", description='编号')
    product_type: ProductTypeEnum = Field(..., description="产品类型")
    product_name_and_version: Dict[Union[ProductClusterNameTypeEnum, ProductCloudNameTypeEnum], List[str]] = Field(
        ...,
        example={"Standard": ["7.3.1", "8.2.0", "8.3.1"]},
        description="支持的产品名称及版本字典，key为产品名称，value为产品版本列表",
    )

    is_reboot: bool = Field(..., description='是否需要重启')
    level: PatchLevelEnum = Field(..., description='严重级别')
    type: PatchTypeEnum = Field(..., nullable=False, description='补丁类型')
    built_time: Optional[datetime.datetime] = Field(None, example="2032-04-23T10:20:30", description='打包时间')
    built_timestamp: Optional[float] = Field(None, example=1966280412345.6789, description='打包时间戳')

    short_comment: str = Field(..., nullable=False, description='补丁修复问题描述')
    long_comment: str = Field(..., nullable=False, description='补丁修复问题详细说明')
    solution: str = Field(..., nullable=False, description='补丁提供的解决方案')

    gitlab_url: Optional[str] = Field(None, description='GitLab链接')
    gitlab_id: Optional[int] = Field(None, description='项目id')
    gitlab_commit_id: Optional[str] = Field(None, description='提交id')

    qcs_url: Optional[str] = Field(None, description='QCS链接')
    jone_url: Optional[str] = Field(None, description='Jone链接')
    wiki_url: Optional[str] = Field(None, description='Wiki链接')


if __name__ == '__main__':
    test_patch = PatchVersionModel(
        serial="Q-20220719-001",
        product_type=ProductTypeEnum.CLUSTER,
        product_name_and_version={
            ProductClusterNameTypeEnum.QDATA_STANDARD: ["7.2.1", "7.1.2"],
        },
        is_reboot=False,
        level=PatchLevelEnum.IMPORTANT,
        type=PatchTypeEnum.BUGFIX,
        built_time="2032-04-23 10:20:30",
        built_timestamp=1966280412345.6789,
        short_comment="测试，修复bug",
        long_comment="目前只是测试阶段，用于测试patch功能",
        solution="使用洗哦安静的方法\n"
                 "来解决该问题",
        gitlab_url="https://gitlab.com",
        gitlab_id=1,
        gitlab_commit_id="abcdef12344555211",
        qcs_url="https://qcs.com",
        jone_url="https://jone.com",
        wiki_url="https://wiki.com",
    )

    pathlib.Path("./test_patch.json").write_text(data=test_patch.json(indent=4, ensure_ascii=False))