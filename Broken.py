#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: Broken.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/3/1 17:52
# History:
#=============================================================================
"""
import os

key_list = [
    "QRQ4N-4TGD8-J2X36-BJYY9-6CQGY",
    "TPYNC-4J6KF-4B4GP-2HD89-7XMP6",
    "2BXNW-6CGWX-9BXPV-YJ996-GMT6T",
    "NRTT2-86GJM-T969G-8BCBH-BDWXG",
    "XC88X-9N9QX-CDRVP-4XV22-RVV26",
    "TNM78-FJKXR-P26YV-GP8MB-JK8XG",
    "TR8NX-K7KPD-YTRW3-XTHKX-KQBP6",
    "VK7JG-NPHTM-C97JM-9MPGT-3V66T",
    "NPPR9-FWDCX-D2C8J-H872K-2YT43",
    "W269N-WFGWX-YVC9B-4J6C9-T83GX",
    "NYW94-47Q7H-7X9TT-W7TXD-JTYPM",
    "NJ4MX-VQQ7Q-FP3DB-VDGHX-7XM87",
    "Mp7W-N47XK-V7XM9-C7227-GCQG9",
]

cmd = """slmgr /ipk {key}
slmgr /skms kms.xspace.in
slmgr /ato"""

for key in key_list:
    p = os.popen(cmd.format(key=key))
    stdout = p.read()
    print("stdout: {}".format(stdout))
    # print("stderr: {}".format(stderr))
    pass
