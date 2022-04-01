#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: ci.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/7/7 下午3:12
# History:
#=============================================================================
"""
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    inspect,
)
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm.exc import NoResultFound

from ..base import (
    CloudEntity,  # 请不要在模板类中使用 open_session, 使用方式参考 ./__init__.py
 CloudSqlAlchemyEnum,
)
from .qdata_schema import (
    FlashInfoModel,
    JobStatus,
    NvmeInfoModel,
    PartInfoModel,
    RacInfoModel,
    RaidInfoModel,
    ReplaceDiskAttrModel,
    SshInfoModel,
)
from .utils import convert_to_size_str, convert_utc_to_beijing
from .crypt import decrypt_string, md5sum
from loguru import logger

# ==================== ci-web-service 表结构移植，说明转至 .__init__.py==========================


def gen_uuid() -> str:
    return uuid.uuid4().hex


class QDataCluster(CloudEntity):
    """集群信息表"""
    __tablename__ = "qdata_cluster"

    # enum
    THREE_TIER = "Three-tier"
    SAN_FREE = "Sanfree"
    UNKNOWN = "Unknown"
    LONGHAUL = "Longhaul"
    enum_qdtype = CloudSqlAlchemyEnum(THREE_TIER, SAN_FREE, UNKNOWN, LONGHAUL)
    TYPE_NAME = {
        THREE_TIER: u"三层架构",
        SAN_FREE: u"双节点架构",
        LONGHAUL: u"长距双活",
        UNKNOWN: u"未知",
    }

    attr = Column(JSON, default={}, doc="一体机额外信息，机房信息/scan_ip支持多个/replace_disk")
    name = Column(String(length=128), nullable=True, unique=True, doc="集群名字")
    uuid = Column(String(length=128), nullable=False, doc="集群uuid")
    type = Column(enum_qdtype, nullable=False, doc="集群类型")
    # distance = Column(Integer, nullable=True, doc="距离：1/10/40/80公里")
    description = Column(String(length=1024), nullable=True, doc="集群描述")
    ssh = Column(JSON, default={}, doc="登录集群的user/password/port/key")
    inspection = Column(JSON, default={}, doc="巡检配置信息")
    recovery_drill = Column(JSON, default={}, doc="演练恢复配置信息")
    network_monitor = Column(Boolean, default=True, doc="开启/关闭 网络质量监控")

    # 关联QDataCluster的表，后续不使用 backref 的方式进行绑定。
    # relationship参考：https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#one-to-many
    rac_clusters: Set["RacCluster"] = relationship("RacCluster", back_populates="cluster", cascade="all, delete-orphan",
                                                   collection_class=set)  # rac集群，支持多rac
    nodes: Set["QDataNode"] = relationship("QDataNode", back_populates="cluster", cascade="all, delete-orphan",
                                           collection_class=set)
    switches: Set["QDataSwitch"] = relationship("QDataSwitch", back_populates="cluster", cascade="all, delete-orphan",
                                                collection_class=set)
    diskgroup: Set["QDataIO"] = relationship("QDataIO", back_populates="cluster", cascade="all, delete-orphan",
                                             collection_class=set)  # fixme:后续去除
    arbiter: Set["LogArbiter"] = relationship("LogArbiter", back_populates="cluster", cascade="all, delete-orphan",
                                              collection_class=set)
    links: Set["LogLink"] = relationship("LogLink", back_populates="cluster", cascade="all, delete-orphan",
                                         collection_class=set)
    highvars: Set["LinkHighMgr"] = relationship("LinkHighMgr", back_populates="cluster", cascade="all, delete-orphan",
                                                collection_class=set)
    strategy: "InspectionStrategy" = relationship("InspectionStrategy", back_populates="cluster",
                                                  cascade="all, delete-orphan", uselist=False)
    # 演练关联
    net: Set["DrillNet"] = relationship("DrillNet", back_populates="cluster", cascade="all, delete-orphan",
                                        collection_class=set)
    base: Set["DrillBase"] = relationship("DrillBase", back_populates="cluster", cascade="all, delete-orphan",
                                          collection_class=set)
    range: Set["DrillRange"] = relationship("DrillRange", back_populates="cluster", cascade="all, delete-orphan",
                                            collection_class=set)
    recovery: Set["DrillRecovery"] = relationship("DrillRecovery", back_populates="cluster",
                                                  cascade="all, delete-orphan", collection_class=set)

    inspections: Set["QDataInspection"] = relationship("QDataInspection", back_populates="cluster",
                                                       cascade="all, delete-orphan", collection_class=set)

    # 集群中的asm信息
    disk_groups_info: Set["HulkDiskGroup"] = relationship("HulkDiskGroup", back_populates="cluster",
                                                          cascade="all, delete-orphan", collection_class=set)

    __repr_columns__ = ["id", "name", "type"]

    def get_ssh_config(self, ssh_name: str = "default") -> SshInfoModel:
        """
        返回集群中所有节点的ssh信息
        :param ssh_name: 配置中的ssh信息key
        :return: 连接节点的用户名，密码，端口，私钥
        """
        ssh_config = self.ssh.get(ssh_name, {})
        username = ssh_config["user"]
        password = ssh_config.get("password", "")
        if password:
            password = decrypt_string(password)
        port = ssh_config.get("port", 22)
        pkey = ssh_config.get("key", "")
        if pkey:
            pkey = decrypt_string(pkey)

        return SshInfoModel(username=username, password=password, port=port, pkey=pkey)

    @property
    def compute_nodes(self) -> List["QDataNode"]:
        """集群中的计算节点"""
        return [n for n in self.nodes if n.type in [QDataNode.COMPUTE, QDataNode.SANFREE]]

    @property
    def storage_nodes(self) -> List["QDataNode"]:
        """集群中的存储节点"""
        return sorted([n for n in self.nodes if n.type in [QDataNode.STORAGE, QDataNode.SANFREE]],
                      key=lambda node: node.id)

    @property
    def not_cloud_nodes(self) -> List["QDataNode"]:
        """
        除双活外的其他节点
        :return: 成功返回qdata节点列表；失败返回空
        """
        return sorted([n for n in self.nodes if n.type not in [QDataNode.CLOUD, ]], key=lambda node: node.id)

    @property
    def attr_rac_info(self) -> RacInfoModel:
        """
        返回rac info信息，双rac环境建议在QDataNode attr中添加rac info
        """
        rac_info = self.get_attr(key="rac_info", default=dict())
        return RacInfoModel(**rac_info)

    @property
    def attr_replace_disk(self) -> ReplaceDiskAttrModel:
        """返回智能换盘参数"""
        replace_disk_info = self.get_attr(key="replace_disk", default=dict())
        return ReplaceDiskAttrModel(**replace_disk_info)

    def update_attr_replace_disk(self, replace_disk_attr: ReplaceDiskAttrModel) -> None:
        """
        更新智能换盘参数
        :param replace_disk_attr: 待更新的智能换盘参数
        :return:
        """
        self.set_attr(key="replace_disk", value=replace_disk_attr.dict())


class QDataNode(CloudEntity):
    """主机信息表"""
    __tablename__ = "qdata_node"

    AUTO_INCREMENT_VALUE = 100000

    # enum
    COMPUTE = "compute"
    STORAGE = "storage"
    SANFREE = "sanfree"
    NORMAL = "normal"
    CLOUD = 'cloud'
    enum_host_type = CloudSqlAlchemyEnum(CLOUD, COMPUTE, STORAGE, SANFREE, NORMAL)
    NODE_TYPE = [COMPUTE, STORAGE, SANFREE, NORMAL, CLOUD]

    NODE = "host"
    HARDWARE = "hardware"
    ORACLE = "oracle"
    SWITCH = "snmp"
    REDFISH = "redfish"
    PING_CLUSTER = "bulkping"
    ETCD_EXPORTER = "etcd"
    VM_EXPORTER = "vm"
    BLACKBOX_EXPORTER = "blackbox"
    EXPORTER_TYPE = [
        NODE,
        HARDWARE,
        ORACLE,
        SWITCH,
        REDFISH,
        PING_CLUSTER,
        ETCD_EXPORTER,
        VM_EXPORTER,
        BLACKBOX_EXPORTER
    ]

    TYPE_NAME = {
        COMPUTE: u"计算节点",
        STORAGE: u"存储节点",
        SANFREE: u"融合节点",
        NORMAL: u"主机",
        CLOUD: u"分布式锁主机",
    }

    # columns
    attr = Column(JSON, default={}, doc="主机额外信息，cpu/hac/ram/raid/kernel/ibcard_ip/media_num/raid_card等")
    uuid = Column(String(100), nullable=False, default=lambda context: context.current_parameters["ip"], doc="主机uuid")
    name = Column(String(length=100), nullable=False, default=lambda context: context.current_parameters["hostname"],
                  doc="host别名")

    hostname = Column(String(length=100), nullable=False, doc="主机名")
    room = Column(String(length=100), nullable=True, doc="机房名称, room_A, room_B")
    ip = Column(String(length=39), nullable=False, doc="ip地址，长度兼容ipv6")
    vip = Column(String(length=39), nullable=True, doc="vip地址，长度兼容ipv6")
    type = Column(enum_host_type, doc="主机类型")
    rac_id = Column(Integer, default=0, doc="节点的id")
    status = Column(JSON, default={}, doc="主机状态 up/down")  # fixme 增加枚举 @jianxin
    config = Column(JSON, default={}, doc="主机配置信息")  # 存ipmi信息
    ssh = Column(JSON, default={}, doc="登录机器的user/password/port/key")

    instances = relationship("RacInstance", back_populates="node", doc="所关联的数据库实例", cascade="all, delete-orphan",
                             order_by='RacInstance.name')

    # todo 原cloud日志告警的字段，迁移到qdata_node，日志告警方案成型后，需重新考虑去留
    monitor_log_paths = relationship("RacMonitorLog", back_populates="node", cascade="all, delete-orphan",
                                     collection_class=list, order_by="asc(RacMonitorLog.path)")

    # 关联一体机集群表
    cluster_id = Column(Integer, ForeignKey(column=QDataCluster.id, ondelete="CASCADE"))
    cluster: QDataCluster = relationship(QDataCluster, back_populates="nodes", foreign_keys=[cluster_id],
                                         lazy='subquery', doc="所关联的一体机集群")

    # 关联rac集群表
    rac_cluster_id = Column(Integer, ForeignKey(column="rac_cluster.id", ondelete="SET NULL"),
                            nullable=True)  # 无法引用到RacCluster，因此使用列:字符串;并且ondelete=SET NULL，删除rac集群时，不删除其下节点，并设置本外键为null
    rac_cluster: "RacCluster" = relationship('RacCluster', back_populates="nodes", foreign_keys=[rac_cluster_id])

    # 节点下的磁盘信息
    logical_disks_info: Set["HulkLogicalDisk"] = relationship("HulkLogicalDisk", back_populates="node",
                                                              cascade="all, delete-orphan", collection_class=set)
    physical_disks_info: Set["HulkPhysicalDisk"] = relationship("HulkPhysicalDisk", back_populates="node",
                                                                cascade="all, delete-orphan", collection_class=set)
    qlinks_info: Set["HulkQLink"] = relationship("HulkQLink", back_populates="node", cascade="all, delete-orphan",
                                                 collection_class=set)

    __repr_columns__ = ["id", "name", "ip", "type", "cluster_id", "rac_cluster_id"]

    def get_ssh_config(self, ssh_name: str = "default") -> SshInfoModel:
        """
        返回连接节点的ssh信息
        :param ssh_name: 配置中的ssh信息key
        :return: 连接节点的用户名，密码，端口，私钥
        """
        return self.cluster.get_ssh_config(ssh_name)

    @property
    def rac_info(self) -> RacInfoModel:
        return self.cluster.attr_rac_info

    @classmethod
    def get_obj_by_name(cls, session: Session, cluster_id: int, node_name: str) -> "QDataNode":
        """
        通过节点名获取节点对象
        :param session: 会话对象
        :param cluster_id: 节点所在的集群id
        :param node_name: 节点名称
        :return: 存在返回节点对象，不存在返回None
        """
        return session.query(cls).filter_by(cluster_id=cluster_id, name=node_name).first()

    @classmethod
    def get_by_hostname(cls, session: Session, cluster_id: int, hostname: str) -> "QDataNode":
        """
        通过hostname查找节点
        """
        return session.query(cls).filter_by(cluster_id=cluster_id, hostname=hostname).first()

    @classmethod
    def get_by_ip(cls, session: Session, ip: str) -> "QDataNode":
        """
        通过ip查找节点
        """
        return session.query(cls).filter_by(ip=ip).first()


class QDataSwitch(CloudEntity):
    """
    集群交换机表
    """
    __tablename__ = "qdata_switch"

    # 交换机的类型有 ib_switch，longhaul
    # 与端口连接时的的类型为 ib_switch，longhaul_switch
    IB_SWITCH = "ib_switch"
    LONGHAUL_SWITCH = "longhaul"
    enum_stype = CloudSqlAlchemyEnum(IB_SWITCH, LONGHAUL_SWITCH)
    SWITCH_TYPE = [IB_SWITCH, LONGHAUL_SWITCH]
    EXPORTER_TYPE = ["snmp"]
    TYPE_NAME = {
        IB_SWITCH: u"IB交换机",
        LONGHAUL_SWITCH: u"长距IB交换机"
    }

    ROOM_A = "room_A"
    ROOM_B = "room_B"
    enum_rtype = CloudSqlAlchemyEnum(ROOM_A, ROOM_B)

    attr = Column(JSON, default={}, doc="交换机额外信息，port/password/用户名/厂商信息等")
    guid = Column(String(length=128), nullable=False, unique=False, doc="switch guid")
    type = Column(enum_stype, nullable=True, doc="交换机类型")
    name = Column(String(length=128), nullable=True, doc="交换机名字")
    ip = Column(String(length=39), default="", doc="交换机ip")
    room = Column(enum_rtype, nullable=True, doc="机房")
    port_info = Column(JSON, default={}, doc="交换机端口信息")
    port_count = Column(Integer, nullable=False, doc="交换机端口数量")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="switches", doc="所关联的集群")

    def ssh_info(self) -> Dict[str, Any]:
        """
        获取交换机的ssh信息
        """
        return {
            "ip": self.ip,
            "port": self.attr.get("port", ""),
            "username": self.attr.get("username", ""),
            "password": self.attr.get("password", ""),
        }


class QDataIO(CloudEntity):
    __tablename__ = "qdata_io"

    # START = u"开启"
    # SHUTDOWN = u"关闭"
    # UPDATE = u"更新"
    # enum_etype = Enum(START, SHUTDOWN, UPDATE)

    # disk = Column(String(length=10), nullable=False, doc="磁盘组")
    # todo 补充doc
    attr = Column(JSON, default={}, doc="")
    # fixme: 此处的diskgroup命名有待商榷
    DGs = Column(JSON, default={}, doc="磁盘组信息")
    ip = Column(String(length=39), default="", doc="操作用户ip")
    name = Column(String(length=128), nullable=True, doc="操作用户")
    event = Column(String(length=39), default="", doc="执行过的操作")
    notice = Column(String(length=200), default="", doc="操作日志记录")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="diskgroup", doc="所关联的集群")


class LogArbiter(CloudEntity):
    """仲裁日志"""
    __tablename__ = "log_arbiter"

    attr = Column(JSON, default={}, doc="")
    event = Column(String(length=50), default="", doc="事件")
    notice = Column(String(length=200), default="", doc="事件说明")
    faultip = Column(String(length=39), default="", doc="故障ip")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="arbiter", doc="所关联的集群")


class LogLink(CloudEntity):
    """操作交换机端口日志"""
    __tablename__ = "log_link"

    # todo 补充doc
    attr = Column(JSON, default={}, doc="")
    event = Column(String(length=50), default="", doc="事件")
    notice = Column(Text, default="", doc="事件说明")
    user = Column(String(length=20), default="", doc="操作人")
    ip = Column(String(length=39), default="", doc="操作人ip")
    switchname = Column(String(length=30), default="", doc="操作的交换机的名字")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="links", doc="所关联的集群")


class LinkHighMgr(CloudEntity):
    """链路管理高级功能存参"""
    __tablename__ = "link_highmgr"

    FUNCTION_ON = "on"
    FUNCTION_OFF = "off"
    enum_rtype = CloudSqlAlchemyEnum(FUNCTION_ON, FUNCTION_OFF)

    status = Column(enum_rtype, nullable=False, doc="高级功能是否开启")
    delay_nocnt = Column(Float, nullable=True, doc="持续n秒的延迟时间")
    duration_nocnt = Column(Integer, nullable=True, doc="延迟持续时间")
    unit_nocnt = Column(String(length=10), default="", doc="单位_nocnt")
    rule_nocnt = Column(Boolean, default=True, doc="是否开启了规则_nocnt")
    delay_cnt = Column(Float, nullable=True, doc="持续n分钟的延迟时间")
    duration_cnt = Column(Integer, nullable=True, doc="延迟持续时间")
    unit_cnt = Column(String(length=10), default="", doc="单位_cnt")
    rule_cnt = Column(Boolean, default=True, doc="是否开启了规则_cnt")
    count = Column(Integer, nullable=True, doc="n分钟内延迟发生次数")
    user = Column(String(length=20), default="", doc="打开高级功能的操作人")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="highvars", doc="所关联的集群")


class DrillNet(CloudEntity):
    """链路加延迟操作"""
    __tablename__ = "drill_net"

    TYPE = "net"
    start = Column(Boolean, default=False, doc="是否正在演练")
    user = Column(String(length=20), default="", doc="演练的操作人")
    webip = Column(String(length=39), default="", doc="操作人web端ip")
    ip = Column(String(length=39), default="", doc="操作的链路ip")
    ib_port = Column(String(length=39), default="", doc="操作的链路的ip所在的ib_port")
    node_ip = Column(String(length=39), default="", doc="操作的链路所在节点的ip")
    node_id = Column(Integer, nullable=False, doc="操作的链路所在节点的id")
    room_name = Column(String(length=50), default="", doc="机房名")
    delay = Column(Float, nullable=False, doc="延迟")
    shake = Column(Float, nullable=True, doc="抖动")
    loss = Column(Float, nullable=True, doc="丢包")
    duration = Column(Integer, nullable=True, doc="持续时间")

    count = Column(Integer, nullable=False, doc="演练历史计数")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="net", doc="所关联的集群")


class DrillBase(CloudEntity):
    __tablename__ = "drill_base"

    TYPE = "base"
    COMPUTE = "compute"
    STORAGE = "storage"
    SANFREE = "sanfree"
    NORMAL = "normal"
    CLOUD = 'cloud'
    SWITCH = "switch"
    enum_hosttype = CloudSqlAlchemyEnum(CLOUD, COMPUTE, STORAGE, SANFREE, NORMAL, SWITCH)

    FUNCTION_ON = "on"
    FUNCTION_OFF = "off"
    FUNCTION_RESET = "reset"
    PORT_ON = "port_on"
    PORT_OFF = "port_off"
    enum_rtype = CloudSqlAlchemyEnum(FUNCTION_ON, FUNCTION_OFF, FUNCTION_RESET, PORT_ON, PORT_OFF)

    action = Column(enum_rtype, nullable=False, doc="操作事件")
    name = Column(String(length=39), default="", doc="被操作的机器名")
    type = Column(enum_hosttype, doc="被操作的机器类型")
    ip = Column(String(length=39), default="", doc="被操作的机器的ip")
    base_id = Column(Integer, nullable=False, doc="被操作机器的id")
    room_name = Column(String(length=50), default="", doc="机房名")

    webip = Column(String(length=39), default="", doc="操作人web端ip")
    user = Column(String(length=20), default="", doc="演练的操作人")
    count = Column(Integer, nullable=False, doc="演练历史计数")  # 每12小时为一次演练

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="base", doc="所关联的集群")


class DrillRange(CloudEntity):
    __tablename__ = "drill_range"

    TYPE = "range"

    RG_ROOM_A = "room_A"
    RG_ROOM_B = "room_B"
    RG_CLOUD = "cloud"
    RG_L3 = "l3"
    RG_L2L3 = "l2l3"
    RG_L1L3 = "l1l3"

    RESULT_SUCCESS = u"成功"
    RESULT_FAILURE = u"失败"
    RESULT_UNDO = u"无"

    enum_rgtype = CloudSqlAlchemyEnum(RG_ROOM_A, RG_ROOM_B, RG_CLOUD, RG_L3, RG_L2L3, RG_L1L3)
    enum_drill_result = CloudSqlAlchemyEnum(RESULT_SUCCESS, RESULT_FAILURE, RESULT_UNDO)
    enum_recovery_result = CloudSqlAlchemyEnum(RESULT_SUCCESS, RESULT_FAILURE, RESULT_UNDO)

    action = Column(Boolean, nullable=False, doc="演练开关，1开始演练，0 已恢复")
    pre_check_msg = Column(Text, default="", doc="演练前检查环境日志")
    start_msg = Column(Text, default="", doc="执行日志")
    drill_result = Column(enum_drill_result, doc="演练结果")
    suf_check_msg = Column(Text, default="", doc="演练后检查环境日志")
    recover_msg = Column(Text, default="", doc="恢复日志")
    recovery_result = Column(enum_recovery_result, doc="恢复结果")

    webip = Column(String(length=39), default="", doc="操作人web端ip")
    user = Column(String(length=20), default="", doc="演练的操作人")
    rg_type = Column(enum_rgtype, doc="演练类型")
    count = Column(Integer, nullable=False, doc="演练历史计数")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="range", doc="所关联的集群")

    @classmethod
    def get_type_name(cls, session: Session, cluster_id: int) -> Dict[str, Any]:
        obj = QDataCluster.get_first(session, "id", cluster_id)
        type_name = {
            "room_A": obj.attr.get("room_A_name", "机房A"),
            "room_B": obj.attr.get("room_B_name", "机房A"),
            "cloud": "分布式锁",
            "l2l3": "L2和L3",
            "l1l3": "L1和L3",
            "l3": "L3"
        }
        return type_name


class DrillRecovery(CloudEntity):
    __tablename__ = "drill_recovery"

    TYPE = "recovery"

    mode = Column(Boolean, default=0, nullable=False, doc="模式，1 自动，0 手动")
    recovery_result = Column(Integer, default=0, nullable=False, doc="恢复结果，1 成功，0 失败，-1 终止")
    log = Column(Text, default="", doc="恢复日志")
    retry = Column(Integer, default=0, doc="恢复某一任务尝试次数")
    task = Column(Integer, default=7, doc="执行的任务数")
    step = Column(Integer, default=0, doc="最终执行到的任务")

    webip = Column(String(length=39), default="", doc="操作人web端ip")
    user = Column(String(length=20), default="", doc="演练的操作人")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="recovery", doc="所关联的集群")


class QDataInspection(CloudEntity):
    """巡检信息结果表
    """
    __tablename__ = "qdata_inspection"

    RUNNING = 0  # 正在检查
    FINISH = 1  # 检查完成
    CANCEL = 2  # 取消了检查

    status = Column(Integer, nullable=False, default=RUNNING, doc="检查状态")
    mode = Column(Boolean, nullable=False, doc="检查方式  True: 自动巡检 False: 手动巡检")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="inspections", doc="所关联的集群")

    @classmethod
    def get_last_inspection(cls, session: Session, cluster_id: int) -> Optional["QDataInspection"]:
        """查询最后一次的巡检对象
        :param session: session 对象
        :param cluster_id: 集群id
        """
        obj = session.query(cls) \
            .filter(cls.cluster_id == cluster_id, cls.status == cls.FINISH) \
            .order_by(cls.create_time.desc()).first()
        return obj


class QDataChannel(CloudEntity):
    """巡检接收通道
    """
    __tablename__ = "qdata_channel"

    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"), doc="集群id")
    group_id = Column(Integer, nullable=False, doc="接收组id")
    channel = Column(JSON, nullable=True, default={"email": True, "sms": False}, doc="接收告警的方式(邮件、短信)")


# todo @jianxin 检查有无必要
class QDataCollectRACLog(CloudEntity):
    """收集RAC信息记录
    """
    __tablename__ = "qdata_collect_rac_log"

    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    alias_rac_name = Column(String(length=45), nullable=False, doc="rac集群别名")
    is_success = Column(Boolean, nullable=False, doc="收集是否成功")


class QDataDiskGroup(CloudEntity):
    """集群磁盘组信息
    """
    __tablename__ = "qdata_diskgroup"

    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    alias_rac_name = Column(String(length=45), nullable=False, doc="rac集群别名")
    disk_path = Column(String(length=128), nullable=False, doc="磁盘路径", primary_key=True)
    dg_name = Column(String(length=45), nullable=False, doc="磁盘组名字")
    disk_name = Column(String(length=45), nullable=False, doc="磁盘名字")
    failgroup = Column(String(length=45), nullable=False, doc="failgroup名字")
    mode_status = Column(String(length=45), nullable=False, doc="磁盘状态")


class QDataQPlusNode(CloudEntity):
    """
    QPlus管理节点
    """
    __tablename__: str = "qdata_qplusnode"
    __table_args__: Union[Dict[str, Any], Tuple[Any]] = (  # type: ignore
        # 避免管理节点重复添加,通过联合索引，来实现双列唯一
        # Ref: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/table_config.html#declarative-table-args
        Index('ip_port', 'ip', 'port', unique=True),
        CloudEntity.__table_args__
    )

    ip = Column(String(length=15), nullable=False, doc="节点ip")
    port = Column(Integer, nullable=False, doc="管理节点端口")
    username = Column(String(length=32), nullable=False, doc="用户名")
    password = Column(String(length=128), nullable=False, doc="密码")


class HulkQLink(CloudEntity):
    """记录集群中存储节点上的qlink信息"""

    __tablename__ = "hulk_qlink"

    QLINK_DRIVER_NVMF = "nvmf"
    QLINK_DRIVER_ISER = "iser"
    QLINK_DRIVER_ISCSI = "iscsi"
    target_driver_enum = CloudSqlAlchemyEnum(QLINK_DRIVER_NVMF, QLINK_DRIVER_ISER, QLINK_DRIVER_ISCSI)

    lun_path = Column(String(length=256), primary_key=True, nullable=False, doc="qlink挂载的lun路径")
    lun_id = Column(Integer, nullable=True, doc="qlink挂载的lun id")
    lun_size_bytes = Column(BigInteger, nullable=True, doc="qlink挂载的lun大小，单位bytes")
    is_del_lun = Column(Boolean, nullable=False, doc="是否已经del_lun")

    qlink_port = Column(Integer, nullable=False, doc="qlink挂载的lun对应的qlink port")
    qlink_driver = Column(target_driver_enum, nullable=False, doc="qlink挂载的lun对应的target name")
    target_id = Column(Integer, nullable=False, doc="qlink挂载的lun对应的target id")
    target_name = Column(String(128), nullable=False, doc="qlink挂载的lun对应的target name")

    acl_list = Column(JSON, nullable=True, doc="qlink对应的acl规则")
    external = Column(String(10), nullable=True, doc="是否是通过其他节点输上来")

    # 关联的存储节点
    node_id = Column(Integer, ForeignKey(QDataNode.id, ondelete="CASCADE"), doc="磁盘所在存储节点的id")
    node = relationship(QDataNode, lazy='subquery', back_populates="qlinks_info", doc="磁盘所关联的存储节点")

    __repr_columns__ = ["qlink_port", "target_name", "lun_path"]

    @property
    def lun_size_str(self) -> str:
        return convert_to_size_str(size_num=self.lun_size_bytes)

    @classmethod
    def get_obj_by_lun_path(cls, session: Session, node_id: int, lun_path: str) -> "HulkQLink":
        """
        通过qlink挂载的lun路径查找对应的
        :param session: 会话对象
        :param node_id: LUN所在的存储节点id
        :param lun_path: 指定的lun路径
        :return:
        """
        return session.query(cls).filter_by(node_id=node_id, lun_path=lun_path).first()


class HulkDiskGroup(CloudEntity):
    """记录集群中ASM中diskgroup信息"""

    __tablename__ = "hulk_asm_disk_group"

    # 磁盘组冗余级别
    TYPE_EXTEND = "EXTEND"
    TYPE_EXTERN = "EXTERN"
    TYPE_FLEX = "FLEX"
    TYPE_HIGH = "HIGH"
    TYPE_NORMAL = "NORMAL"
    TYPE_NONE = "NONE"  # 未知类型
    diskgroup_type_enum = CloudSqlAlchemyEnum(TYPE_EXTEND, TYPE_EXTERN, TYPE_FLEX, TYPE_HIGH, TYPE_NORMAL, TYPE_NONE)

    # grid版本
    GRID_VERSION_10G = "10g"
    GRID_VERSION_11G = "11g"
    GRID_VERSION_12C = "12c"
    GRID_VERSION_18C = "18c"
    GRID_VERSION_19C = "19c"
    GRID_VERSION_UNKNOWN = "unknown"
    diskgroup_grid_version_enum = CloudSqlAlchemyEnum(GRID_VERSION_10G, GRID_VERSION_11G, GRID_VERSION_12C,
                                                      GRID_VERSION_18C, GRID_VERSION_19C, GRID_VERSION_UNKNOWN)

    group_id = Column(Integer, primary_key=True, nullable=False, doc="v$asm_diskgroup表中的 Disk group number")
    name = Column(String(length=30), nullable=False, doc="Disk group名称")
    type = Column(diskgroup_type_enum, nullable=False, doc="Disk group冗余级别")
    grid_version = Column(diskgroup_grid_version_enum, nullable=False, doc="Disk group所属的数据库版本")
    is_dropped = Column(Boolean, nullable=False, doc="磁盘组是否被卸载，卸载磁盘组需要被删除")

    total_mb = Column(Integer, nullable=False, doc="该磁盘组整体的容量大小，单位MB")
    free_mb = Column(Integer, nullable=False, doc="该磁盘组剩余的容量大小，单位MB")
    usable_file_mb = Column(Integer, nullable=False, doc="坏盘后，磁盘组中满足冗余度之后，还有多少剩余空间可以使用，小于零时，恢复冗余会有风险，单位MB")

    offline_disks = Column(Integer, nullable=False, doc="磁盘组中离线的磁盘数量")

    is_rebalance = Column(Boolean, nullable=False, doc="磁盘组是否处于重平衡状态")
    rebalance_time_left_min = Column(Integer, nullable=False, default=0, doc="重平衡剩余时间，单位分钟")

    all_nodes = Column(JSON, nullable=False, doc="RAC中所有的计算节点列表，[node1_id, node2_id, node3_id]")
    mounted_nodes = Column(JSON, nullable=False, doc="挂载的计算节点列表，[node1_id, node2_id]")

    last_update_time = Column(DateTime, nullable=False, doc="该条数据最后一次的更新时间")
    last_fail_time = Column(DateTime, doc="该条数据最后一次刷新失败的时间")
    last_fail_msg = Column(String(length=1024), doc="该条数据最后一次刷新失败的异常原因")

    # 关联集群表
    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"), primary_key=True)
    cluster = relationship(QDataCluster, back_populates="disk_groups_info", lazy='subquery', doc="所关联的集群")

    # 磁盘组中的磁盘信息
    disks_info: List["HulkLogicalDisk"] = relationship("HulkLogicalDisk", back_populates="diskgroup",
                                                       cascade="all, delete-orphan", collection_class=set)

    __repr_columns__ = ["group_id", "name", "type", "mounted_nodes"]

    @property
    def is_last_refresh_success(self) -> bool:
        """最后这条数据是否刷新成功"""
        return self.last_update_time > self.last_fail_time if self.last_fail_time else True

    @property
    def predictive_disks(self) -> int:
        """预警磁盘数，按照磁盘中 media error > 0 或 predictive failure error > 0 来判断"""
        return len({disk.physical_disk_id for disk in self.disks_info if
                    disk.media_error > 0 or disk.predictive_failure_error > 0})

    @classmethod
    def get_obj_by_group_id_and_name(
        cls,
        session: Session,
        cluster_id: int,
        group_id: int,
        group_name: str,
    ) -> "HulkDiskGroup":
        """
        根据磁盘组id和名称，获取磁盘组对象，group id 在dismount时会改变，不能作为唯一依据
        :param session: 会话对象
        :param cluster_id: 磁盘组所在的集群id
        :param group_id: 磁盘组id
        :param group_name: 磁盘组名称
        :return: 存在返回磁盘组对象信息，失败返回None
        """
        return session.query(cls).filter_by(group_id=group_id, name=group_name, cluster_id=cluster_id).first()

    @classmethod
    def get_obj_by_group_name(cls, session: Session, cluster_id: int, group_name: str) -> "HulkDiskGroup":
        """
        根据磁盘组名称，获取磁盘组对象
        :param session: 会话对象
        :param cluster_id: 磁盘组所在的集群id
        :param group_name: 磁盘组id
        :return: 存在返回磁盘组对象信息，失败返回None
        """
        return session.query(cls).filter_by(name=group_name, cluster_id=cluster_id).first()


class HulkLogicalDisk(CloudEntity):
    """记录存储节点中的磁盘信息"""

    __tablename__ = "hulk_asm_logical_disk"

    disk_id = Column(Integer, primary_key=True, nullable=False, doc="磁盘所在的 v$asm_disk 表中的disk_number")
    name = Column(String(length=30), nullable=False, doc="磁盘所在的 v$asm_disk 表中的名称")
    fail_group = Column(String(length=30), nullable=False, doc="磁盘所属的故障组")
    mode_status = Column(String(length=7), nullable=False, doc="磁盘的状态，Online 或者 Offline")
    is_dropped = Column(Boolean, nullable=False, doc="逻辑磁盘是否掉线")

    com_path = Column(String(length=256), nullable=True, default="",
                      doc="计算节点磁盘所在的路径，/dev/qdata/mpath-s03.3261.01.P0B00S01p1")
    sto_path = Column(String(length=256), nullable=True, default="", doc="存储节点磁盘所在的路径，/dev/qdisk/P0B00S01p1")
    sto_real_path = Column(String(length=256), nullable=True, default="", doc="存储节点磁盘所在的绝对路径，/dev/sdd1")

    total_mb = Column(Integer, nullable=True, default=0, doc="该逻辑磁盘整体的容量大小，单位MB")
    free_mb = Column(Integer, nullable=True, default=0, doc="该逻辑磁盘剩余的容量大小，单位MB")

    # 关联的存储节点
    node_id = Column(Integer, ForeignKey(QDataNode.id, ondelete="CASCADE"), doc="磁盘所在存储节点的id")
    node = relationship(QDataNode, lazy='subquery', back_populates="logical_disks_info", doc="磁盘所关联的存储节点")

    # 关联的asm中的diskgroup表
    diskgroup_id = Column(Integer, ForeignKey(HulkDiskGroup.id, ondelete="CASCADE"))
    diskgroup = relationship(HulkDiskGroup, lazy='subquery', back_populates="disks_info", doc="磁盘所关联的磁盘组")

    # 关联的物理磁盘
    physical_disk_id = Column(Integer, ForeignKey("hulk_physical_disk.id", ondelete="CASCADE"))
    physical_disk: "HulkPhysicalDisk" = relationship("HulkPhysicalDisk", lazy='subquery',
                                                     back_populates="logical_disks", doc="磁盘所关联的磁盘组")

    __repr_columns__ = ["name", "fail_group", "mode_status", "com_path"]

    @property
    def media_error(self) -> int:
        return self.physical_disk.media_error if self.physical_disk else 0

    @property
    def predictive_failure_error(self) -> int:
        return self.physical_disk.predictive_failure_error if self.physical_disk else 0

    @property
    def other_error(self) -> int:
        return self.physical_disk.other_error if self.physical_disk else 0

    # @property
    # def qlink_target_id(self) -> int:
    #     """
    #     通过target_name获取对应的target_id，方法为查找最右侧的 '.' 符号，后续的数字为target_id
    #     s03.3263.01  ->  1
    #     """
    #     return int(self.qlink_target_name[self.qlink_target_name.rfind('.') + 1:])

    def get_qlink_info(self, session: Session) -> Optional["HulkQLink"]:
        if self.physical_disk:
            return HulkQLink.get_obj_by_lun_path(session=session, node_id=self.physical_disk.node_id,
                                                 lun_path=self.sto_path)
        else:
            return None

    @classmethod
    def get_failgroup_by_diskgroup_id(
        cls,
        session: Session,
        diskgroup_id: int,
    ) -> List[str]:
        """
        获取磁盘组下的所有failgroup名

        :param session: 会话对象
        :param diskgroup_id: 磁盘组在cloud数据库中的ID
        :return:
        """
        return [logical_disk_obj.fail_group for logical_disk_obj in cls.get_all(session=session, key="diskgroup_id", value=diskgroup_id)]

    # disk_id有可能变化，导致同一块盘出现两条数据
    # @classmethod
    # def get_obj_by_disk_id(
    #     cls,
    #     session: Session,
    #     node_id: int,
    #     diskgroup_id: int,
    #     physical_disk_id: int,
    #     disk_id: int
    # ) -> "HulkLogicalDisk":
    #     """
    #     根据逻辑磁盘在asm中的磁盘id获取逻辑磁盘对象
    #     :param session: 会话对象
    #     :param node_id: 逻辑磁盘所在的存储节点id
    #     :param diskgroup_id: 逻辑磁盘所在的磁盘组id
    #     :param physical_disk_id: 逻辑磁盘对应的物理磁盘id
    #     :param disk_id: 逻辑磁盘在asm中的磁盘id
    #     :return: 存在时返回逻辑磁盘对象id，不存在时返回None
    #     """
    #     return session.query(cls).filter_by(node_id=node_id,
    #                                         diskgroup_id=diskgroup_id,
    #                                         physical_disk_id=physical_disk_id,
    #                                         disk_id=disk_id).first()

    @classmethod
    def get_obj_by_com_path(
        cls,
        session: Session,
        node_id: int,
        diskgroup_id: int,
        physical_disk_id: int,
        fail_group: str,
        com_path: str
    ) -> "HulkLogicalDisk":
        """
        根据逻辑磁盘在asm中的磁盘id获取逻辑磁盘对象
        :param session: 会话对象
        :param node_id: 逻辑磁盘所在的存储节点id
        :param diskgroup_id: 逻辑磁盘所在的磁盘组id
        :param physical_disk_id: 逻辑磁盘对应的物理磁盘id
        :param fail_group: 磁盘对应的failgroup名称
        :param com_path: 磁盘对应的计算节点上的路径
        :return: 存在时返回逻辑磁盘对象id，不存在时返回None
        """
        return session.query(cls).filter_by(node_id=node_id,
                                            diskgroup_id=diskgroup_id,
                                            physical_disk_id=physical_disk_id,
                                            fail_group=fail_group,
                                            com_path=com_path).first()

    @classmethod
    def get_obj_by_disk_name(
        cls,
        session: Session,
        fail_group: str,
        disk_name: str
    ) -> "HulkLogicalDisk":
        """
        根据逻辑磁盘在asm中的磁盘id获取逻辑磁盘对象
        :param session: 会话对象
        :param fail_group: 磁盘对应的failgroup名称
        :param disk_name: 磁盘在ASM中的名称
        :return: 存在时返回逻辑磁盘对象id，不存在时返回None
        """
        return session.query(cls).filter_by(fail_group=fail_group,
                                            name=disk_name).first()


