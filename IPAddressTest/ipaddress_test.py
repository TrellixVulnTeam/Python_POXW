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

ip_a = ipaddress.IPv4Address("172.16.128.22")
ip_b = ipaddress.ip_interface(address=ip_a)
ip_c = ipaddress.ip_network(address=f"{ip_a}/24", strict=False)

print(f"{ip_a=}")
print(f"{ip_b=}")
print(f"{ip_c=}")
print(f"{ip_b in ip_c = }")

ip_d = ipaddress.IPv4Address("172.16.129.23")
print(f"{ip_d=}")
print(f"{ip_d in ip_c = }")

print("\n", '*' * 64)
ib_a = ipaddress.IPv4Interface("172.16.128.22/255.255.255.0")
ib_b = ipaddress.IPv4Interface("172.16.129.22/255.255.255.0")

print(f"{ib_a.network=}")
print(f"{ib_b.network=}")
print(f"{ib_a.network == ib_b.network = }")

print(f"{ib_a.netmask=}")
print(f"{ib_b.netmask=}")
print(f"{ib_a.netmask == ib_b.netmask = }")

# print(str(ipaddress.IPv4Address("10.10.100.220/24")))
print(str(ipaddress.IPv4Address("10.10.100.220")))
print(str(ipaddress.IPv4Interface("10.10.100.220/24")))
print(str(ipaddress.IPv4Network("10.10.100.220/24", strict=False)))

# print(ipaddress.ip_network("10.10.100.220", strict=True))
# print(str(ipaddress.IPv4Network("10.10.100.220/24", strict=False).network_address))
#
# print(ipaddress.IPv4Network("10.10.100.0/24") in [ipaddress.IPv4Network("10.10.100.0/24")])
