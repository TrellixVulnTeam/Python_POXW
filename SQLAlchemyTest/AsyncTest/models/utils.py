#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: utils.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/3/17 4:40 PM
# History:
#=============================================================================
"""
from typing import Union, Optional
from datetime import datetime, timedelta


def convert_utc_to_beijing(dt: datetime, hours: int = 8, format_: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    utc时间转为北京时间
    """
    if not dt:
        return ""
    bj_time = dt + timedelta(hours=hours)
    return bj_time.strftime(format_)


def convert_to_size_str(
        size_num: Union[int, float, str],
        start_unit: str = "B",
        end_unit: Optional[str] = None,
        is_iec: bool = True,
        is_round: bool = True,
        decimal: int = 1,
        sep: str = ' '
) -> str:
    """
    单位自动转换，返回最合适单位的字符类型的大小

    convert_to_size_str(10240, start_unit="kb", end_unit="pb") -> 10.0MB

    :param size_num: 待转换的大小
    :param start_unit: 开始时size对应的大小
    :param end_unit: 结束时size对应的单位
    :param is_iec: 是否使用IEC标准，默认使用，进制是1024
    :param is_round: 是否进行四舍五入，为True时，进行四舍五入；为False时，进行只舍不入
    :param decimal: 保留的小数位数
    :param sep: 连接大小和单位的连接符号
    :return:
    """
    size_num = float(size_num)
    system = 1024 if is_iec else 1000
    multiplier_unit_to_num = {
        'PB': 5,
        'TB': 4,
        'GB': 3,
        'MB': 2,
        'KB': 1,
        'PIB': 5,
        'TIB': 4,
        'GIB': 3,
        'MIB': 2,
        'KIB': 1,
        'B': 0,
    }
    multiplier_num_to_unit = {
        5: 'PB',
        4: 'TB',
        3: 'GB',
        2: 'MB',
        1: 'KB',
        0: 'B',
    }

    # 起始单位和结束单位转换
    start_unit = f"{start_unit}B" if not start_unit.strip().upper().endswith("B") else start_unit
    start_unit_num = multiplier_unit_to_num[start_unit.upper()]

    if end_unit:
        end_unit = f"{end_unit}B" if not end_unit.strip().upper().endswith("B") else end_unit
        end_unit_num = multiplier_unit_to_num.get(end_unit.upper(), None)
    else:
        end_unit_num = None

    # 针对往小单位转换的情况
    if end_unit_num and end_unit_num <= start_unit_num:
        return "{size}{sep}{unit}".format(size=size_num * pow(system, start_unit_num - end_unit_num),
                                          sep=sep,
                                          unit=multiplier_num_to_unit[end_unit_num])

    # 进行转化
    unit: int = start_unit_num
    while size_num // system:
        if unit == 5 or unit == end_unit_num:
            break

        unit += 1
        size_num = float(size_num) / system

    # 根据不同参数，转换成不同类型
    if is_round:
        # 输出数值，四舍五入
        return "{size}{sep}{unit}".format(size="%.{}f".format(decimal) % size_num,
                                          sep=sep,
                                          unit=multiplier_num_to_unit.get(unit) if size_num else 'B')
    else:
        # 2020-06-03: 输出数值，只舍不入
        head, _, tail = str(size_num).partition('.')
        tail = (tail + "0" * decimal)[:decimal]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
        return "{size}{sep}{unit}".format(size=".".join([head, tail]),
                                          sep=sep,
                                          unit=multiplier_num_to_unit.get(unit) if size_num else 'B')