class HulkPhysicalDisk(CloudEntity):
    __tablename__ = "hulk_physical_disk"

    # 磁盘类型
    TYPE_PHYSICAL = "physical"  # 物理磁盘，未做其他操作
    TYPE_CACHE = "cache"  # 作为cache使用
    TYPE_QBO = "qbo"  # 作为qbo设备使用
    TYPE_VG = "VG"  # 作为vg中的pv使用
    disk_type_enum = CloudSqlAlchemyEnum(TYPE_PHYSICAL, TYPE_CACHE, TYPE_QBO, TYPE_VG)

    # 磁盘接口类型
    INTERFACE_SAS = "SAS"
    INTERFACE_SATA = "SATA"
    disk_interface_enum = CloudSqlAlchemyEnum(INTERFACE_SAS, INTERFACE_SATA)

    # 磁盘介质类型
    MEDIUM_HDD = "HDD"
    MEDIUM_SSD = "SSD"
    MEDIUM_NVME = "NVME"
    MEDIUM_FLASH = "FLASH"
    disk_medium_enum = CloudSqlAlchemyEnum(MEDIUM_HDD, MEDIUM_SSD, MEDIUM_NVME, MEDIUM_FLASH)

    # 磁盘换盘状态
    REPLACE_SUCCESS = "success"  # 换盘成功
    REPLACE_FAIL = "failed"  # 换盘失败
    REPLACE_REPLACE = "replace"  # 正在换盘
    REPLACE_WAITING = "waiting"  # 等待换盘
    REPLACE_CANCEL = "cancel"  # 取消换盘
    replace_status_enum = CloudSqlAlchemyEnum(REPLACE_SUCCESS, REPLACE_FAIL, REPLACE_REPLACE, REPLACE_WAITING,
                                              REPLACE_CANCEL)

    # 换盘界面展示状态
    REPLACE_VIEW_WAITING = REPLACE_WAITING
    REPLACE_VIEW_REPLACE = REPLACE_REPLACE
    REPLACE_VIEW_FAIL = REPLACE_FAIL
    REPLACE_VIEW_SUCCESS = REPLACE_SUCCESS
    replace_view_status_enum = CloudSqlAlchemyEnum(REPLACE_VIEW_WAITING, REPLACE_VIEW_REPLACE, REPLACE_VIEW_FAIL,
                                                   REPLACE_VIEW_SUCCESS)  # 换盘界面展示状态

    slot = Column(String(length=64), primary_key=True, nullable=False, doc="物理磁盘的slot号")
    real_path = Column(String(length=256), nullable=False, doc="物理磁盘真实路径")
    size_bytes = Column(BigInteger, nullable=False, doc="物理磁盘的大小，单位byte")

    disk_type = Column(disk_type_enum, default=TYPE_PHYSICAL, doc="物理磁盘加入存储协议的类型，physical/cache/qbo/vg")
    disk_interface = Column(disk_interface_enum, doc="物理磁盘的接口类型，SAS/SATA")
    disk_medium = Column(disk_medium_enum, doc="物理磁盘介质类型，hdd/sdd/nvme/flash")
    disk_is_online = Column(Boolean, default=True, doc="物理磁盘是否在线")

    media_error = Column(Integer, nullable=False, doc="磁盘的media error参数")
    predictive_failure_error = Column(Integer, nullable=False, doc="磁盘的 predictive failure error参数")
    other_error = Column(Integer, nullable=False, doc="磁盘的 other_error参数")

    allow_replace = Column(Boolean, default=True, doc="物理磁盘是否允许更换")
    replace_status = Column(replace_status_enum, default=REPLACE_WAITING, doc="物理磁盘换盘状态")
    replace_view_status = Column(replace_view_status_enum, default=REPLACE_VIEW_WAITING, doc="物理磁盘换盘状态，界面展示使用")

    node_id = Column(Integer, ForeignKey(QDataNode.id, ondelete="CASCADE"), doc="磁盘所在存储节点的id")
    node = relationship(QDataNode, lazy='subquery', back_populates="physical_disks_info", doc="磁盘所关联的存储节点")

    logical_disks: List[HulkLogicalDisk] = relationship(HulkLogicalDisk, back_populates="physical_disk",
                                                        cascade="all, delete-orphan", collection_class=set)
    replace_steps: List["HulkReplaceStep"] = relationship("HulkReplaceStep", back_populates="physical_disk",
                                                          cascade="all, delete-orphan", collection_class=set)

    __repr_columns__ = ["slot", "real_path", "disk_type", "disk_interface", "disk_medium"]

    # ------------------------- 属性 --------------------------
    @property
    def path(self) -> str:
        """
        返回磁盘所在的/dev/qdisk 目录下的路径
        老版本qdatamgr media show_nvme 中没有slot字段，使用真实路径代替
        """
        return os.path.join("/dev/qdisk/", self.slot) if self.slot != self.real_path else self.slot

    @property
    def raid_info(self) -> RaidInfoModel:
        """返回物理磁盘的raid卡下的信息"""
        return RaidInfoModel(**self.get_attr("raid", dict()))

    # model中不允许这种赋值方式
    # @raid.setter
    def set_raid_info(self, raid_info: RaidInfoModel) -> None:
        """
        设置raid卡类型磁盘的硬件属性
        :param raid_info: 磁盘在raid卡上的相关信息，包括raid_level、WWN、inquiry_data
        """
        self.set_attr(key="raid", value=raid_info.dict())

    @property
    def nvme_info(self) -> NvmeInfoModel:
        """返回nvme磁盘的特殊信息"""
        return NvmeInfoModel(**self.get_attr("nvme", dict()))

    def set_nvme_info(self, nvme_info: NvmeInfoModel) -> None:
        """
        设置nvme磁盘的特殊信息
        :param nvme_info: nvme磁盘的特殊信息
        """
        self.set_attr(key="nvme", value=nvme_info.dict())

    @property
    def flash_info(self) -> FlashInfoModel:
        """返回flash磁盘的特殊信息"""
        return FlashInfoModel(**self.get_attr("flash", dict()))

    def set_flash_info(self, flash_info: FlashInfoModel) -> None:
        """
        设置flash磁盘的特殊信息
        :param flash_info: flash磁盘的特殊信息
        """
        self.set_attr(key="flash", value=flash_info.dict())

    @property
    def parts_info(self) -> List[PartInfoModel]:
        """返回分区信息列表"""
        return [PartInfoModel(**p) for p in self.get_attr("parts", list())]

    def set_parts_info(self, part_info_list: List[PartInfoModel]) -> None:
        """
        设置分区信息列表
        :param part_info_list: 待存储的分区信息
        :return:
        """
        self.set_attr(key="parts", value=[p.dict() for p in part_info_list])

    @property
    def size_str(self) -> str:
        return convert_to_size_str(size_num=self.size_bytes)

    # ------------------------- 根据条件获取对象 --------------------------
    @classmethod
    def get_obj_by_slot(cls, session: Session, node_id: int, slot: str) -> Optional["HulkPhysicalDisk"]:
        """
        通过真实路径获取物理磁盘对象
        :param session: 会话
        :param node_id: 节点id
        :param slot: 物理磁盘slot号
        :return: 存在返回物理磁盘对象，不存在返回None
        """
        return session.query(cls).filter_by(node_id=node_id, slot=slot).first()

    @classmethod
    def get_obj_by_real_path(cls, session: Session, node_id: int, real_path: str) -> Optional["HulkPhysicalDisk"]:
        """
        通过真实路径获取物理磁盘对象
        :param session: 会话
        :param node_id: 节点id
        :param real_path: 物理磁盘的绝对路径
        :return: 存在返回物理磁盘对象，不存在返回None
        """
        return session.query(cls).filter_by(node_id=node_id, real_path=real_path).first()


