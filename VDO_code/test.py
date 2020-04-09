#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: test.py.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/4/8 下午3:38
# History:
#=============================================================================
"""
# import os
# from statistics.VDOStatistics import VDOStatistics
#
# vdo_statistics = VDOStatistics()
# stat = vdo_statistics._getCClass()()
# exist = os.path.exists("/proc/vdo/QP0B00S08/dedupe_stats")
# with open("/proc/vdo/QP0B00S08/dedupe_stats", 'rb') as f:
#     f.readinto(stat)

# print vdo_statistics.labeled(sample=vdo_statistics.getSamples())

from ctypes import Structure, c_char, c_bool, c_byte, c_ulong, c_ulonglong, c_uint


class VDOStatistics(Structure):
    _fields_ = [
        ("version", c_uint),
        ("releaseVersion", c_uint),
        ("dataBlocksUsed", c_ulonglong),
        ("overheadBlocksUsed", c_ulonglong),
        ("logicalBlocksUsed", c_ulonglong),
        ("physicalBlocks", c_ulonglong),
        ("logicalBlocks", c_ulonglong),
        ("oneKBlocks", c_ulonglong),
        ("oneKBlocksUsed", c_ulonglong),
        ("oneKBlocksAvailable", c_ulonglong),
        ("usedPercent", c_byte),
        ("savings", c_byte),
        ("savingPercent", c_byte),
        ("blockMapCacheSize", c_ulonglong),
        ("writePolicy", c_char * 15),
        ("blockSize", c_ulonglong),
        ("completeRecoveries", c_ulonglong),
        ("readOnlyRecoveries", c_ulonglong),
        ("mode", c_char * 15),
        ("inRecoveryMode", c_bool),
        ("recoveryPercentage", c_byte),

    ]
