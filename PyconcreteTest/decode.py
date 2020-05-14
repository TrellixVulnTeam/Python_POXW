#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: decode.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/5/14 下午4:26
# History:
#=============================================================================
"""


import os
import sys
import marshal
from pyconcrete._pyconcrete import decrypt_buffer

pye_dir = "./pye_dir"
pyc_dir = "./pyc_dir"

for file_name in os.listdir(pye_dir):
    with open(os.path.join(pye_dir, file_name), 'rb') as f:
        data = decrypt_buffer(f.read())  # decrypt pye

    if sys.version_info >= (3, 3):
        # reference python source code
        # python/Lib/importlib/_bootstrap_external.py _code_to_bytecode()
        magic = 12
    else:
        # load pyc from memory
        # reference http://stackoverflow.com/questions/1830727/how-to-load-compiled-python-modules-from-memory
        magic = 8

    pyc_code = marshal.loads(data[magic:])