class HulkReplaceStep(CloudEntity):
    __doc__ = "智能换盘步骤存储表"
    __tablename__ = "hulk_replace_disk_step"

    STEP_STATUS_PENDING = "Pending"
    STEP_STATUS_CANCEL = STEP_STATUS_PENDING
    STEP_STATUS_SKIPPED = "Skipped"
    STEP_STATUS_IN_PROGRESS = "In Progress"
    STEP_STATUS_SUCCESS = "Success"
    STEP_STATUS_FAILED = "Failed"
    step_status_enum = CloudSqlAlchemyEnum(STEP_STATUS_PENDING, STEP_STATUS_SKIPPED, STEP_STATUS_IN_PROGRESS,
                                           STEP_STATUS_SUCCESS, STEP_STATUS_FAILED)

    WS_TYPE_REQUEST = "Request"
    WS_TYPE_RESPONSE = "Response"
    ws_type_enum = CloudSqlAlchemyEnum(WS_TYPE_REQUEST, WS_TYPE_RESPONSE)

    step_id = Column(Integer, primary_key=True, doc="换盘步骤编号")
    step_uuid = Column(String(256), default="", nullable=True, doc="换盘步骤uuid，用于标识步骤中的小步骤")
    step_title = Column(String(256), default="", nullable=True, doc="换盘步骤标题，默认使用步骤对象中的标题，特殊步骤使用数据库中的标题")
    status = Column(step_status_enum, nullable=False, doc="该步骤状态")
    description = Column(LONGTEXT, default="", nullable=True, doc="换盘进度描述")
    error_msg = Column(LONGTEXT, default="", nullable=True, doc="展示换盘步骤的错误信息")
    ws_type = Column(ws_type_enum, default=WS_TYPE_RESPONSE, nullable=False, doc="换盘进度返回给前端的消息类型")

    physical_disk_id = Column(Integer, ForeignKey(HulkPhysicalDisk.id, ondelete="CASCADE"), primary_key=True,
                              doc="换盘操作对应的物理磁盘id")
    physical_disk = relationship(HulkPhysicalDisk, lazy='subquery', back_populates="replace_steps", doc="换盘操作对应的物理磁盘")

    __repr_columns__ = ["step_id", "status", "physical_disk_id"]

    @classmethod
    def get_obj_by_flag(
        cls,
        session: Session,
        node_id: int,
        physical_disk_slot: str,
        step_id: Optional[int] = None
    ) -> Union["HulkReplaceStep", List["HulkReplaceStep"], None]:
        """
        通过特征，找到对应磁盘的步骤对象
        :param session: 会话
        :param node_id: 节点id
        :param physical_disk_slot: 物理磁盘slot号
        :param step_id: 换盘步骤id，未设置时返回物理磁盘所有的步骤信息
        :return: 存在返回步骤对象，不存在返回None
        """
        if (physical_disk_obj := HulkPhysicalDisk.get_obj_by_slot(session=session,
                                                                  node_id=node_id,
                                                                  slot=physical_disk_slot)) is None:
            return None

        if step_id is not None:
            return session.query(cls).filter_by(physical_disk_id=physical_disk_obj.id, step_id=int(step_id)).first()
        else:
            return session.query(cls).filter_by(physical_disk_id=physical_disk_obj.id).all()


