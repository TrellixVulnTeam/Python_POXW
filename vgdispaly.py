#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: vgdispaly.py
@time: 2020/5/8
@author: alfons
"""


def get_volume_groups():
    # output = ssh.run_cmd("sudo /sbin/vgdisplay")
    with open("vgdisplay", 'r') as f:
        volume_groups_raw = f.read().split("\n")
        volume_groups_raw = [volume_groups_raw[i:i + 21] for i in xrange(0, len(volume_groups_raw), 21)]
        volume_groups = []
        for volume_group in volume_groups_raw:
            if len(volume_group) < 21:
                continue
            vg_name = volume_group[1].replace(" ", "").split("VGName")[1]
            if vg_name == "VolGroup":
                continue
            volume_groups.append({
                "vg_name": volume_group[1].replace(" ", "").split("VGName")[1],
                "vg_access": volume_group[6].replace(" ", "").split("VGAccess")[1],
                "cur_pv": volume_group[12].replace(" ", "").split("CurPV")[1],
                "vg_size": volume_group[14].replace(" ", "").split("VGSize")[1],
                "free_size": volume_group[18].replace(" ", "").split("FreePE/Size")[1].split("/")[1]
            })
        return volume_groups


def _get_target_vg_info(vg_name, sp_name):
    """获得制定 vg 名的 vg 信息

    :param node_obj:
    :param vg_name:
    :return:
    """
    vg_info = {}
    try:
        vgs_info = get_volume_groups()
        target_vg = filter(lambda x: x["vg_name"], vgs_info)
        if target_vg:
            vg_info["name"] = target_vg[0]["vg_name"]
            vg_info["permission"] = target_vg[0]["vg_access"]
            vg_info["free"] = target_vg[0]["free_size"]
            vg_info["total"] = target_vg[0]["vg_size"]
            vg_info["sp"] = sp_name
    except Exception as e:
        print str(e)
    return vg_info


def func_a():
    children = [_get_target_vg_info(None, None)]
    children = sorted(children, key=lambda x: x["name"])
    return children

print list("hello world")
c = func_a()
pass
