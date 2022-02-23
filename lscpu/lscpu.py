#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: lscpu.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/12/22 8:40 PM
# History:
#=============================================================================
"""
values = {"Vendor ID": "-1"}
vendor = values.get("Vendor ID", "N/A")
print({
          "0x41": "ARM",
          "0x42": "Broadcom",
          "0x43": "Cavium",
          "0x44": "DEC",
          "0x46": "FUJITSU",
          "0x48": "HiSilicon",
          "0x49": "Infineon",
          "0x4d": "Motorola/Freescale",
          "0x4e": "NVIDIA",
          "0x50": "APM",
          "0x51": "Qualcomm",
          "0x53": "Samsung",
          "0x56": "Marvell",
          "0x61": "Apple",
          "0x66": "Faraday",
          "0x69": "Intel",
          "0x70": "Phytium",
          "0xc0": "Ampere",
      }.get(vendor, vendor))