# ------------------------------------------- rac集群 ---------------------------------------
def set_auto_increment_value(session: Session, value: Any) -> None:
    session.execute("ALTER TABLE qdata_node AUTO_INCREMENT = :value", {'value': value})


class RacCluster(CloudEntity):
    __tablename__ = "rac_cluster"

    TYPE = "cloud"
    TYPE_NAME = {
        "cloud": u"计算资源池"
    }

    attr = Column(JSON, default={},
                  doc="creator(创建者信息)/grid_user,gi_home,grid_version/oracle_user,oracle_home/database_version/cluster_scan_ip(rac的scanip信息，支持多个scan)")
    name = Column(String(length=128), nullable=False, doc="集群名字")
    alias_name = Column(String(length=128), nullable=False, doc="集群别名")
    support_cdb = Column(Boolean, nullable=False, doc="集群是否支持容器数据库的创建")

    cluster_id = Column(Integer, ForeignKey(QDataCluster.id, ondelete="CASCADE"))
    cluster: QDataCluster = relationship(QDataCluster, back_populates="rac_clusters", lazy='subquery', uselist=False,
                                         doc="所关联的qdata集群")

    # 一个rac集群下有多个nodes/databases/pools/database_templates
    nodes: Set["QDataNode"] = relationship("QDataNode", back_populates="rac_cluster", cascade="all, none",
                                           order_by='QDataNode.name',
                                           collection_class=set)  # 当删除rac集群时，不对其关联的计算节点进行级联操作，因为计算节点是属于qdata集群的资源
    databases: Set["RacDatabase"] = relationship("RacDatabase", back_populates="rac_cluster",
                                                 cascade="all, delete-orphan", order_by='RacDatabase.name',
                                                 collection_class=set)
    pools: Set["RacSrvPool"] = relationship("RacSrvPool", back_populates="rac_cluster", cascade="all, delete-orphan",
                                            collection_class=set)
    database_templates: Set["RacDatabaseTemplate"] = relationship("RacDatabaseTemplate", back_populates="rac_cluster",
                                                                  cascade="save-update,merge", collection_class=set)

    def connect_info(self) -> List[Dict[str, Any]]:
        """
        连接信息
        """
        return self.attr.get("cluster_scan_ip", [])

    def basic_info(self) -> Dict[str, Any]:
        """
        获取rac集群的基本信息
        """
        asm_pass = self.attr.get('asm_pass', '')
        if asm_pass:
            asm_pass = decrypt_string(asm_pass)
        return dict(
            grid_home=self.attr.get('gi_home', ''),  # 兼容以前的字段
            grid_user=self.attr.get('grid_user', ''),
            grid_version=self.attr.get('grid_version', ''),
            oracle_user=self.attr.get('oracle_user', ''),
            oracle_home=self.attr.get('oracle_home', ''),
            database_version=self.attr.get('database_version', ''),
            asm_user=self.attr.get('asm_user', ''),
            asm_pass=asm_pass,
            cluster_scan_ip=self.attr.get('cluster_scan_ip', []),
            scan_port=self.connect_info()[0].get("scan_port"),
            node_count=len(self.nodes)
        )


