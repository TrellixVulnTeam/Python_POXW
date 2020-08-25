#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: arg_hook.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/8/25 3:01 下午
# History:
#=============================================================================
"""
import argparse


# 1. 使用参数处理之外的方法实现
def convert_size(values, default_unit="GB"):
    if isinstance(values, (str, bytes)):
        values = str(values)

        # 输入合法性判断
        if set(values.upper()) - set("0123456789.BKMGTP"):
            raise ValueError("Input size {v} not available.".format(v=values))

        # 输入单位判断，需要判断小数点位数，如果大于一个，不是数字类型
        for unit_char in list("BKMGTP."):
            if values.upper().count(unit_char) > 1:
                raise ValueError("Input size {v} error.".format(v=values))

        # 如果只输入数字，则添加上默认的单位后缀
        if not set(values.strip()) - set("0123456789."):
            values = str(float(values)) + default_unit

        return values


# 2. 使用自定义action对象实现
class _StoreSizeAction(argparse._StoreAction):
    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, (str, bytes)):
            values = str(values)

            # 输入合法性判断
            if set(values.upper()) - set("0123456789.BKMGTP"):
                parser.error("Input size {v} not available.".format(v=values))

            # 输入单位判断，小数点位数也需要判断，大于一个点，将不是数字类型
            for unit_char in list("BKMGTP."):
                if values.upper().count(unit_char) > 1:
                    parser.error("Input size {v} error.".format(v=values))

            # 如果只输入数字，则添加上默认的单位后缀
            if not set(values.strip()) - set("0123456789."):
                values = str(float(values)) + "GB"

        setattr(namespace, self.dest, values)


def get_parser():
    parser = argparse.ArgumentParser(description="Test size hook")
    parser.add_argument("-s", "--size",
                        required=True,
                        action="store",
                        # action=_StoreSizeAction,
                        type=convert_size,
                        dest="size",
                        default="",
                        help="Specify one size, eg: 1T、200GB. "
                             "Default unit is GB. ")
    return parser


def run():
    parser = get_parser()

    args = parser.parse_args()
    # args.size = convert_size(args.size)
    print(f"{args.size=}")


if __name__ == '__main__':
    run()
