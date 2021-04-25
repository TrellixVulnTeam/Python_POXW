#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: ECC_eciespy.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/4/22 5:19 下午
# History:
#=============================================================================
"""
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k = generate_eth_key()
private_key = eth_k.to_hex()  # hex string
public_key = eth_k.public_key.to_hex()  # hex string

data = b'this is a test'
cipher_text = encrypt(public_key, data)
plain_text = decrypt(private_key, cipher_text)

print(f"{data=}")
print(f"{cipher_text=}")
print(f"{pla}")