class RacDatabase(CloudEntity):
    __tablename__ = "rac_database"

    attr = Column(JSON, default={},
                  doc="port(监听端口，每一个db都可能有自己独有的port)/o_user/o_pass/service_name/pool_ids/lifecycle/connect_method(连接方式)")
    name = Column(String(length=100), nullable=False, doc="数据库唯一名字")
    type = Column(String(length=20), nullable=False, doc="数据库类型, 1:Rac One Node, 2:Rac")  # todo @马克鸣 增加枚举
    create_type = Column(String(length=100), doc="数据库创建类型: DBCA,APP")  # todo @马克鸣 增加枚举
    create_status = Column(String(length=100), nullable=True, doc="数据库创建状态: creating, done")  # todo @马克鸣 增加枚举
    role = Column(String(length=20), nullable=True, doc="数据库角色, 1:primary, 2:standby")  # todo @马克鸣 增加枚举
    managed = Column(String(length=20), nullable=False, doc="策略, 1:admin, 2:policy")  # todo @马克鸣 增加枚举
    version = Column(String(length=100), default="", doc="数据库版本")
    is_container = Column(Boolean, default=None, doc="是否是容器数据库")
    description = Column(String(length=200), doc="备注信息")
    user_name = Column(String(length=20), doc="关联的用户")

    # cluster, 一个cluster对应多个database
    rac_cluster_id = Column(Integer, ForeignKey(RacCluster.id, ondelete='CASCADE'), doc="集群id")
    rac_cluster: RacCluster = relationship(RacCluster, back_populates="databases", uselist=False, doc="关联的集群")

    # 一个database下有多个instances/containers/role_transition_notifications
    instances: Set["RacInstance"] = relationship("RacInstance", back_populates="database", cascade="all, delete-orphan",
                                                 collection_class=set, order_by="RacInstance.name")
    containers: Set["RacContainer"] = relationship("RacContainer", back_populates="database",
                                                   cascade="all, delete-orphan", collection_class=set,
                                                   order_by="RacContainer.name")
    role_transition_notifications: Set["DatabaseRoleTransitionNotification"] = relationship(
        "DatabaseRoleTransitionNotification", back_populates="database", cascade="all, delete-orphan",
        collection_class=set,
        order_by="desc(DatabaseRoleTransitionNotification.create_time)")

    def to_dict(self) -> Dict[str, Any]:
        dict_format_data = {}
        for column in inspect(RacDatabase).c:
            name = column.name
            value = getattr(self, name)
            dict_format_data[name] = value
        dict_format_data.pop('attr')
        dict_format_data.pop('create_type')
        dict_format_data['o_user'] = self.attr['o_user']
        dict_format_data['o_pass'] = decrypt_string(self.attr['o_pass'])
        session = inspect(self).session
        pools = session.query(RacSrvPool).filter(RacSrvPool.id.in_(self.attr['pool_ids']))
        dict_format_data['pool_name'] = ','.join([pool.pool_name for pool in pools])
        return dict_format_data


class RacInstance(CloudEntity):
    __tablename__ = "rac_instance"

    TYPE = 'cloud_instance'
    TYPE_NAME = {TYPE: u'oracle实例'}

    attr = Column(JSON, default={}, doc="connected(连通性)/alert_path(告警日志路径)/db_inst_stat(实例状态)")
    name = Column(String(length=100), nullable=False, doc="实例名字")
    host_name = Column(String(length=100), nullable=False, doc="主机节点名")
    status = Column(String(length=20), doc="实例状态, running, down, starting, stopping")  # todo @马克鸣 增加枚举
    monitor_state = Column(String(length=20), doc="实例监控状态, True, False, running")  # todo @马克鸣 增加枚举
    monitoring_container_list = Column(JSON, default=[], doc="正在实时监控的容器列表")

    # database, 一个database对应多个instance
    database_id = Column(Integer, ForeignKey(RacDatabase.id, ondelete='CASCADE'), doc="db表的id")
    database: RacDatabase = relationship(RacDatabase, back_populates="instances", uselist=False, doc="关联的数据库")

    # node, 一个instance对应对应一个node，删除节点时，其上实例跟随删除
    node_id = Column(Integer, ForeignKey(QDataNode.id, ondelete='CASCADE'), doc="QDataNode表的id")
    node: QDataNode = relationship(QDataNode, back_populates="instances", uselist=False, doc="关联的数据库")

    def to_dict(self) -> Dict[str, Any]:
        instance = {
            "id": self.id,
            "name": self.name,
            "hostname": self.host_name,
            "status": self.status,
            "monitor_state": self.monitor_state,
            **self.attr,
        }
        return instance


class RacContainer(CloudEntity):
    __tablename__ = "rac_container"

    TYPE = 'cloud_container'
    TYPE_NAME = {TYPE: u'容器'}

    name = Column(String(length=100), nullable=False, doc="容器名称")
    container_id = Column(Integer, nullable=False, doc="容器ID")
    container_uid = Column(BigInteger, nullable=False, doc="容器unique ID")
    is_root_container = Column(Boolean, nullable=False, doc="是否是根容器")

    # database, 一个database对应多个container
    database_id = Column(Integer, ForeignKey(RacDatabase.id, ondelete='CASCADE'), doc="instance表的id")
    database: RacDatabase = relationship(RacDatabase, back_populates='containers', doc="关联的数据库", uselist=False)

    def merge(self, session: Session) -> None:
        try:
            con = session.query(RacContainer).filter_by(name=self.name, database_id=self.database_id).one()
        except NoResultFound:
            session.merge(self)
        else:
            self.id = con.id
            session.merge(self)


class RacSrvPool(CloudEntity):
    """db资源池，对应oralce的servers pool"""
    __tablename__ = "rac_srv_pool"

    attr = Column(JSON, default={}, doc="imp(重要度)/max｜min(serverpool中运行服务器的最大｜小数量)/active_hosts(pool中主机)")
    pool_name = Column(String(length=100), nullable=False, doc="DBPool名称")

    rac_cluster_id = Column(Integer, ForeignKey(RacCluster.id, ondelete='CASCADE'), nullable=False, doc="rac集群id")
    rac_cluster: RacCluster = relationship(RacCluster, back_populates="pools", doc="关联的集群", uselist=False)

    # database_templates，一个资源池对应多个database_template
    database_templates: Set["RacDatabaseTemplate"] = relationship("RacDatabaseTemplate", back_populates="pool",
                                                                  cascade="save-update,merge", collection_class=set)


class RacParameterTemplate(CloudEntity):
    """参数模版，参数模板包含了数据库参数的配置信息"""
    __tablename__ = "rac_parameter_template"

    template_name = Column(String(length=100), nullable=False, unique=True, doc="模版名")
    description = Column(String(length=200), doc="备注信息")
    template_type = Column(String(length=100), doc="模板类型: 示例模板，默认模板，用户模板")  # todo @马克鸣 增加枚举
    parameter = Column(Text(), doc="模板参数")

    # database_templates，一个参数模板对应多个database_template
    database_templates: Set["RacDatabaseTemplate"] = relationship("RacDatabaseTemplate", back_populates="parameter",
                                                                  cascade="save-update,merge", collection_class=set)


