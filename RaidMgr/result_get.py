#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: result_get.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/9/18 11:51 上午
# History:
#=============================================================================
"""
import pathlib

megaraid_code_map = [

    # 磁盘信息获取
    {
        "name": "获取 raid 卡控制器对应的 bus_address",
        "old_cmd": "Megacli -AdpGetPciInfo -aALL",
        "new_cmd": "storcli64 /c{c_id} show pci",
    },
    {
        "name": "获取 raid 卡控制器中的 Enclosure 信息",
        "old_cmd": "MegaCli -EncInfo -a0",
        "new_cmd": "storcli64 /c{c_id}/e{e_id} show all",
    },
    {
        "name": "获取 虚拟磁盘和物理磁盘信息",
        "old_cmd": "MegaCli -LdPdInfo -a%d",
        "new_cmd": "storcli64 /c{c_id}/v{v_id} show all",
    },
    {
        "name": "获取 所有物理磁盘信息",
        "old_cmd": "MegaCli -PDList a%d",
        "new_cmd": "storcli64 /c{c_id}/e{e_id}/sall show all",
    },

    # 磁盘亮灯、熄灯
    {
        "name": "亮灯",
        "old_cmd": "MegaCli -PdLocate -start -physdrv[%d:%d] -a0",
        "new_cmd": "storcli64 /c{c_id}/e{e_id}/s4 start locate",
    },
    {
        "name": "熄灯",
        "old_cmd": "MegaCli -PdLocate -stop -physdrv[%d:%d] -a0",
        "new_cmd": "storcli64 /c{c_id}/e{e_id}/s4 stop locate",
    },

    # 挂载、卸载磁盘
    {
        "name": "清理磁盘缓存",
        "old_cmd": "MegaCli -DiscardPreservedCache -L{vd}",
        "new_cmd": "storcli64 /c{c_id}/v{v_id} delete preservedcache force",
    },

    {
        "name": "修改物理磁盘 Firmware state 状态 1",
        "old_cmd": "MegaCli -PDMakeGood -PhysDrv[{dev_id}:{slot_number}]",
        "new_cmd": "storcli64 /c{c_id}/e{e_id}/sx set good",
    },
    {
        "name": "修改物理磁盘 Firmware state 状态 2",
        "old_cmd": "MegaCli -CfgForeign -Scan",
        "new_cmd": "storcli64 /c{c_id}/fall show all",
    },

    {
        "name": "清理配置信息",
        "old_cmd": "MegaCli -CfgForeign -Clear -a0",
        "new_cmd": "storcli64 /c{c_id}/fall del",
    },
    {
        "name": "正常挂载",
        "old_cmd": "MegaCli -CfgLdAdd -r0 [{dev_id}:{slot_number}] {cache_mode} NORA Direct",
        "new_cmd": "storcli64 /c{c_id} add vd r0 drives=e:s [WT|WB|AWB] nora direct",
    },
    {
        "name": "init disk 清空磁盘上的所有数据",
        "old_cmd": "MegaCli -LDInit -Start -L{vd}",
        "new_cmd": "storcli64 /c{c_id}/v{v_id} start init",
    },
    {
        "name": "磁盘卸载",
        "old_cmd": "MegaCli -CfgLdDel -L{vid}",
        "new_cmd": "",
    },

    # 设置 cache 策略
    {
        "name": "设置 WriteBack 策略",
        "old_cmd": "MegaCli -LDSetProp -WB -L{vid}",
        "new_cmd": "",
    },
    {
        "name": "设置 WriteThrough 策略",
        "old_cmd": "MegaCli -LDSetProp -WT -L{vid}",
        "new_cmd": "",
    },

    {
        "name": "",
        "old_cmd": "MegaCli -GetPreservedCacheList -a%d",
        "new_cmd": "storcli64 /c0 show preservedcache",
    },
    {
        "name": "",
        "old_cmd": "MegaCli -AdpSetProp -EnableJBOD -0",
        "new_cmd": "storcli64 /c0 set jbod=off",
    },
]
