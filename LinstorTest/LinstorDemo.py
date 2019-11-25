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

    def cal_pool_sync_target_on_time(self, pool_name, rebalance_rate="5 GB"):
        """
        通过时间计算重平衡状态
        :param str pool_name: 存储池的名字
        :param str rebalance_rate: 重平衡速率，单位秒
        :return: 重平衡进度
        """
        global expansion_time_dict

        # 计算时间差
        expansion_time = expansion_time_dict[pool_name]["time"]
        time_now = datetime.datetime.now()
        time_interval = (time_now - expansion_time).total_seconds()

        # 按条件遍历卷信息，找出所有的同步盘的磁盘大小
        device_size_dict = dict()
        for node_name, sp_list in expansion_time_dict[pool_name]["nodes"].iteritems():
            resource_info_list = self.lin_api.volume_list(filter_by_stor_pools=sp_list)[0].data_v1
            for resource_info in resource_info_list:
                for volume_info in resource_info.get("volumes", list()):
                    device_size_dict[volume_info.get("device_path", "")] = volume_info.get("allocated_size_kib", 0) * 1024

        # 计算同步进度
        total_rebalance_size_bytes = sum(device_size_dict.values())  # 待同步的数据量，单位B
        rebalance_rate_bytes = parse_capacity_bytes(rebalance_rate, is_iec=True)  # 同步速率，单位B
        if rebalance_rate_bytes * time_interval >= total_rebalance_size_bytes:
            del expansion_time_dict[pool_name]
            return 100
        else:
            return float(100 * (rebalance_rate_bytes * time_interval / total_rebalance_size_bytes))

class test:
    time_dict = defaultdict(dict)

    def change(self):
        self.time_dict["time"] = 100


if __name__ == '__main__':
    # print "{t}".format(t=("sto1", "rd0", "sp0"))
    linstor_rebalance_manager = LinstorRebalanceManager(ip="192.168.1.70")
    # vol_list = linstor_rebalance_manager.__get_node_absence_lvs_info_dict()
    # r = linstor_rebalance_manager.lin_api.resource_list(filter_by_resources=["ch_test"])[0].data_v1
    # sp_list = linstor_rebalance_manager.lin_api.storage_pool_list_raise().data_v1
    # r_list = linstor_rebalance_manager.lin_api.resource_list(filter_by_resources=["rd4"])[0].data_v1
    # v_list = linstor_rebalance_manager.lin_api.volume_list(filter_by_nodes=["china-mobile-sto204"],
    #                                                        filter_by_stor_pools=["sp3"])[0].data_v1
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
    t_1 = test()
    t_1.time_dict["time"] = datetime.datetime.now()

    t_2 = test()
    t_2.change()

    print t_1.time_dict

    pass
