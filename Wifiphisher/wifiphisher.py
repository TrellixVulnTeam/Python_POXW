#!/usr/bin/python
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Wifiphisher.py
@time: 17-6-22 上午9:22
@version: v1.0
"""
import time
import logging
import traceback
import threading
import WWSGC
import subprocess
from subprocess import Popen
import WifiphisherHTTPServer

NETWORK_IP = "192.168.0.0"
NETWORK_GW_IP = "192.168.0.1"
NETWORK_MASK = "255.255.255.0"
DHCP_RANGE = "192.168.0.2,192.168.0.250,255.255.255.0,1h"


class Wifiphisher(threading.Thread):
    def __init__(self):
        self.__interface = None
        self.__ssid = None
        self.__channel = None
        self.__hostapd_cfg_path = None
        self.__dhcp_cfg_path = None
        self.__hostapd_proc = None
        self.__dnsmasq_proc = None
        pass

    def SetParams(self, interface = '', ssid = '', channel = 6, hostapd_cfg_path = '', dhcp_cfg_path = ''):
        '''设置钓鱼AP的启动参数数据。
        interface:              钓鱼AP使用的网卡名字，需为monitor模式
        ssid:                   钓鱼AP的SSID，utf-8编码
        channel:                钓鱼AP的信道
        hostapd_cfg_path:       hostapd对应的配置文件路径
        dhcp_cfg_path:          dhcpd的配置文件路径
        返回：成功返回True，否则False。'''
        if not interface or not ssid:
            logging.debug('设置伪造AP的参数错误！')
            return False
        self.__interface = interface
        self.__ssid = ssid
        self.__channel = channel
        self.__hostapd_cfg_path = hostapd_cfg_path if hostapd_cfg_path else WWSGC.FILE_WifiphisherApCnf()
        self.__dhcp_cfg_path = dhcp_cfg_path if dhcp_cfg_path else WWSGC.FILE_WifiphisherDHCPCnf()
        return True

    def __StartHostapd(self):
        '''开启Hostapd功能'''
        # 钓鱼AP Hostapd配置
        config = ('interface=%s\n'
                  'driver=nl80211\n'
                  'ssid=%s\n'
                  'hw_mode=g\n'
                  'channel=%s\n'
                  'macaddr_acl=0\n'
                  'ignore_broadcast_ssid=0\n') % (self.__interface, self.__ssid, self.__channel)

        try:
            with open(self.__hostapd_cfg_path, 'w', encoding = 'utf-8') as hostapd_conf:
                hostapd_conf.write(config)

            # 启动hostapd进程
            self.__hostapd_proc = Popen([WWSGC.PROG_hostapd(), self.__hostapd_cfg_path], close_fds = True)

            time.sleep(2)
            if self.__hostapd_proc.poll():
                return False
        except:
            return False
        return True

    def __StartDHCP(self):
        '''开启DHCP功能'''
        # 钓鱼AP DHCP配置
        config = ('no-resolv\n'
                  'interface=%s\n'
                  'dhcp-range=%s\n'
                  'address=/#/%s') % (self.__interface, DHCP_RANGE, NETWORK_GW_IP)

        with open(self.__dhcp_cfg_path, 'w', encoding = 'utf-8') as dhcp_cnf:
            dhcp_cnf.write(config)

        # 开启dnsmasq
        self.__dnsmasq_proc = Popen(['dnsmasq', '-C', self.__dhcp_cfg_path], close_fds = True)

        # 设置网卡地址
        Popen(['ifconfig', str(self.__interface), 'up', NETWORK_GW_IP, 'netmask', NETWORK_MASK], close_fds = True)
        time.sleep(.5)

        # 检测网卡是否正确配置
        proc = subprocess.check_output(['ifconfig', str(self.__interface)])
        if NETWORK_GW_IP not in proc:
            return False

        # 添加路由功能
        cmd = 'route add -net %s netmask %s gw %s' % (NETWORK_IP, NETWORK_MASK, NETWORK_GW_IP)
        Popen(cmd, close_fds = True)
        return True

    def __StartHTTPServer(self):
        pass

    def StartWifiphisher(self):
        '''启动钓鱼AP。'''
        try:
            if self.is_alive():
                logging.debug('钓鱼AP已经启动，不能重新启动!')
                return False
        except:
            logging.debug("%s" % traceback.format_exc())
            return False
        self.start()
        return True

    def Stop(self):
        '''外部要求停止供给功能'''
        try:
            if self.is_alive():
                self.join()
        except:
            logging.debug("%s" % traceback.format_exc())
            pass

        if self.__dnsmasq_proc is not None:
            WWSGC.KillProcByPIDAndName(self.__dnsmasq_proc.pid, 'dnsmasq')
        if self.__hostapd_proc is not None:
            WWSGC.KillProcByPIDAndName(self.__hostapd_proc.pid, 'hostapd')

    def run(self):
        '''重载线程运行函数'''
        logging.info('线程【钓鱼AP工作】启动')
        # 启动hostapd
        if not self.__StartHostapd():
            return False

        # 启动dnsmasq
        if not self.__StartDHCP():
            return False

        # 启动HTTP服务器
        if not self.__StartHTTPServer():
            return False
        pass
