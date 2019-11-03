#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: Changescp.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2019/10/24 上午10:42
# History:
#=============================================================================
"""
import os
import logging
import subprocess


class sshCls:
    """Oracle 19c install in Redhat 7.5"""

    def __init__(self):

        # 用于修复ssh导致安装时互信不能通过的bug
        self.ssh_version = self.__get_ssh_version()
        self.scp_src_path = "/usr/bin/scp"
        self.scp_dst_path = "/usr/bin/scp.orig"

    @staticmethod
    def __get_ssh_version():
        """
        获取本机上的ssh版本
        """
        try:
            p = subprocess.Popen("ssh -V", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_str = p.stderr.read()
            if isinstance(stdout_str, str):
                return stdout_str[8:stdout_str.find('.')]
        except Exception as e:
            logging.warning("Get ssh version warning!\n{error}".format(error=str(e)))
        return

    def ssh_bug_fix_start(self):
        """
        ssh8.x版本，在安装19c时会出现ssh连接不了的问题，需要做些处理
        :return:
        """

        if self.ssh_version in ['7']:
            if os.path.isfile(self.scp_src_path) and os.path.isfile(self.scp_dst_path):
                return

            if os.path.isfile(self.scp_src_path) and not os.path.isfile(self.scp_dst_path):
                os.system("mv {src} {dst} -f".format(src=self.scp_src_path, dst=self.scp_dst_path))
                os.system("echo '{dst} -T $*' > {src}".format(src=self.scp_src_path, dst=self.scp_dst_path))
                os.system("chmod +x {src}".format(src=self.scp_src_path))
                return

    def ssh_bug_fix_end(self):
        """
        还原scp文件
        :return:
        """
        if self.ssh_version in ['7'] and os.path.isfile(self.scp_dst_path):
            os.system("mv {dst} {src} -f".format(src=self.scp_src_path, dst=self.scp_dst_path))


if __name__ == '__main__':
    ssh_obj = sshCls()
    ssh_obj.ssh_bug_fix_start()
    ssh_obj.ssh_bug_fix_end()
