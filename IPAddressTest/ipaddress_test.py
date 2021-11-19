#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: ipaddress_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/12/7 3:38 下午
# History:
#=============================================================================
"""
import ipaddress

ip = ipaddress.ip_address("10.10.100.220")
if ip != None:
    pass

print(str(ipaddress.IPv4Address("10.10.100.220")))

print(ipaddress.ip_network("10.10.100.220", strict=True))
print(str(ipaddress.IPv4Network("10.10.100.220/24", strict=False).network_address))

print(ipaddress.IPv4Network("10.10.100.0/24") in [ipaddress.IPv4Network("10.10.100.0/24")])
