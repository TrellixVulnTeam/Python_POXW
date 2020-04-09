#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: ctype_test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/4/9 上午11:43
# History:
#=============================================================================
"""
import ctypes

"""
typedef struct _user {
    int type;
    uint64_t  userid;
    char username[64];
    unsigned int created_at;
} user;
"""

class User(ctypes.Structure):
    _fields_ = [
        ('type', ctypes.c_int),
        ('userid', ctypes.c_uint64),
        ('username', ctypes.c_char * 64),
        ('created_at', ctypes.c_uint),
    ]


print ctypes.POINTER(User)  # <class '__main__.LP_User'>
u = User(userid=19)
print ctypes.pointer(u)  # <__main__.LP_User object at 0x10982c7a0>