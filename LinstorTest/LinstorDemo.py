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
import logging
import linstor
import random
from linstor import ResourceData
import json
import pprint
from collections import defaultdict

logger = logging


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


class LinstorRebalanceManager(LinstorManager):
    """Linstor存储节点重平衡管理"""

    def __get_nodes(self, filter_by_status=None):
        """
        获取指定状态的节点
        :param List[str] filter_by_status: 节点状态
        :return list[Node]: 成功返回linstor节点信息列表，异常返回None
        """
        try:
            nodes_info_list = self.lin_api.node_list()[0].data_v1

            if filter_by_status is not None:
                return [node_info for node_info in nodes_info_list if node_info["connection_status"] in filter_by_status]
            else:
                return nodes_info_list
        except Exception as e:
            logging.warning("获取{status}节点发生异常：{error}".format(status=filter_by_status, error=str(e)))
            return None

    def get_online_nodes(self):
        """获取在线的节点信息列表"""
        return self.__get_nodes(filter_by_status=["ONLINE"])

    def get_offline_nodes(self):
        """获取离线的节点信息列表"""
        # 在返回离线节点之前，先尝试进行重连
        self.lin_api.node_reconnect(node_names=[node_info["name"] for node_info in self.__get_nodes(filter_by_status="OFFLINE")])
        return self.__get_nodes(filter_by_status=["OFFLINE", "VERSION_MISMATCH"])

    def get_all_nodes(self):
        """获取所有的节点信息列表"""
        return self.__get_nodes()

    def _clean_offline_node(self):
        """
        清理掉线节点的资源
        :return:
        """
        # linstor获取掉线的存储节点
        # offline_nodes = [node_info["name"] for node_info in self.get_offline_nodes()]
        offline_nodes = [node_info["name"] for node_info in self.get_online_nodes()]
        for offline_node in offline_nodes:
            # 删除离线节点上的所有资源
            rsc_list = self.lin_api.resource_list(filter_by_nodes=[offline_node])[0].data_v1
            # for rsc in rsc_list:
            #     ret, err_msg = self.check_result(self.lin_api.resource_delete(node_name=offline_node, rsc_name=rsc["name"]))
            #     if not ret:
            #         logger.warning("删除离线节点({off_node})上的资源({rsc})发生错误！{error}".format(off_node=offline_node, rsc=rsc["name"], error=err_msg))
            #         continue

            # 删除离线节点上的存储池
            sp_list = self.lin_api.storage_pool_list(filter_by_nodes=[offline_node])[0].data_v1
            for sp in sp_list:
                ret, err_msg = self.check_result(self.lin_api.storage_pool_delete(node_name=offline_node, storage_pool_name=sp["storage_pool_name"]))
                if not ret:
                    logger.warning("删除离线节点({off_node})上的存储池({sp})发生错误！{error}".format(off_node=offline_node, sp=sp["storage_pool_name"], error=err_msg))
                    continue

    def _available_nodes(self, is_online=True):
        """
        获取所有符合条件的存储节点
        :param bool is_online: 节点是否在线
        :return list[str]: 可用的存储节点名列表
        """
        # linstor获取存储节点
        node_info_list = self.lin_api.node_list()[0].data_v1

        if is_online:
            node_info_dict = {node_info["net_interfaces"][0]["address"]: node_info["name"] for node_info in node_info_list if node_info["connection_status"] == "ONLINE"}
        else:
            node_info_dict = {node_info["net_interfaces"][0]["address"]: node_info["name"] for node_info in node_info_list}

        node_info_dict.pop("10.10.160.97")

        return node_info_dict.values()

    def _resource_info_dict(self, filter_by_nodes=None):
        """
        获取资源信息字典
        :param list[str] filter_by_nodes: 过滤节点列表
        :return:
        {
            "r0": {
                "sp0": ["sto1", "sto2", "sto3"],
                "sp1": ["sto1", "sto2"]
            }
        }
        """
        # 从linstor接口获取资源信息
        resource_list = self.lin_api.resource_list(filter_by_nodes=filter_by_nodes)[0].data_v1

        # 归档资源信息， r0 -> sp0 -> sto1
        resource_info_dict = defaultdict(lambda: defaultdict(list))
        for resource_info in resource_list:
            resource_name = resource_info["name"]  # 卷名称
            sp_name = resource_info.get("props", dict()).get("StorPoolName")  # 池名称

            resource_info_dict[resource_name][sp_name].append(resource_info.get("node_name"))

        return resource_info_dict

    def _create_volume_with_available_nodes(self, available_nodes, sp_name, rsc_name):
        """
        在可用的节点上创建卷
        :param list[str] available_nodes: 待创建的节点列表
        :param str sp_name: 卷所在的存储池
        :param str rsc_name: 卷所使用的资源名
        :return:
        """
        for node_name in available_nodes:
            # 创建存储池，以防万一。这里需满足的条件是，必须还有一个副本剩余
            sp_info_list = self.lin_api.storage_pool_list(filter_by_stor_pools=[sp_name])[0].data_v1
            storage_driver = sp_info_list[0]["provider_kind"]  # 存储的驱动，如 LVM
            driver_pool_name = sp_info_list[0]["props"].values()[0]  # 所在的存储节点上的 vg 名称，如 vg1
            ret, error_msg = self.check_result(self.lin_api.storage_pool_create(node_name=node_name,
                                                                                storage_pool_name=sp_name,
                                                                                storage_driver=storage_driver,
                                                                                driver_pool_name=driver_pool_name))
            if not ret:
                logging.warning("创建存储池{sp}时返回错误：{error}".format(sp=sp_name, error=error_msg))

            # 在指定节点上创建资源卷
            # res = self.lin_api.resource_delete(node_name=node_name, rsc_name=rsc_name)
            rsc_data = [linstor.ResourceData(node_name=node_name, rsc_name=rsc_name, storage_pool=sp_name)]
            ret, error_msg = self.check_result(self.lin_api.resource_create(rscs=rsc_data))
            if not ret:
                logging.warning("创建资源卷{rsc}时返回错误：{error}".format(rsc=(node_name, rsc_name, sp_name), error=error_msg))

    def rebalance(self):
        """
        linstor重平衡策略：
            - 过滤出可用的存储节点，存储节点需满足条件
                - 1.在线(默认);
                - 2.是存储节点，通过数据库表QData_Node表中的type字段判断
            - 找出linstor上资源的分布情况，找到对应关系。资源对应的存储池，存储池所在的存储节点信息。
                {
                    "r0": {
                        "sp0": ["sto1", "sto2", "sto3"],
                        "sp1": ["sto1", "sto2"]
                    }
                }
            - 如果资源真实的副本数，不满足设置的副本数，则在空余的可用存储节点中，挑选出 差额副本数的存储节点，进行卷副本的创建

        假设，当前可用的存储节点为 ["sto1", "sto2", "sto3", "sto4", "sto5"],
        r0资源在存储池sp1上创建的目标副本数为3，
        但只在 ["sto1", "sto2"] 节点上存在副本。
        那么需要在剩余的 ["sto3", "sto4", "sto5"] 副本中挑选出一个副本，进行资源的同步。
        使用的方法是： random.sample(["sto3", "sto4", "sto5"], 1)
        第一个参数为待选择的同步的存储节点列表， 第二个参数为从中挑选的节点数。
        如果上面挑选出的节点为 ["sto3"]
        则在 ["sto3"] 上进行副本的创建
        """
        available_nodes_list = self._available_nodes()  # linstor中可使用的存储节点名称列表
        rsc_info_dict = self._resource_info_dict(filter_by_nodes=available_nodes_list)  # 存储节点上的卷分布信息

        # 遍历卷分布信息，进行重平衡
        for rsc_name, sp_info in rsc_info_dict.iteritems():
            # 目标资源卷所需的副本数量
            target_copy_num = 3

            for sp_name, sto_list in sp_info.iteritems():
                # 资源副本数达到要求时，跳过此资源
                if len(sto_list) >= target_copy_num:
                    logging.info("资源({rsc})分布在存储节点({sto_list})上，数量 {sto_num} >= {target}，满足要求，无需进行重平衡。".format(rsc=rsc_name,
                                                                                                               sto_list=sto_list,
                                                                                                               sto_num=len(sto_list),
                                                                                                               target=target_copy_num))
                    continue

                logging.info("资源({rsc})分布在存储节点({sto_list})上，数量 {sto_num} < {target}，不满足要求，需要进行重平衡。".format(rsc=rsc_name,
                                                                                                           sto_list=sto_list,
                                                                                                           sto_num=len(sto_list),
                                                                                                           target=target_copy_num))
                # 从全部节点中，挑选出可以平衡的节点
                node_list = list(set(available_nodes_list) - set(sto_list))
                if not node_list:
                    logging.info("可用的存储节点({a_nodes})中没有除存在节点({s_nodes})以外的可用节点，跳过此条资源({rsc})。".format(a_nodes=available_nodes_list,
                                                                                                      s_nodes=sto_list,
                                                                                                      rsc=rsc_name))
                    continue

                # 随机挑选出存储节点，满足目标副本数
                add_node_list = random.sample(node_list, target_copy_num - len(sto_list))

                # 在对应的存储节点上创建缺失的卷
                self._create_volume_with_available_nodes(available_nodes=add_node_list, sp_name=sp_name, rsc_name=rsc_name)
                logging.info("create volume (node_name={node_name}, sp_name={sp_name}, rsc_name={rsc_name})".format(node_name=add_node_list,
                                                                                                                    sp_name=sp_name,
                                                                                                                    rsc_name=rsc_name))

    def __clean_cache_device(self, node_name, dm_names):
        """

        :param str node_name:
        :param list[str] dm_names:
        :return:
        """
        pass

    def _del_error_pool(self, node_name, sp_name, rsc_name, dm_names):
        """

        :param str node_name:
        :param str sp_name:
        :param str rsc_name:
        :param list[str] dm_names:
        :return:
        """

        ret, err_msg = self.check_result(self.lin_api.resource_delete(node_name=node_name, rsc_name=rsc_name))
        if not ret:
            logger.warning("")

        ret, err_msg = self.lin_api.storage_pool_delete(node_name=node_name, storage_pool_name=sp_name)
        if not ret:
            logger.warning("")

        pass

    def del_error_pool(self, filter_by_nodes=None):
        volume_info_list = self.lin_api.volume_list(filter_by_nodes=filter_by_nodes)[0].data_v1
        for volume_info in volume_info_list:
            diskless_flag = "DISKLESS" in volume_info.get("flags", list())
            for volume in volume_info.get("volumes", list()):
                volume_state = volume.get("state", dict()).get("disk_state", "")
                if volume_state == "Diskless" and not diskless_flag:
                    node_name = volume_info["node_name"]
                    sp_name = volume_info.get("props", dict()).get("StorPoolName")
                    rsc_name = volume_info["name"]
                    dm_names = [drbd_info.get("backing_device", "").replace("/dev/", "").replace('/', '-')
                                for drbd_info in volume_info.get("layer_object", dict()).get("drbd", dict()).get("drbd_volumes", list())
                                if "backing_device" in drbd_info]

                    break
        pass