class RacDatabaseTemplate(CloudEntity):
    """创建数据库模版，基于rac集群，一套rac下有多个数据库模版"""
    __tablename__ = "rac_database_template"

    template_name = Column(String(length=100), nullable=False, unique=True, doc="模版名")
    rac_type = Column(String(length=20), nullable=False, doc="rac类型: RAC or RACOneNode")  # todo @马克鸣 增加枚举
    managed_type = Column(String(length=20), nullable=False, doc="管理类型, admin, policy")  # todo @马克鸣 增加枚举
    resource_allocation = Column(JSON, doc="资源分配", nullable=False)
    basic_information = Column(JSON, nullable=False, doc="基本信息")
    storage = Column(JSON, doc="数据库存储信息", nullable=False)
    log_mode = Column(String(length=24), doc="归档模式", nullable=False)  # todo @马克鸣 增加枚举
    description = Column(String(1024), doc="备注")
    monitor_user = Column(String(length=100), nullable=False, doc="监控用户")
    monitor_password = Column(String(length=100), nullable=False, doc="监控用户密码")
    script_name = Column(String(length=100), doc="脚本名称")
    node_list = Column(JSON, doc="节点列表")
    is_cdb = Column(Boolean, doc="是否是容器", nullable=True)
    cdb_config = Column(JSON, doc="cdb配置信息")

    # cluster, 一个集群下有多个database_templates
    rac_cluster_id = Column(Integer, ForeignKey(RacCluster.id, ondelete='SET NULL'), doc="集群id")
    rac_cluster: RacCluster = relationship(RacCluster, back_populates="database_templates", doc="关联的集群", uselist=False)

    # parameter，一个参数模板下有多个database_templates
    parameter_id = Column(Integer, ForeignKey(RacParameterTemplate.id, ondelete='SET NULL'), doc="参数模板id")
    parameter: RacParameterTemplate = relationship(RacParameterTemplate, back_populates="database_templates",
                                                   doc="关联的参数模板", uselist=False)

    # pool一个资源池下有多个database_templates
    pool_id = Column(Integer, ForeignKey(RacSrvPool.id, ondelete='SET NULL'), doc="pool id")
    pool: RacSrvPool = relationship(RacSrvPool, back_populates="database_templates", doc="关联的资源池", uselist=False)


class RacMonitorLog(CloudEntity):
    """保存用户设置的日志监控路径"""

    __tablename__: str = "rac_monitor_log"
    __table_args__: Union[Dict[str, Any], Tuple[Any]] = (  # type: ignore
        # 联合索引，node_id&path保证单个主机针对同一path只有一条配置
        # Ref: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/table_config.html#declarative-table-args
        Index('node_path_unique', 'node_id', 'path', unique=True),
        CloudEntity.__table_args__
    )

    name = Column(String(length=100), nullable=True, doc="名称")
    path = Column(String(length=200), nullable=False, doc="日志路径")
    description = Column(String(length=200), doc="备注信息")

    # node，一个节点下有多个日志监控路径
    node_id = Column(Integer, ForeignKey(QDataNode.id, ondelete='CASCADE'), doc="主机id")
    node: QDataNode = relationship(QDataNode, back_populates="monitor_log_paths", doc="关联的节点", uselist=False)


class DatabaseRoleTransitionNotification(CloudEntity):
    __tablename__ = "rac_database_role_transition_notification"

    notified = Column(Boolean, nullable=False, doc="是否被通知")
    content = Column(String(length=1024), doc="通知内容", nullable=False)

    # database，一个数据库下有多个角色关联
    database_id = Column(Integer, ForeignKey(RacDatabase.id, ondelete='CASCADE'), doc="数据库ID", nullable=False)
    database: Set["RacDatabase"] = relationship(RacDatabase, back_populates="role_transition_notifications",
                                                doc="关联的数据库", collection_class=set)


# ==================== 租户系统 ==========================


class PdbSpec(CloudEntity):
    """
    pdb预置规格
    """
    __tablename__ = "pdb_spec"

    TYPE_ENABLED = "enabled"  # 开启
    TYPE_DISABLED = "disabled"  # 关闭
    status_enum = CloudSqlAlchemyEnum(TYPE_ENABLED, TYPE_DISABLED)

    TYPE_GROUP_STANDARD = "standard"
    TYPE_GROUP_PERFORMANCE = "performance"
    spec_group_enum = CloudSqlAlchemyEnum(TYPE_GROUP_STANDARD, TYPE_GROUP_PERFORMANCE)

    TYPE_VOLUME_NORMAL = "vg"  # 标准存储
    TYPE_VOLUME_ARCHIVE = "vcg"  # 归档/容量存储
    TYPE_VOLUME_PERFORMANCE = "vpg"  # 高性能/SSD存储
    volume_type_enum = CloudSqlAlchemyEnum(TYPE_VOLUME_NORMAL, TYPE_VOLUME_ARCHIVE, TYPE_VOLUME_PERFORMANCE)

    name = Column(String(length=36), nullable=False, doc="规格名,中文")
    alias_name = Column(String(length=36), nullable=False, doc="规格名，英文简写")
    description = Column(String(255), default="", doc="规格说明")

    group = Column(spec_group_enum, default=TYPE_GROUP_STANDARD, doc="规格组")

    cpu = Column(Integer, default=0, doc="cpu核心数，单位:核心数")
    memory = Column(Integer, default=0, doc="内存容量，单位：GB")

    volume_type = Column(volume_type_enum, default=TYPE_VOLUME_NORMAL, doc="存储类型，默认标准存储")
    iops = Column(Integer, default=0, doc="每秒的输入输出量/读写次数/IO请求数量，单位：次")

    day_price = Column(Integer, default=0, doc="规格对应的单价，单位：元/日")

    status = Column(status_enum, default=TYPE_ENABLED, doc="该配置项的开关，可以在数据库中关闭该规格")

    def format_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "alias_name": self.alias_name,
            "description": self.description,
            "group": self.group,
            "cpu": self.cpu,
            "memory": self.memory,
            "volume_type": self.volume_type,
            "iops": self.iops,
            "day_price": self.day_price,
            "status": self.status
        }


class RootContainer(CloudEntity):
    """
    pdb的根容器表
    CDB的引用
    """
    __tablename__ = "root_container"

    alias_name = Column(String(length=36), unique=True, nullable=False, doc="根容器别名")
    description = Column(String(255), default="", doc="说明")

    cdb_id = Column(Integer, ForeignKey(RacDatabase.id, ondelete="CASCADE"), nullable=False, doc="cdb的id")
    database: RacDatabase = relationship(RacDatabase, lazy='subquery', uselist=False, doc="所关联的database，此处的必须是CDB")

    pdbs: Set["Pdb"] = relationship("Pdb", backref="pdb", doc="根容器所属pdb列表")

    password_for_sys = Column(String(255), nullable=True, doc="sys用户,具有sysdba角色的sys用户的密码，该用户可以创建数据库,需要aes存储")

    # 创建资源池时会自动生成总配额，该配额为该资源池配额的最大值
    cpu = Column(Integer, default=0, doc="cpu核心数，单位:核心数")
    memory = Column(Integer, default=0, doc="内存容量，单位：GB")
    volume = Column(Integer, default=0, doc="物理存储容量，单位：GB")

    def format_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "cdb_id": self.cdb_id,
            "alias_name": self.alias_name,
            "cpu": self.cpu,
            "memory": self.memory,
            "volume": self.memory,
        }


class RootContainerSpec(CloudEntity):
    """
    挂在root_container即cdb上的规格
    """
    __tablename__ = "root_container_spec"

    pdb_spec_id = Column(Integer, ForeignKey(PdbSpec.id, ondelete="CASCADE"), nullable=False, doc="pdb_spec的id")
    root_container_id = Column(Integer, ForeignKey(RootContainer.id, ondelete="CASCADE"), nullable=False,
                               doc="root_container的id")


class Tenant(CloudEntity):
    """
    租户表
    当前对租户概念的使用，仅限于配额组的层面，和pm确认过，不会有真正的租户的概念
    """
    __tablename__ = "tenant"

    # 外部租户id可能为uuid/guid，因此租户id设置为非int
    id = Column(String(length=36), primary_key=True, nullable=False, doc="租户id")
    name = Column(String(length=36), nullable=False, doc="租户名")
    organization_name = Column(String(255), default="", doc="组织名，可适配概念：公司名/部门名")
    description = Column(String(255), default="", doc="租户说明")

    def format_data(self) -> Dict[str, Any]:
        return {
            "uuid": self.id,
            "name": self.name,
            "organization_name": self.organization_name,
            "description": self.description
        }


class TenantQuote(CloudEntity):
    """
    租户配额表
    一个租户有多条配额，即将自己的总配额分散在多个资源之上
    """
    __tablename__ = "tenant_quote"

    tenant_id = Column(String(length=36), ForeignKey(Tenant.id, ondelete="CASCADE"), nullable=False, doc="tenant的id")
    root_container_id = Column(Integer, ForeignKey(RootContainer.id, ondelete="CASCADE"), nullable=False,
                               doc="root_container的id")

    cpu = Column(Integer, default=0, doc="cpu核心数，单位:核心数")
    memory = Column(Integer, default=0, doc="内存容量，单位：GB")
    volume = Column(Integer, default=0, doc="物理存储容量，单位：GB")

    def format_data(self) -> Dict[str, Any]:
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "volume": self.volume
        }


class User(CloudEntity):
    """
    用户表
    PM确认为了简化成本和复杂度，以及长期不会有真正的租户的概念，租户只是当作资源组/配额组的实际概念来使用，因此只实现一套用户系统
    """
    __tablename__ = "auth_user"

    id = Column(String(length=36), primary_key=True, nullable=False,
                doc="用户id，可能和外部系统同步，因此考虑需要兼容uuid/guid")  # 36个字符 - 32个十六进制数字+4个破折号
    name = Column(String(length=100), nullable=False, unique=True, doc="账户名，用来登陆，并且具有唯一性，在全局具有唯一性")
    password = Column(String(length=100), nullable=False)

    # 更丰富的用户属性，非必选属性
    nickname = Column(String(length=100), default="", doc="用户昵称/别名/姓名，用来进行展示通知时候使用，可任意重复")
    avatar = Column(String(length=255), default="", doc="用户头像，预留字段")
    description = Column(String(length=255), default="", doc="用户描述")

    email = Column(String(100))
    wechat = Column(String(100))
    mobile = Column(String(length=12))

    @classmethod
    def get_auth_user(cls, session: Session, name: str, password: bytes) -> Optional["User"]:
        """
        验证用户名、密码是否对应
        :param session: 会话对象
        :param name: 用户名
        :param password: 密码
        :return: 成功返回用户对象，失败返回空
        """
        try:
            if user := session.query(cls).filter_by(name=name).first():
                if user.password == cls.encrypt(password):
                    return user
            return None
        except Exception as e:
            logger.error(f"auth {name} password {password.decode()} error -> {e}")
            return None

    @classmethod
    def encrypt(cls, password: bytes) -> str:
        return md5sum(password)

    @property
    def detail(self) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email if self.email else "",
            "mobile": self.mobile if self.mobile else "",
            "wechat": self.mobile if self.wechat else "",
            "create_time": convert_utc_to_beijing(self.create_time),
            "update_time": convert_utc_to_beijing(self.update_time),
        }
        return data


class TenantUserRole(CloudEntity):
    """租户用户角色关联表"""
    __tablename__ = "tenant_user_role"

    user_id = Column(String(length=36), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, doc="user的id")
    tenant_id = Column(String(length=36), nullable=True, doc="tenant的id,当没有tenant_id的时候，则为后台用户，因此不与tenant形成键关系")
    role_id = Column(String(length=36), nullable=False, doc="role的id,非外键,id来自于外部权限控制系统，因此不与role表形成键关系")


class UserGroup(CloudEntity):
    """用户组用户对应关系表"""
    __tablename__ = "auth_user_group"

    user_id = Column(String(length=36), nullable=False)
    group_id = Column(Integer, nullable=False)


