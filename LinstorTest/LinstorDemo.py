#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: LinstorDemo.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2019/11/3 上午10:52
# History:
#=============================================================================
"""
import re
import redis
import logging
import linstor
import datetime
import random
from linstor import ResourceData
from linstor import sharedconsts as api_consts
import json
import pprint
from collections import defaultdict

import time
from multiprocessing.pool import ThreadPool

logger = logging.getLogger(__name__)


class LinstorManager(object):
    def __init__(self, ip, port=3370, timeout=300):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.url = "linstor://{ip}:{port}".format(ip=self.ip, port=self.port)
        self._lin_api = linstor.Linstor(self.url, timeout=self.timeout)

    @property
    def lin_api(self):
        self._lin_api.connect()
        print id(self._lin_api)
        return self._lin_api

    def __del__(self):
        self._lin_api.disconnect()
        print "self._lin_api.disconnect() -> {}".format(id(self._lin_api))

    def check_result(self, ret):
        res = linstor.Linstor.all_api_responses_success(ret)
        error_msg = []
        if not res:
            error_msg = [r.message for r in ret if not r.is_success()]
            error_msg = "<br/>".join(error_msg)
        return res, error_msg


expansion_time_dict = defaultdict(dict)


def parse_capacity_bytes(s, is_iec=False):
    """
    去掉单位，返回 单位为 B 的数值
    :param s: 带单位size
    :param is_iec: 是否使用IEC标准，默认不使用，进制是1000
    * -- 国际电工协会（IEC）拟定了"KiB"、“MiB”、“GiB"的二进制单位，专用来标示“1024进位”的数据大小;
         而硬盘厂商在计算容量方面是以每1000为一进制的，每1000字节为1KB，每1000KB为1MB，每1000MB为1GB，每1000GB为1T;
         在操作系统中对容量的计算是以1024为进位的，并且并未改为"KiB"、“MiB”、“GiB"的二进制单位
    :return:
    """
    # 获取数值 和 单位
    system = 1024 if is_iec else 1000
    pattern = re.compile(r"(\d+\.?\d*)\s*(\w+)")
    match = pattern.search(s)
    if match:
        size, units = match.group(1), match.group(2)
    else:
        return float(s)
    size = float(size)
    if "B" not in units:
        units += "B"
    multiplier = {
        'PB': 5,
        'TB': 4,
        'GB': 3,
        'MB': 2,
        'KB': 1,
        'B': 0
    }.get(units.upper(), 0)

    return int(size * pow(system, multiplier))


class LinstorRebalanceManager(LinstorManager):
    """Linstor存储节点重平衡管理"""

    # ======================按需要获取相关节点============================
    def __get_nodes(self, filter_by_status=None):
        """
        获取指定状态的节点
        :param List[str] filter_by_status: 节点状态
        :return list[Node]: 成功返回linstor节点信息列表
        """
        try:
            # 从linstor中查询出列表结果
            nodes_info_list = self.lin_api.node_list()[0].data_v1

            if filter_by_status is not None:
                return [node_info for node_info in nodes_info_list if node_info["connection_status"] in filter_by_status]
            else:
                return nodes_info_list
        except Exception as e:
            logger.warning("获取{status}节点发生异常：{error}".format(status=filter_by_status, error=str(e)))
            return list()

    def get_online_nodes(self):
        """获取在线的节点信息列表"""
        return self.__get_nodes(filter_by_status=["ONLINE"])

    # ======================重平衡针对lv错误进行的相关相关=============================
    def __get_node_absence_lvs_info_dict(self):
        """
        从linstor中获取卷信息，得到卷在各个节点上的分布情况，
        比较在线的节点列表与卷分布的节点情况，得到卷不能存在的节点信息字典
        :return: 卷不能存在的节点信息集合
        {
            "sto1": {
                "vg2": ["lv2_1"]
            },
            "sto2": {
                "vg1": ["lv1_2"]
            },
            "sto3": {
                "vg1": ["lv1_1", "lv1_2", "lv1_3"],
                "vg2": ["lv2_1", "lv2_2", "lv2_3"]
            }
        }
        """
        # 获取卷存在的节点信息字典
        # {
        #     "lv1_1": {
        #         "vg1": ["sto1", "sto2", "sto3"]
        #     },
        #     "lv1_2": {
        #         "vg1": ["sto1", "sto2", "sto3"]
        #     },
        #     "lv2_1": {
        #         "vg2": ["sto1", "sto2"]
        #     }
        # }
        lvs_vg_node_dict = defaultdict(lambda: defaultdict(list))
        node_vol_info_list = self.lin_api.volume_list()[0].data_v1
        for node_vol_info in node_vol_info_list:
            node_name = node_vol_info["node_name"]
            for vol_info in node_vol_info.get("volumes", list()):
                for lvs_info in vol_info.get("layer_data_list", list()):
                    backing_device_name = lvs_info.get("data", dict()).get("backing_device", "")
                    if backing_device_name.count('/') < 2:
                        continue

                    # 正常情况下，返回的字符串为 /dev/vg1/lv1_1 这种格式
                    backing_device_name_list = backing_device_name.split('/')
                    vg_name = backing_device_name_list[-2]
                    lv_name = backing_device_name_list[-1]
                    lvs_vg_node_dict[lv_name][vg_name].append(node_name)

        # 获取在线节点列表
        online_node_list = [node["name"] for node in self.get_online_nodes()]

        # 计算出在线节点中，卷不可能存在的节点
        node_vg_lvs_dict = defaultdict(lambda: defaultdict(list))
        for lv_name, vg_info_dict in lvs_vg_node_dict.iteritems():
            for vg_name, node_list in vg_info_dict.iteritems():
                # 遍历 不可能存在的 节点，将信息补全
                for node_name in (set(online_node_list) - set(node_list)):
                    node_vg_lvs_dict[node_name][vg_name].append(lv_name)

        return node_vg_lvs_dict

    def clean_lvs_info_from_system(self):
        """清除不应该存在于节点上的lv卷"""
        # 获取节点不应存在的卷信息
        node_vg_lvs_dict = self.__get_node_absence_lvs_info_dict()

        # 遍历卷信息，执行 lvremove 操作
        for node_name, vg_info_dict in node_vg_lvs_dict.iteritems():
            for vg_name, lv_list in vg_info_dict.iteritems():
                # fixme： 为防止删除过程中linstor刚好创建了对应的资源卷，需要再次判断lv是否存在于linstor中
                pass


DEL_DISK_TASK_NAME = "rebalance_after_del_disk_task"
DEL_NODE_TASK_NAME = "rebalance_after_del_node_task"
r_client = redis.Redis(host="192.168.1.16")


def _task_name(func_name, *args):
    """任务名称format"""
    return "{func}_{args}".format(func=func_name, args="_".join(str(a) for a in args))


def get_task(func_name, *args):
    """获取任务"""
    value = r_client.get(_task_name(func_name, *args))
    return int(value) if value is not None else 0


def set_task(func_name, ex, value, *args):
    """
    在redis中设置任务名称
    :param str func_name: 功能的名字
    :param timedelta ex: 过期时间
    :param int value: 设置的值
    """
    key = _task_name(func_name, *args)
    if ex:
        r_client.set(key, value, ex=datetime.timedelta(seconds=int(ex + 3600)))  # 过期时间
    else:
        r_client.set(key, value, ex=datetime.timedelta(seconds=10 * 60))
    logger.debug("👈Linstor定时任务，设置{k}参数".format(k=key))


set_task(DEL_DISK_TASK_NAME, 1, 1, "name", "spool")

if __name__ == '__main__':
    # print "{t}".format(t=("sto1", "rd0", "sp0"))
    linstor_rebalance_manager = LinstorRebalanceManager(ip="192.168.1.70")
    # vol_list = linstor_rebalance_manager.__get_node_absence_lvs_info_dict()
    # r = linstor_rebalance_manager.lin_api.resource_list(filter_by_resources=["ch_test"])[0].data_v1
    # sp_list = linstor_rebalance_manager.lin_api.storage_pool_list_raise().data_v1
    # r_list = linstor_rebalance_manager.lin_api.resource_list(filter_by_resources=["rd4"])[0].data_v1
    # v_list = linstor_rebalance_manager.lin_api.volume_list(filter_by_nodes=["sto4"],
    #                                                        filter_by_stor_pools=["ls_pool_ls"])[0].data_v1
    linstor_rebalance_manager.clean_lvs_info_from_system()
    pass
    # sp_list = linstor_rebalance_manager.lin_api.storage_pool_list()[0].data_v1
    # expansion_time_dict["poola"] = dict(nodes={"china-mobile-sto205": ["sp10", "sp11", "sp12"],
    #                                            "china-mobile-sto204": ["sp10"], },
    #                                     time=datetime.datetime.now() - datetime.timedelta(seconds=25))
    # del expansion_time_dict["poola"]
    # print datetime.datetime.now()
    # print expansion_time_dict["poola"]["time"]
    #
    # res = linstor_rebalance_manager.cal_pool_sync_target_on_time("poola")
    # print "{:2} %".format(res)

    pass
