#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: pvs_stdout.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2019/11/4 下午3:21
# History:
#=============================================================================
"""
import os


class Ssh:
    def run_cmd(self, cmd):
        return os.system(cmd)


def get_physical_volumes(ssh, vg_list=None):
    """
    获取物理卷对应的信息
    :param ssh:
    :param vg_list:
    :return:
    """
    pvs_stdout = ssh.run_cmd("sudo pvs | awk 'NR == 1 {next} {print $1, $2}'")

    pass


if __name__ == '__main__':
    ssh = Ssh()
    get_physical_volumes(ssh)