class Pdb(CloudEntity):
    """
    pdb
    创建数据库的时候，dg直接现查
    """
    __tablename__ = "pdb"
    # uuid的生成方法使用uuid.uuid5(uuid.NAMESPACE_DNS, f"{root_container_obj.alias_name}-{self.pdb_name}")
    uuid = Column(String(length=36), unique=True, nullable=False, doc="pdb的uuid")

    root_container_id = Column(Integer, ForeignKey(RootContainer.id, ondelete="CASCADE"), nullable=False,
                               doc="pdb的根容器的id")
    rac_container_id = Column(Integer, ForeignKey(RacContainer.id, ondelete="CASCADE"), nullable=False,
                              doc="真实container的id")
    tenant_id = Column(String(length=36), ForeignKey(Tenant.id, ondelete="CASCADE"), nullable=False, doc="tenant的id")
    user_id = Column(String(length=36), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, doc="创建者的id")

    name = Column(String(length=36), nullable=False, unique=True, doc="数据库名")
    description = Column(String(255), default="", doc="数据库说明")

    cpu = Column(Integer, default=0, doc="cpu核心数，单位:核心数")
    memory = Column(Integer, default=0, doc="内存容量，单位：GB")
    volume = Column(Integer, default=0, doc="物理存储容量，单位：GB")

    def format_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "attr": self.attr,
            "uuid": self.uuid,
            "name": self.name,
            "root_container_id": self.root_container_id,
            "cpu": self.cpu,
            "memory": self.memory,
            "volume": self.volume,
            "create_time": convert_utc_to_beijing(self.create_time)
        }

    @classmethod
    def used_resource(cls, session: Session, key: Optional[str] = None, value: Any = None) -> Dict[str, int]:
        """
        某个根容器下PDB中cpu、memory和volume各自之和
        """
        if key:
            used_cpu = session.query(func.sum(cls.cpu)).filter(getattr(cls, key) == value).scalar()
            used_memory = session.query(func.sum(cls.memory)).filter(getattr(cls, key) == value).scalar()
            used_volume = session.query(func.sum(cls.volume)).filter(getattr(cls, key) == value).scalar()
        else:
            used_cpu = session.query(func.sum(cls.cpu)).scalar()
            used_memory = session.query(func.sum(cls.memory)).scalar()
            used_volume = session.query(func.sum(cls.volume)).scalar()
        return {
            "used_cpu": used_cpu,
            "used_memory": used_memory,
            "used_volume": used_volume
        }


class PdbAlert(CloudEntity):
    """
    pdbAlert
    关联实时告警，由于告警中心，实时告警/历史告警的表的结构复杂，并且容易发生变化，因此通过关联来解决
    业务场景是：
    私有云对接程序，通过读取未发送的告警，发送到云端
    后期告警中心重构后，计划废弃历史告警，将实时告警和历史告警，使用该表，可以直接关联告警表，实现前后台界面逻辑控制的完全隔离

    好处：
    - 多存导致数据不一致的问题
    - 将发送的业务逻辑融合在内，避免污染原始告警历史表
    """
    __tablename__ = "pdb_alert"

    TYPE_NOT_SEND = "NotSend"  # 未发送
    TYPE_ALREADY_SENT = "AlreadySent"  # 已发送
    send_status_enum = CloudSqlAlchemyEnum(TYPE_NOT_SEND, TYPE_ALREADY_SENT)

    pdb_uuid = Column(String(length=36), ForeignKey(Pdb.uuid, ondelete="CASCADE"), nullable=False,
                      doc="pdb的id，可以通过pdb_id查到该pdb的创建人及其租户")
    alert_uuid = Column(String(length=36), nullable=False, doc="alert_list/alert_log的uuid")

    send_status = Column(send_status_enum, nullable=False, default=TYPE_NOT_SEND, doc="告警发送状态")
    sent_times = Column(Integer, default=0, doc="尝试发送告警次数，照顾一定次数则放弃")
    alert_status = Column(Boolean, default=False, doc="告警是否解决,True/1: 已解决, False/0: 未解决")


class PdbOperateLog(CloudEntity):
    """
    pdb操作日志
    """
    __tablename__ = "pdb_operate_log"

    STATE_CREATED = "created"  # 已创建
    STATE_SCALED = "scaled"  # 已扩容
    STATE_REMOVED = "removed"  # 已删除
    pdb_operate_type_enum = CloudSqlAlchemyEnum(STATE_CREATED, STATE_SCALED, STATE_REMOVED)

    STATE_REPORTED = "reported"  # 已上报
    STATE_NOT_REPORT = "not_report"  # 未上报
    report_status_enum = CloudSqlAlchemyEnum(STATE_REPORTED, STATE_NOT_REPORT)

    operate_type = Column(pdb_operate_type_enum, nullable=False, doc="pdb在创建/扩容/删除时候的标记，提供给thor进程来对接私有云")
    report_status = Column(report_status_enum, nullable=False, default=STATE_NOT_REPORT,
                           doc="pdb在创建/扩容/删除时候的标记，提供给thor进程来对接私有云")
    pdb_uuid = Column(String(36), nullable=False, doc="pdb的uuid")
    pdb_name = Column(String(36), nullable=False, doc="pdb的名称")
    root_container_id = Column(Integer, nullable=False, doc="pdb的根容器cdb的id")
    rac_container_id = Column(Integer, nullable=False, doc="真实container的id")
    tenant_id = Column(String(length=36), ForeignKey(Tenant.id, ondelete="CASCADE"), nullable=False, doc="tenant的id")
    user_id = Column(String(length=36), ForeignKey(User.id, ondelete="CASCADE"), nullable=False, doc="创建者的id")

    cpu = Column(Integer, default=0, doc="cpu核心数，单位:核心数，创建/扩容/删除的cpu数量")
    memory = Column(Integer, default=0, doc="内存容量，单位：GB，创建/扩容/删除的内存容量")
    volume = Column(Integer, default=0, doc="物理存储容量，单位：GB，创建/扩容/删除的存储大小")


# ==================== auth相关表结果 ==========================


class Group(CloudEntity):
    """
    用户组
    """
    __tablename__ = "auth_group"

    name = Column(String(length=100), nullable=False, unique=True)
    desc = Column(String(length=100), nullable=True)

    # 关联alert_channel表
    # auth_channels: Set["AlertChannel"] = relationship("AlertChannel", back_populates="groups",
    #                                                   cascade="all, delete-orphan", collection_class=set)

    # @property
    # def detail(self):
    #     data = {
    #         "id": self.id,
    #         "name": self.name,
    #         "desc": self.desc,
    #         "create_time": format_time(self.create_time),
    #         "update_time": format_time(self.update_time) if self.update_time else "",
    #     }
    #     return data


# ==================== audit相关表结果 ==========================

class AuditAlertModel(CloudEntity):
    """"""
    __tablename__ = "audit_alert"

    cmd_id = Column(Integer, doc="命令ID")
    cmd_name = Column(String(length=255), doc="命令描述")
    category = Column(JSON, default={}, doc="审计分类")
    ip = Column(String(length=255), doc="操作人IP")
    name = Column(String(length=255), doc="操作人名称")
    cluster_id = Column(Integer, doc="集群ID")
    confirmed = Column(Float, doc="应用变更")
    device_hostname = Column(String(length=255), doc="设备信息")
    device_ip = Column(String(length=255), doc="设备信息")
    device_id = Column(Integer, doc="设备信息")
    device_type = Column(String(length=255), doc="设备信息")
    alert_times = Column(Float, doc="告警次数")
    send_times = Column(Float, doc="发送次数")
    old_value = Column(String(length=255), doc="旧告警项值")
    new_value = Column(String(length=255), doc="新告警项值")
    index = Column(Integer, doc="不同的采集index")


class AuditLogModel(CloudEntity):
    """"""
    __tablename__ = "audit_log"

    # colums
    details = Column(JSON, default={}, doc="日志详情")
    event = Column(String(length=500), doc="描述事件类别")
    execute_result = Column(String(length=255), doc="执行结果")
    user = Column(String(length=255), doc="执行用户")
    ip = Column(String(length=255), doc="操作人IP")
    cluster_id = Column(Integer, doc="集群ID")


class AuditTargerModel(CloudEntity):
    """"""
    __tablename__ = "audit_target_model"

    collect_frequency = Column(Integer, doc="采集频率")
    notice_interval = Column(Integer, doc="通知间隔")
    repeat_notice_interval = Column(Integer, doc="重复通知间隔")
    channel_wechat = Column(Boolean, doc="微信告警")
    channel_mail = Column(Boolean, doc="邮箱告警")
    channel_smg = Column(Boolean, doc="短信")
    alert_group = Column(JSON, doc="告警组")
    cluster_id = Column(Integer, doc="集群ID")


class CheckCommandsModel(CloudEntity):
    """"""
    __tablename__ = "audit_check_commands"

    CMD = "cmd"
    FILE = "file"
    enum_type = Enum(CMD, FILE)

    # colums
    name = Column(String(length=200), doc="名称")
    cmd_or_file_path = Column(String(length=500), doc="命令或路径")
    type = Column(enum_type, doc="命令的类别")
    category_id = Column(Integer, doc="分类id")
    audit_state = Column(Integer, doc="是否开启审计")
    cluster_id = Column(Integer, doc="集群ID")


class DefaultValueModel(CloudEntity):
    """添加的审计项与采集到的值"""
    __tablename__ = "audit_default_value"

    SANFREE = 'sanfree'
    STORAGE = 'storage'
    CLOUD = 'cloud'
    COMPUTE = 'compute'
    NORMAL = 'normal'
    UNKNOWN = 'unknow'
    IB_SWITCH = 'ib_switch'
    LONGHAUL = 'longhaul'

    enum_node_type = Enum(UNKNOWN, LONGHAUL, SANFREE, STORAGE, CLOUD, COMPUTE, NORMAL, IB_SWITCH)
    # colums
    cmd_id = Column(Integer, doc="参数值")
    check_res = Column(JSON, doc="检查结果")
    node_id = Column(Integer, doc="节点ID")
    node_type = Column(enum_node_type, doc="节点类型")
    node_cluster_id = Column(Integer, doc="节点所在集群")


class MonitoringCategoryModel(CloudEntity):
    """审计监控"""
    __tablename__ = "audit_monitoring_category"

    # colums
    category_name = Column(String(length=200), doc="分类名称")
    default = Column(Integer, doc="是否是默认项")
    cluster_id = Column(Integer, doc="集群ID")


class MonitoringItemsModel(CloudEntity):
    """审计监控"""
    __tablename__ = "monitoring_items"

    # colums
    item_name = Column(String(length=200), doc="监控项名称")
    category_id = Column(Integer, doc="类别ID")


# ==================== 巡检相关表结果 ==========================
class InspectionStrategy(CloudEntity):
    """巡检策略"""
    __tablename__ = "inspection_strategy"

    inspect_mode = Column(String(50), doc='巡检方式')
    inspect_frequency = Column(String(50), doc='巡检频率')
    next_inspect_time = Column(DateTime, doc='下次巡检时间')
    last_inspect_time = Column(DateTime, doc='上次巡检时间')
    execution_time = Column(DateTime, doc='执行时间')
    original_analysis = Column(Boolean, doc='原厂分析')
    group_id = Column(String(256), doc="接收组uuid")
    report_store_time = Column(String(50), doc='巡检报告保留时间')
    inspect_status = Column(String(50), doc='巡检状态')
    cluster_id = Column(Integer, ForeignKey(column=QDataCluster.id, ondelete="CASCADE"), doc='集群id')
    cluster = relationship(QDataCluster, lazy='subquery', back_populates="strategy", doc="所关联的集群")


# 历史记录
class InspectionHistory(CloudEntity):
    __tablename__ = 'inspection_history'

    inspect_time = Column(DateTime, doc='巡检时间')
    next_inspect_time = Column(DateTime, doc='下次巡检时间')
    send_email = Column(String(50), doc='邮件发送')
    inspect_result = Column(Boolean, doc='巡检结果')
    inspect_mode = Column(String(50), doc='巡检方式')
    inspect_frequency = Column(String(50), doc='巡检频率')
    original_analysis = Column(Boolean, doc='原厂分析')
    group_id = Column(String(255), doc="接收组id")
    report_name = Column(String(255), doc='巡检报告原始名称')
    uuid = Column(String(255), default=gen_uuid, unique=True, index=True, doc='巡检报告唯一id')
    cluster_id = Column(Integer, ForeignKey(column=QDataCluster.id, ondelete="CASCADE"), doc='集群id')


class FunctionCount(CloudEntity):
    __tablename__ = "func_count"

    func_id = Column(String(255), doc='事件id')
    doc = Column(String(50), doc='事件描述')
    type = Column(String(50), doc='事件类型')
    day = Column(Date, doc='事件日期')
    count = Column(Integer, default=1, doc='事件发生次数')


