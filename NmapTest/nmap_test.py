"""
@file: nmap_test.py
@time: 2019/10/8
@author: alfons
"""
import nmap

scaner = nmap.PortScannerAsync()
res = scaner.scan(hosts="10.10.100.0/24", arguments="-sP")
print(res)
pass