if __name__ == '__main__':
    # print "{t}".format(t=("sto1", "rd0", "sp0"))
    linstor_rebalance_manager = LinstorRebalanceManager(ip="10.10.160.13")
    # for snapshot in linstor_rebalance_manager.lin_api.snapshot_dfn_list()[0].data_v1:
    #     snapshot_name = snapshot["name"]
    #     rd_name = snapshot["resource_name"]
    #     linstor_rebalance_manager.lin_api.snapshot_delete(rsc_name=rd_name, snapshot_name=snapshot_name)
    #     pass
    linstor_rebalance_manager.del_error_pool(filter_by_nodes=["sto3", "twx2"])
    # linstor_rebalance_manager._clean_offline_node()
    # node_l = linstor_rebalance_manager._available_nodes(is_online=False)
    # volume_info_d = linstor_rebalance_manager._resource_info_dict(filter_by_nodes=node_l)
    # linstor_rebalance_manager.create_volume_single_node(node_name="sto1", sp_name="sp0", rsc_name="yt")
    # linstor_rebalance_manager.rebalance()
    # pass
    # with LinstorManager(ip="10.10.160.13") as lin:
    #     # node_list = lin.node_list()
    #     # pprint.pprint(node_list[0].data_v1, indent=4)
    #
    #     stor_list = lin.storage_pool_list()
    #     pprint.pprint(stor_list[0].data_v1, indent=4)
    #
    #     pass  # This file was autogenerated by genconsts.py
