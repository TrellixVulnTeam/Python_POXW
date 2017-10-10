#!/usr/bin/env python  
# encoding: utf-8  
"""
@file: MeetingControler.py
@author: shangchenhui
@time: 2017/10/10 10:57 
@version: v1.0 
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import argparse
import socket
import MySQLdb
import xml.dom.minidom
import logging
import traceback


class MeetingControler:
    def __init__(self, config_path):
        """
        初始化
        :param config_path: 配置文件路径
        """
        self.__db = None             # 数据库连接
        self.__db_host = None        # 数据库地址
        self.__db_port = None        # 数据库端口
        self.__db_name = None        # 数据库名字
        self.__db_user = None        # 数据库登陆用户名
        self.__db_pass = None        # 数据库登陆密码
        self.__db_char = None

        self.__socketer = None       # socket连接
        self.__sock_dev_host = None      # 设备端socket的ip地址
        self.__sock_dev_port = None      # 设备端socket端口
        self.__sock_con_host = None      # 控制端socket的ip地址
        self.__sock_con_port = None      # 控制端socket端口

        self.__dev_address = None   # 设备地址
        self.__con_address = None   # 本地监听地址

        if config_path is None:
            self.__config_path = "./MeetingControl.xml"
        else:
            self.__config_path = config_path

    def __InitDB(self):
        """
        初始化数据库连接
        :return:
        """
        self.__db = MySQLdb.connect(host = self.__db_host,
                                    port = self.__db_port,
                                    db = self.__db_name,
                                    user = self.__db_user,
                                    passwd = self.__db_pass,
                                    charset = self.__db_char)

    def __InitSocket(self):
        """
        初始化socket连接
        :return:
        """
        self.__dev_address = (self.__sock_dev_host, self.__sock_dev_port)

        self.__socketer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__con_address = (self.__sock_con_host, self.__sock_con_port)
        self.__socketer.bind(self.__con_address)

    def SetConfig(self):
        """
        设置参数
        :return: 成功返回True，异常返回False
        """
        try:
            dom = xml.dom.minidom.parse(self.__config_path)
            root_node = dom.documentElement
            self.__SetDBConfig(root_node)
            self.__SetSocketConfig(root_node)
        except:
            logging.error("读取配置文件%s错误。\n%s" % (self.__config_path, traceback.format_exc()))
            return False
        return True

    def __SetDBConfig(self, root):
        """
        设置数据库参数
        :param root: 配置文件根节点
        :return:
        """
        DB_node = root.getElementsByTagName('MySqlDB')[0]
        self.__db_host = DB_node.getAttribute("host")
        self.__db_port = DB_node.getAttribute("port")
        self.__db_name = DB_node.getAttribute("dbname")
        self.__db_user = DB_node.getAttribute("username")
        self.__db_pass = DB_node.getAttribute("password")
        self.__db_char = DB_node.getAttribute("charset")

    def __SetSocketConfig(self, root):

        """
        设置socket参数
        :param root: 配置文件根节点
        :return:
        """
        socket_node = root.getElementsByTagName('Socket')[0]
        self.__sock_dev_host = socket_node.getAttribute("dev_host")
        self.__sock_dev_port = int(socket_node.getAttribute("dev_port"))
        self.__sock_con_host = socket_node.getAttribute("control_host")
        self.__sock_con_port = int(socket_node.getAttribute("control_port"))

    def __SendMessage(self, message):
        self.__socketer.sendto()
        pass

    def __ReceiveMessage(self):
        pass

    def __MysqlStore(self):
        pass

    def Start(self):
        pass


def ParseArgs():
    """
    参数读取
    :return: 参数
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help = 'Metting control config path.')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 6544))
    for data in ["lgdgod", "nvgod", "大吉大利"]:
        s.sendto(data, ("192.168.2.174", 6555))
        rece, addr = s.recvfrom(1024)
        print rece + "%s:%s" % addr
    # args = ParseArgs()
    # mettingControl = MeetingControler(args.config)
    # if mettingControl.SetConfig():
    #     mettingControl.Start()
    # pass