# ==================== 全局其他一些配置表等 ==========================
class Job(CloudEntity):
    """
    异步任务日志表
    """
    __tablename__ = "q_job"

    uuid = Column(String(255), nullable=False, unique=True, default=gen_uuid)
    cluster_id = Column(Integer, nullable=False, doc="集群id")  # 非强关联
    # 兼容cloud和web_service的Job创建
    root_container_id = Column(Integer, nullable=True, doc="根容器id")  # 非强关联
    pdb_id = Column(Integer, nullable=True, doc="pdb的id")  # 非强关联
    tenant_uuid = Column(String(length=128), nullable=True, doc="租户的uuid")  # 非强关联
    user_uuid = Column(String(length=128), nullable=True, doc="用户的uuid")  # 非强关联
    type = Column(String(length=100), doc="任务类型:create db,create tablespace ...")  # todo @jianxin 增加enum
    progress = Column(String(length=100), default=JobStatus.JOB_PROGRESS_WAIT,
                      doc="任务进度: Waiting schedule, Executing:90%....")
    desc = Column(String(length=3000), doc="任务描述, 在计算资源池xxx新建了数据库...")
    message = Column(String(length=3000), default="", doc="任务执行的中间结果信息")
    last_updated = Column(DateTime, default=datetime.now(), doc="最后一次更新时间")
    finish_time = Column(DateTime)

    def format_data(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "uuid": self.uuid,
            "job_type": self.type,
            "job_progress": self.progress,
            "job_desc": self.desc,
            "attr": self.attr,
            "create_time": convert_utc_to_beijing(self.create_time),
            "finish_time": convert_utc_to_beijing(self.finish_time) if self.finish_time else "",
            "message": self.message,
            "cluster_id": self.cluster_id,
        }

    def mark(self, message: str, has_err: bool = False) -> None:
        """
        更新任务进度
        """
        self.last_updated = datetime.now()
        if self.progress == JobStatus.JOB_PROGRESS_WAIT:
            self.progress = JobStatus.JOB_RUNNING
        prefix = ""
        if not message.startswith("["):
            prefix = "[OK]" if not has_err else "[ERROR]"
        self.message = f"{self.message}\n{prefix}    {message}"

    def mark_failed(self, message: Optional[str] = None) -> None:
        """
        标记任务失败
        """
        self.mark(message=message or "发生了一些未知错误.", has_err=True)
        self.progress = JobStatus.JOB_ERROR
        self.finish_time = datetime.now()

    def mark_finished(self, message: Optional[str] = None) -> None:
        """
        任务结束
        """
        self.mark(message or "任务被标记已完成")
        self.progress = JobStatus.JOB_DONE
        self.finish_time = datetime.now()


class QConfig(CloudEntity):
    """
    全局配置
    """
    __tablename__ = "q_config"

    EMAIL = "qdata_email"
    WECHAT = "qdata_wechat"
    LICENSE = "qdata_license"

    key = Column(String(256), nullable=False, unique=True, doc="用于配置查询的key")
    attr = Column(JSON, default=dict(), doc="key对应配置，配置无法范化，使用json来存储")

    @classmethod
    def get(cls, session: Session, key: str) -> Dict[str, Any]:
        config = session.query(cls).filter(QConfig.key == key).one()
        return config

    @classmethod
    def set(cls, session: Session, key: str, json_obj: Dict[str, Any]) -> None:
        config = session.query(cls).filter(QConfig.key == key).one()
        if config:
            config.attr = json_obj
            flag_modified(config, "attr")
            session.merge(config)
            session.commit()
            return

        config = QConfig(key=key, attr=json_obj)  # type:ignore
        session.add(config)
        session.commit()


# ==============================容灾集群===================================================
class DisasterRecoveryCluster(CloudEntity):
    """
    容灾集群表
    """
    __tablename__ = "disaster_recovery_cluster"
    name = Column(String(length=128), nullable=False, unique=True, doc="容灾集群名称")
    attr = Column(JSON, default={}, doc="容灾集群的额外信息")
    disaster_recovery_databases: Set["DisasterRecoveryDatabase"] = relationship("DisasterRecoveryDatabase",
                                                                                back_populates="disaster_recovery_cluster",
                                                                                cascade="all, delete-orphan",
                                                                                order_by='DisasterRecoveryDatabase.name',
                                                                                collection_class=set)

    def to_dict(self) -> Dict[str, Union[int, str]]:
        return {
            "dg_cluster_id": self.id,
            "dg_cluster_name": self.name.upper()
        }


class DisasterRecoveryDatabase(CloudEntity):
    """
    加入容灾集群的数据库
    """
    __tablename__ = "disaster_recovery_database"

    CLUSTER = "RAC"
    SINGLE = "Single"
    RACONENODE = "RACONENODE"
    enum_db_type = CloudSqlAlchemyEnum(CLUSTER, SINGLE, RACONENODE)
    DB_TYPE_NAME = {
        CLUSTER: u"集群",
        SINGLE: u"单机",
        RACONENODE: u"RacOneNode",
    }

    PRIMARY = "PRIMARY"
    STANDBY = "PHYSICAL STANDBY"
    enum_db_role = CloudSqlAlchemyEnum(PRIMARY, STANDBY)
    DB_ROLE_NAME = {
        PRIMARY: u"主库",
        STANDBY: u"备库",
    }

    attr = Column(JSON, default={}, doc="容灾数据库的额外信息,数据库版本/DB_UNIQUE_NAME")
    name = Column(String(length=128), nullable=False, unique=True, doc="业务系统名称")
    is_qdata = Column(Boolean, default=True, doc="是否是qdata集群")
    password_for_sys = Column(String(255), nullable=True, doc="sys用户,具有sysdba角色的sys用户的密码，该用户可以创建数据库,需要aes存储")
    qdata_database_id = Column(Integer, nullable=True, doc="qdata集群中的database_id")
    qdata_rac_cluster_id = Column(Integer, nullable=True, doc="qdata集群中的rac_cluster_id")
    qdata_cluster_id = Column(Integer, nullable=True, doc="qdata一体机集群的id")
    scan_ip = Column(String(length=128), nullable=False, doc="oracle的scan_ip")
    port = Column(Integer, nullable=True, doc="oracle的监听端口")
    service_name = Column(String(length=128), nullable=False, doc="oracle的service_name")
    monitor_user = Column(String(length=32), nullable=False, doc="oracle的监控用户")
    monitor_password = Column(String(length=128), nullable=False, doc="oracle的监控密码")
    database_type = Column(enum_db_type, nullable=False, doc="数据库类型")
    ori_database_role = Column(enum_db_role, nullable=False, doc="切换前数据库角色")
    database_role = Column(enum_db_role, nullable=False, doc="数据库角色")
    database_name = Column(String(length=32), nullable=False, doc="数据库名")

    disaster_recovery_cluster_id = Column(Integer, ForeignKey(DisasterRecoveryCluster.id, ondelete='CASCADE'),
                                          doc="容灾集群id")
    disaster_recovery_cluster: DisasterRecoveryCluster = relationship(DisasterRecoveryCluster,
                                                                      back_populates="disaster_recovery_databases",
                                                                      uselist=False, doc="关联的容灾集群")

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}  # type: ignore


class QBDisasterRecovery(CloudEntity):
    """容灾恢复任务表"""
    __tablename__ = "qb_disaster_recovery"

    SWITCHOVER_TYPE = "switchover"
    FAILOVER_TYPE = "failover"
    enum_db_switch_type = CloudSqlAlchemyEnum(SWITCHOVER_TYPE, FAILOVER_TYPE)

    STATUS_OK = "Done"
    STATUS_ERROR = "Error"
    STATUS_RUNNING = "Running"
    enum_running_status = CloudSqlAlchemyEnum(STATUS_OK, STATUS_RUNNING, STATUS_ERROR)

    cluster_id = Column(String(length=100), nullable=False, index=True, doc="集群id")
    ori_primary = Column(Integer, nullable=True, doc="切换前的主库id")
    ori_standby = Column(Integer, nullable=True, doc="切换前的备库id")

    switch_type = Column(enum_db_switch_type, nullable=False, doc="容灾操作类型 switchover failover")
    step = Column(Integer, nullable=False, default=0, doc="步骤，执行前先记录步骤，switchover根据节点情况有不同的步骤，"
                                                          "failover有3步")
    status = Column(enum_running_status, nullable=False, doc="切换总状态，Running表示运行中，Error代表错误，Done表示正确")
    desc = Column(String(length=3000), doc="任务描述")
    err_message = Column(String(length=300), default=None, doc="错误步骤的报错信息")
    message = Column(String(length=3000), default="", doc="任务执行的中间结果信息")

    finish_time = Column(DateTime)

    def mark(self, message: str, has_err: bool = False) -> None:
        """
        更新任务进度
        """
        self.update_time = datetime.now()
        self.status = self.STATUS_RUNNING
        prefix = ""
        if not message.startswith("["):
            prefix = "[OK]" if not has_err else "[ERROR]"
        self.message = f"{self.message}\n{prefix}    {message}"

    def mark_with_prefix(self, message: str, prefix: str = "WARNING") -> None:
        """
        更新任务进度
        """
        self.update_time = datetime.now()
        self.status = self.STATUS_RUNNING
        self.message = f"{self.message}\n[{prefix}]    {message}"

    def mark_title(self, message: str) -> None:
        """
        更新无prefix：如标题
        """
        self.update_time = datetime.now()
        self.status = self.STATUS_RUNNING

        self.message = f"{self.message}\n \n{message}" if self.message else message

    def mark_failed(self, message: Optional[str] = None) -> None:
        """
        标记任务失败
        """
        self.mark(message=message or "发生了一些未知错误.", has_err=True)
        self.status = self.STATUS_ERROR
        self.finish_time = datetime.now()

    def mark_finished(self, message: Optional[str] = None) -> None:
        """
        任务结束
        """
        self.mark(message or "任务被标记已完成")
        self.status = self.STATUS_OK
        self.finish_time = datetime.now()


# ==============================license===================================================
class LicenseData(CloudEntity):
    """
    license信息表
    """
    __tablename__ = "license_data"
    data = Column(Text, default="", doc="license信息")


# ================================用户资源关联表============================================
class DepartmentResourceQuota(CloudEntity):
    """
    租户资源关联表
    """
    __tablename__ = "department_resource_quota"
    uuid = Column(String(length=128), nullable=False, doc="QFusion租户的uuid")
    cluster_id = Column(String(length=100), nullable=False, doc="一体机集群id")

    @classmethod
    def get_qdata_cluster_by_uuid(cls, session: Session, department_uuid: Optional[str]) -> List[QDataCluster]:
        """
        根据租户uuid返回一体机集群列表
        :param session: 会话对象
        :param department_uuid: 租户的uuid;
        :return: 成功返回集群列表；失败返回空
        """
        cluster_id_list = cls.get_qdata_cluster_id_list_by_uuid(session, department_uuid)
        qdata_cluster_list: List[QDataCluster] = []
        if cluster_id_list:
            for cluster_id in cluster_id_list:
                qdata_cluster = QDataCluster.get_by_id(session, int(cluster_id))  # type: ignore
                qdata_cluster_list.append(qdata_cluster)
        return qdata_cluster_list

    @classmethod
    def get_qdata_cluster_id_list_by_uuid(cls, session: Session, department_uuid: Optional[str]) -> List[str]:
        """获取当前用户租户的qdata_cluster_id_list

        Args:
            session: 数据库会话
            department_uuid: 租户(部门)的uuid

        Returns:
            [success]返回qdata集群的id列表;[fail]返回None
        """
        if not department_uuid:  # admin用户查所有
            query = session.query(cls.cluster_id)
        else:
            query = session.query(cls.cluster_id).filter(cls.uuid == department_uuid)
        cluster_id_list: List[str] = [cluster.cluster_id for cluster in query.all()]
        return cluster_id_list

    @classmethod
    def get_tenant_ids_by_cluster(cls, session: Session, cluster: QDataCluster) -> List[str]:
        """
        根据传入的一体机返回绑定的租户ID列表
        :param session: 会话对象
        :param cluster: qdata_cluster一体机对象
        :return:
        """
        admin_uuid: str = "847798ee3db44716b6357b04e5a55c16"
        tenant_id_list: List[str] = session.query(cls.uuid).filter(cls.cluster_id == cluster.id).all()
        return [tenant.uuid for tenant in tenant_id_list] if tenant_id_list else [admin_uuid, ]  # type: ignore
