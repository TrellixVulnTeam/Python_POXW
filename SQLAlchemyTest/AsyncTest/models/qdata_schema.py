#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: qdata_schema.py
# Desc: 作为
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/7/22 4:27 下午
# History:
#=============================================================================
"""
from enum import Enum
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field


# ============================ 部分可格式化的数据类型 ==========================
class RacInfoModel(BaseModel):
    scan_port: int  # scan端口
    # 废弃掉了
    # db_user: str  # db用户
    # db_pass: str  # db密码
    asm_user: str  # asm用户
    asm_pass: str  # asm密码
    grid_home: str  # grid用户，程序执行路径
    grid_user: str  # grid用户名
    oracle_home: str  # oracle用户，程序执行路径
    oracle_user: str  # oracle用户名


class SshInfoModel(BaseModel):
    username: str
    password: str
    port: int = 22
    pkey: str


class ReplaceDiskAttrModel(BaseModel):
    is_refresh: bool = Field(default=False, description="是否正在刷新")
    last_refresh_timestamp_start: float = Field(default=0, description="最后一次元数据刷新开始的时间")
    last_refresh_timestamp_end: float = Field(default=0, description="最后一次元数据刷新结束的时间")
    last_is_success: bool = Field(default=True, description="最后一次刷新是否成功")

    last_fail_timestamp: float = Field(default=0, description="最后一次刷新失败的时间")
    last_fail_msg: str = Field(default="", description="该条数据最后一次刷新失败的异常原因")

    last_handle_timestamp: float = Field(default=0, description="最后一次换盘操作的时间")


# ===================== 磁盘相关属性 ===================
# 磁盘分区信息
class PartInfoModel(BaseModel):
    path: str = Field(..., description="分区磁盘所在的路径")
    real_path: str = Field('', description="分区所在磁盘的真实路径")
    size_bytes: int = Field(..., description="分区磁盘大小，单位bytes")


# raid下管理磁盘的相关信息
class RaidInfoModel(BaseModel):
    class RaidLevel(str, Enum):
        RAID_0: str = "RAID-0"
        RAID_1: str = "RAID-1"
        NO_RAID: str = ''

    raid_level: RaidLevel = Field(..., description="磁盘所做的raid级别，可用于区别系统盘")
    WWN: str = Field(..., description="物理磁盘在raid卡上显示的wwn标识")
    inquiry_data: str = Field(..., description="物理磁盘在raid卡上的Inquiry Data标识")


# nvme磁盘相关信息
class NvmeInfoModel(BaseModel):
    SN: str = Field(..., description="磁盘的SerialNumber")
    model: str = Field(..., description="磁盘的生产厂商号 INTEL SSDPE2KE032T8")
    namespace_id: int = Field(..., description="nvme磁盘所属的命名空间")
    firmware_version: str = Field(..., description="nvme使用的固件版本信息")
    sector_size: str = Field(..., description="扇区大小")


class FlashInfoModel(BaseModel):
    sector_size: str = Field(..., description="扇区大小")


# ===================== alert表结构相关属性 ===================
class AlertSeverityModel(BaseModel):
    value: Union[int, float] = Field(..., description="操作对应的值")
    operators: str = Field(..., description="操作")
    group_interval: str = Field(..., description="通知间隔")
    repeat_interval: str = Field(..., description="重复通知间隔")


class AlertUintValueModel(BaseModel):
    desc: str = Field(..., description="单位描述")
    name: str = Field(..., description="真正的告警项指标名")
    unit: str = Field(..., description="单位")
    metric_en: str = Field(..., description="告警项指标英文名,用于显示用")
    warn_value: float = Field(..., description="警告阈值")
    critical_value: float = Field(..., description="严重阈值")
    warn_operators: str = Field(..., description="操作")
    critical_operators: str = Field(..., description="操作")


# 告警实例配置的告警指标数据集合
class AlertMetricDetailModel(BaseModel):
    class MetricType(str, Enum):
        value: str = "value"
        state: str = "state"

    class AlertGrade(str, Enum):
        all: str = "all"
        warn: str = "warn"
        critical: str = "critical"

    id: int = Field(description="告警项id")
    name: str = Field(..., description="告警项的名字")
    type: str = Field(..., description="指标类型")
    metric: str = Field(..., description="告警项指标名,用于告警用")
    metric_en: str = Field(..., description="告警项指标英文名,用于显示用")
    description: str = Field(..., description="告警项的描述")
    err_code: str = Field(..., description="错误码")
    metric_parent: str = Field(..., description="指标类型 os/hardware")
    exporter: str = Field(..., description="指标所属的exporter")
    last: int = Field(..., description="告警项满足阈值条件时的持续时长")
    unit: str = Field(default="", description="指标单位")
    warn: AlertSeverityModel
    critical: AlertSeverityModel
    metric_type: MetricType = Field(default=MetricType.state, description="告警项是域值还是状态值")
    alert_grade: AlertGrade = Field(default=AlertGrade.warn, description="告警项为域值时值为all,告警项为状态值时warn或者critical")
    ignore_label: str = Field(default="", description="过滤条件前缀提示")
    ignore_value: Optional[str] = Field(default="", description="过滤条件")
    advanced_time: bool = Field(..., description="是否启动单项告警通知间隔")
    advanced_start: bool = Field(..., description="是否启动高级功能")
    optional_value: str = Field(default="", description="单位为可选时,即unit_optional为True时,metric为抽象意义上的指标名,optional_value才是是真正的指标名")
    prompt: str = Field(..., description="告警项的提示")
    ignore_optional: bool = Field(..., description="是否需要过滤")
    unit_optional: bool = Field(..., description="单位是否可选,即会导致一个指标实际上对应多个指标")
    unit_value: List[AlertUintValueModel]


class AlertLogMetricDetailModel(BaseModel):
    class AlertGrade(str, Enum):
        all: str = "all"
        warn: str = "warn"
        critical: str = "critical"

    alert_grade: AlertGrade = Field(default=AlertGrade.warn, description="告警项为域值时值为all,告警项为状态值时warn或者critical")
    description: str = Field(..., description="告警项的描述")
    err_code: str = Field(..., description="错误码")
    errorkeys: str = Field(..., description="告警关键字")
    ignorekeys: str = Field(..., description="忽略关键字")
    lines: int = Field(..., description="上下文行数")
    log_optional: bool = Field(default=True)
    logpaths: str = Field(description="日志路径")
    name: str = Field(..., description="日志告警项的名字")
    metric: str = Field(..., description="告警项指标名,用于告警用")


# 告警实例的指标信息
class AlertParameterModel(BaseModel):
    repeat: str = Field(default="60m", description="重复告警间隔")
    interval: str = Field(default="90s", description="通知间隔")
    # fixme: more information
    # loginfoes 日志告警
    loginfoes: Union[List[AlertLogMetricDetailModel], List[Any]]
    metrics: Union[List[AlertMetricDetailModel], List[Any]]


# 告警模板的信息
class AlertTemplateDetailModel(BaseModel):
    id: int
    type: str
    type_name: str
    name: str
    product_name: str
    desc: Optional[str]
    parameter: AlertParameterModel
    product_type: str


# 实例配置的告警详情信息
class AlertConfigDetailModel(BaseModel):
    id: int = Field(..., description="告警实例的id")
    tid: str = Field(..., description="告警实例的tid")
    name: Optional[str] = Field(..., description="告警实例的名字")
    ip: str = Field(..., description="主机，交换机等的ip")
    type: str = Field(..., description="告警实例的类型")
    type_name: str = Field(..., description="告警实例的类型中文名")
    warn_type: List[str] = Field(..., description="告警通知方式")
    warn_status: int = Field(..., description="告警状态")
    warn_group: List[str] = Field(..., description="告警实例的接受组")
    product_type: str = Field(..., description="告警实例所属的集群类型")
    db_user: str = Field(..., description="监控用户,qdata中为-")
    parameter: AlertParameterModel = Field(..., description="告警规则内容")
    ipmi_allow_manufacturer: bool = Field(..., description="硬件机型是否符合硬件白名单")


class AlertConfigDetailInfo(AlertConfigDetailModel):
    containers: Union[List[AlertConfigDetailModel], List[Any]]


class JobType(str, Enum):
    # ========================  job类型 ==========================
    JOB_TYPE_CREATE_DB = "Apply db"
    JOB_TYPE_CREATE_PDB = "Apply pdb"
    JOB_TYPE_CREATE_SCHEMA = "Apply schema"
    JOB_TYPE_REMOVE_DB = "Remove Database"
    JOB_TYPE_ADD_FILE = "Add file"
    JOB_TYPE_CREATE_TABLESPACE = "Apply tableSpace"
    JOB_TYPE_CREATE_SERVICE = "Apply service"
    JOB_TYPE_CREATE_DATAFILE = "Add dataFile"
    # 开关 集群
    JOB_TYPE_START_CLUSTER = "Start cluster"
    JOB_TYPE_STOP_CLUSTER = "Stop cluster"
    # 启停 实例
    JOB_TYPE_START_INSTANCE = "Start instance"
    JOB_TYPE_STOP_INSTANCE = "Stop instance"
    # 启停DB
    JOB_TYPE_START_DB = "Start db"
    JOB_TYPE_STOP_DB = "Stop db"
    # 在线迁移
    JOB_TYPE_MIGRATE_RON = "Migrate RacOneNode"
    # 设置归档模式
    JOB_TYPE_SET_ARCHIVELOG = "Set ARCHIVE"
    JOB_TYPE_SET_NOARCHIVELOG = "Set UNARCHIVE"
    # serverpool
    JOB_TYPE_CREATE_SERVERPOOL = "Apply serverpool"
    JOB_TYPE_DELETE_SERVERPOOL = "Delete serverpool"
    JOB_TYPE_MODIFY_SERVERPOOL = "Modify serverpool"
    JOB_TYPE_MODIFY_CPU = "Modify cpu"
    JOB_TYPE_MODIFY_SGA = "Modify sga"
    # 容器管理
    JOB_TYPE_CLOSE_PDB = "Stop pdb"
    JOB_TYPE_OPEN_PDB = "Start pdb"
    JOB_TYPE_REMOVE_PDB = "Remove pdb"
    JOB_TYPE_EXPANSION_PDB = "Capacity pdb"


class JobStatus(str, Enum):
    # ============================  job 进度条 ======================
    JOB_PROGRESS_WAIT = "Waiting schedule"
    JOB_ERROR = "Error"
    JOB_DONE = "Done"
    JOB_CLOSED = "Closed"
    JOB_TIMEOUT = "Schedule timeout"
    JOB_RUNNING = "Running"
