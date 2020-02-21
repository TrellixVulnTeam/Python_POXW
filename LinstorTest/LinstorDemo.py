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
from linstor.sharedconsts import FLAG_DISKLESS
from linstor import ResourceData
import datetime
import random
from linstor import ResourceData
from linstor import sharedconsts as api_consts
import json
import pprint
from collections import defaultdict, namedtuple

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

    def _get_nic_map(self):
        """
        获取节点下使用的同步网卡映射关系
        :return:
        {
            "china-mobile-com201": "nic1",
            "china-mobile-com202": "nic2",
        }
        """
        node_list = self.lin_api.node_list()[0].data_v1

        nic_map = dict()
        for node_info in node_list:
            node_name = node_info["name"]
            default_nic = None
            pref_nic = node_info.get("props", dict()).get("PrefNic", "")
            other_nics = list()

            for interface in node_info.get("net_interfaces", list()):
                if interface.get("is_active"):
                    default_nic = interface["name"]
                else:
                    other_nics.append(interface["name"])

            # 优先选择预先设置的prefnic网卡
            # 其次为默认网卡
            # 再其次从设置的其他网卡中选择一块
            # 如果没有，则置为None
            if pref_nic:
                nic_map.update({node_name: pref_nic})
            elif other_nics:
                nic_map.update({node_name: random.choice(other_nics)})
            elif default_nic:
                nic_map.update({node_name: default_nic})
            else:
                nic_map.update({node_name: None})

        return nic_map

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

    def __ssh_run(self):
        return """
        [
    {
        "target_name": "s01.3262.01",
        "target_id": 1,
        "driver": "nvmf",
        "acl": [
            "172.16.129.0/24",
            "172.16.128.0/24"
        ],
        "target_state": "ready",
        "lun_info": [
            {
                "healthy": true,
                "path": "/dev/qdisk/LUN2",
                "id": 1,
                "size": "238374 MB"
            }
        ],
        "external": "NO",
        "port": "3262"
    },
    {
        "target_name": "s01.3263.01",
        "target_id": 1,
        "driver": "nvmf",
        "acl": [
            "172.16.129.0/24",
            "172.16.128.0/24"
        ],
        "target_state": "ready",
        "lun_info": [
            {
                "healthy": true,
                "path": "/dev/qdisk/LUN3",
                "id": 1,
                "size": "10739 MB"
            }
        ],
        "external": "NO",
        "port": "3263"
    },
    {
        "target_name": "s01.3264.01",
        "target_id": 1,
        "driver": "nvmf",
        "acl": [
            "172.16.129.0/24",
            "172.16.128.0/24"
        ],
        "target_state": "ready",
        "lun_info": [
            {
                "healthy": true,
                "path": "/dev/qdisk/LUN39",
                "id": 1,
                "size": "5372 MB"
            }
        ],
        "external": "NO",
        "port": "3264"
    }
]
"""

    def dump_rsc_info(self, bin_name):
        import pickle

        rsc_info_list = self.lin_api.volume_list()[0].data_v1
        with open(bin_name, "wb") as f:
            pickle.dump(rsc_info_list, f)

    def load_rsc_info(self, bin_name):
        import pickle

        with open(bin_name, "rb") as f:
            rsc_info_list = pickle.load(f)

        return rsc_info_list

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
                return [node_info for node_info in nodes_info_list if
                        node_info["connection_status"] in filter_by_status]
            else:
                return nodes_info_list
        except Exception as e:
            logger.warning("获取{status}节点发生异常：{error}".format(status=filter_by_status, error=str(e)))
            return list()

    def get_online_nodes(self):
        """获取在线的节点信息列表"""
        return self.__get_nodes(filter_by_status=["ONLINE"])

    def get_node_absence_lvs_info_dict(self):
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

    @staticmethod
    def wait_drbd_connecting(ssh, lun_path, wait_time=30):
        """
        等待drbd资源同步
        :param ssh: ssh对象
        :param str lun_path: 对应的lun路径
        :param int wait_time: 等待时间
        :return:
        """
        drbd_number = int(lun_path[lun_path.rfind('LUN') + 3:]) - 1 + 1000
        drbd_name = "drbd{num}".format(num=drbd_number)

        for _ in range(2 * wait_time):
            try:
                time.sleep(0.5)
                rsc_name_str = ssh.run_cmd("linstor v l 2>/dev/null | grep %s | awk '{print $4}' | uniq " % drbd_name)
                rsc_name_list = rsc_name_str.splitlines()
                for rsc_name in rsc_name_list:
                    drbd_status_str = ssh.run_cmd("drbdadm status {} 2>/dev/null".format(rsc_name))
                    connect_flag_num = drbd_status_str.count("Connecting")

                    if connect_flag_num > 0:
                        break
                    else:
                        return

            except Exception as e:
                logger.warning("等待drbd块设备({lun})同步发生异常！{error}".format(lun=lun_path, error=str(e)))
        else:
            logger.warning("drbd块设备({lun})在 {sec}'s 内未发生同步！".format(lun=lun_path, sec=wait_time))


if __name__ == '__main__':
    # print "{t}".format(t=("sto1", "rd0", "sp0"))
    linstor_rebalance_manager = LinstorManager(ip="10.10.99.60")

    # linstor_rebalance_manager.lin_api.resource_delete()
    nic_map = linstor_rebalance_manager._get_nic_map()

    #
    # linstor_rebalance_manager._stop_error_disk_qlink(1, "china-mobile-sto203", "spp6", "rd6")

    # linstor_rebalance_manager = LinstorManager(ip="10.10.100.11")

    # linstor_rebalance_manager.get_node_absence_lvs_info_dict()

    # linstor_rebalance_manager.dump_rsc_info(bin_name="./volume_info_del_node.bin")
    # linstor_rebalance_manager.load_rsc_info(bin_name="./volume_info_del_node.bin")

    # node_list = linstor_rebalance_manager.lin_api.node_list()[0].data_v1

    # linstor_rebalance_manager._resource_create_and_modify_nic(rscs=[ResourceData(node_name="cn203", storage_pool="stop0", rsc_name="ewa0")])

    # del_sto_pool = linstor_rebalance_manager.del_storage_pool_with_error_disk(cluster_id=1, filter_by_stor_pools=["stop0"])
    # d_1 = linstor_rebalance_manager._resource_info_dict(filter_by_stor_pools=["stop1"])
    # linstor_rebalance_manager._stop_error_disk_qlink(1, "qdata-sto31-dev", "poolB_vg4", "yt_test")
    # linstor_rebalance_manager._start_qlink_after_resource_create(1, "qdata-sto31-dev", "poolB_vg4", "yt_test")
    # d = linstor_rebalance_manager.lin_api.volume_list()[0].data_v1
    # linstor_rebalance_manager.lin_api.resource_auto_place()
    pass
