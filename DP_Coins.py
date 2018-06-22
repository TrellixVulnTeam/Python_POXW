#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : DP_Coins.py
 @Time    : 2018/6/22 9:31
"""
coins = [1 , 2]

infity = float("inf")
d = dict()

def DP_Conis(num):
    d[0] = 0
    for i in range(1, num + 1):
        d[i] = infity

        for coin in coins:
            if i >= coin and d[i - coin] + 1 < d[i]:
                d[i] = d[i - coin] + 1

    print(d.values())

DP_Conis(10)