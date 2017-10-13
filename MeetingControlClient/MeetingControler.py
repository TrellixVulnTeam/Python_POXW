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
import time
import datetime
import struct
import random
import binascii

num_dig = "0123456789"

commond_hdr = struct.Struct('< I c I H H c c')
message_hdr = struct.Struct('< H H')

CMD_BEG = 0
CMD_END = 15
MES_BEG = 0
MES_END = 4

CMD_LEN_INDEX = 0
CMD_INDEX = 5
MES_LEN_INDEX = 0
MES_INDEX = 1

TRANS_fb = "0x32"
GSM_fb = "0x33"
Voice_fb = "0x1d"
SMS_FB = "0x1e"
# feedback_cmd_list = [TRANS_fb]
feedback_cmd_list = [TRANS_fb, GSM_fb, Voice_fb, SMS_FB, "0x22"]

IMSI_TYPE = "0x50"
IMEI_TYPE = "0x51"
PHONE_TYPE = "0x5d"
Maclist = []


def DataJudge(data):
    """
    数据判断
    :param data: 数据
    :return: 数据正确返回True，失败False
    """
    if data == "" or not data:
        return False

    for i in range(0, len(data)):
        if data[i] not in num_dig:
            return False
    return True


class MeetingControler:
    def __init__(self, config_path):
        """
        初始化
        :param config_path: 配置文件路径
        """
        self.__db_connect = None  # 数据库连接
        self.__db_host = None  # 数据库地址
        self.__db_port = None  # 数据库端口
        self.__db_name = None  # 数据库名字
        self.__db_user = None  # 数据库登陆用户名
        self.__db_pass = None  # 数据库登陆密码
        self.__db_char = None

        self.__socketer = None  # socket连接
        self.__sock_dev_host = None  # 设备端socket的ip地址
        self.__sock_dev_port = None  # 设备端socket端口
        self.__sock_con_host = None  # 控制端socket的ip地址
        self.__sock_con_port = None  # 控制端socket端口

        self.__dev_address = None  # 设备地址
        self.__con_address = None  # 本地监听地址

        self.__Cache = {}
        self.__mac_cache = []

        if config_path is None:
            self.__config_path = "./MeetingControl.xml"
        else:
            self.__config_path = config_path

    def __Init(self):
        """
        初始化操作
        :return:
        """
        try:
            self.__InitDB()
            self.__InitSocket()
        except:
            logging.error("初始化DB或socket错误 %s" % traceback.format_exc())
            return False
        return True

    def __InitDB(self):
        """
        初始化数据库连接
        :return:
        """
        self.__db_connect = MySQLdb.connect(host = self.__db_host,
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

    def __SetConfig(self):
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
        self.__db_port = int(DB_node.getAttribute("port"))
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

    def __MySqlStore(self, imsi, imei, phone, mac):
        """
        存入mysql
        :param imei: imei
        :param imsi: imsi
        :param phone: 电话号码
        :param mac: mac地址
        :return:
        """
        try:
            sys_time = int(time.mktime(datetime.datetime.now().utctimetuple()))
            cursor = self.__db_connect.cursor()

            sql = "insert into virtual_info(id_type, mac, `time`, user_name,password,srv_host,collecting_device_id) values(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (int(3), mac, sys_time, imsi, "", "", int(10086)))
            cursor.execute(sql, (2, mac, sys_time, imei, "", "", 10086))
            cursor.execute(sql, (1, mac, sys_time, phone, "", "", 10086))
            self.__db_connect.commit()
        except:
            logging.error(traceback.format_exc())
            pass

    def __RandMac(self):
        """
        随机生成mac地址，保证不在macCache中重复出现
        :return: 生成的mac地址
        """
        for i in range(1, 7):
            RANDSTR = "".join(random.sample("0123456789abcdef", 2))
            Maclist.append(RANDSTR)
        RANDMAC = ":".join(Maclist)
        if RANDMAC in self.__mac_cache:
            return self.__RandMac()
        return RANDMAC

    def __DealMessage(self, message):
        """
        分解信息
        :param message: 接收到的多个信息单元集合
        :return:
        """
        try:
            IMSI = None
            IMEI = None
            Phone = None
            while message:
                mes_obj = message_hdr.unpack(message[MES_BEG:MES_END])
                mes_len = mes_obj[MES_LEN_INDEX]
                mes_type = hex(mes_obj[MES_INDEX])
                mes_body = message[MES_END:mes_len].strip("\0")

                if mes_type == IMSI_TYPE:
                    IMSI = mes_body
                elif mes_type == IMEI_TYPE:
                    IMEI = mes_body
                elif mes_type == PHONE_TYPE:
                    Phone = mes_body
                message = message[mes_len:]

            if not DataJudge(IMSI) \
                    and not DataJudge(IMEI):
                return

            virtual_info = self.__Cache.get(IMSI, []) if self.__Cache != {} else None
            if not virtual_info:
                Phone = Phone if DataJudge(Phone) else ""
                mac = self.__RandMac()
                self.__Cache.update({IMSI: [IMSI, IMEI, Phone, mac]})
                self.__MySqlStore(IMSI, IMEI, Phone, mac)
            else:
                last_phone = virtual_info[2]
                mac = virtual_info[3]
                if last_phone == "" and DataJudge(Phone):
                    self.__Cache.update({IMSI: [IMSI, IMEI, Phone, mac]})
                    self.__MySqlStore(IMSI, IMEI, Phone, mac)
        except:
            logging.error(traceback.format_exc())

    def __ReceiveMessage(self):
        """
        处理接收到的信息
        :return:
        """
        while True:
            try:
                data = self.__socketer.recv(2048)
                cmd_obj = commond_hdr.unpack(data[CMD_BEG:CMD_END])
                cmd_len = cmd_obj[CMD_LEN_INDEX]
                cmd_code = hex(ord(cmd_obj[CMD_INDEX]))
                if len(data) != cmd_len \
                        or cmd_code not in feedback_cmd_list:
                    continue
                message = data[CMD_END:]
                self.__DealMessage(message)
            except:
                pass

    def Start(self):
        """
        程序开始
        :return:
        """
        if not self.__SetConfig():
            return

        if not self.__Init():
            return

        self.__ReceiveMessage()


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
    args = ParseArgs()
    mettingControl = MeetingControler(args.config)
    mettingControl.Start()
    pass
