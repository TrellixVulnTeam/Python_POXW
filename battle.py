# -*- coding: utf-8 -*-
import os
import random
import logging
import time
import sys
import cx_Oracle
import paramiko

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename='/tmp/automatictest.log',
                    filemode='a')


def conndb():
    ##创建数据库连接，设置默认值
    dsn = cx_Oracle.makedsn('10.10.160.233', 1521, 'orcl1')
    db = cx_Oracle.connect('system', 'oracle', dsn)
    return db


def SelectDB(db, sql):
    ##select 查询
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    return result


def DMLDB_N(db, sql):
    ##插入，更新，删除
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()
    db.commit()


def DDLDB(db, sql):
    # DDL 语句
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()


def printResult(rs):
    for row in rs:
        print   row


def checkifinrebalance():
    '''
    检察是否处于重平衡
    使用linstor r l 检察是否有资源状态不是uptodate，如果有那么认为正处于重平衡之中
    返回False表示正在重平衡,返回True表示重平衡完成
    '''
    resource_status = os.popen('linstor r l -p  | grep -E "InUse|Unused"').readlines()
    for status in resource_status:
        if "UpToDate" in status:
            continue
        else:
            logging.info("检测到正处于重平衡中，不进行断存储测试")
            return False
    logging.info("未检测到重平衡")
    return True


def shutdownstornode():
    '''
    随机挑一台存储节点进行ipmitool power reset操作
    :return:
    '''
    ipmi_ip = "10.10.160.17" + str(random.randint(3, 6))
    command = "ipmitool -I lanplus -H %s -U admin -P Password@_ power status" % ipmi_ip
    logging.info('执行' + command)
    cmd_out = os.system(command)
    if cmd_out == 0:
        try:
            command = "ipmitool -I lanplus -H %s -U admin -P Password@_ power off" % ipmi_ip
            logging.info('执行' + command)
            os.system(command)
            logging.info("带外IP %s 关机" % ipmi_ip)
            return ipmi_ip
        except Exception as e:
            logging.error(e)
    else:
        logging.warn("连接ipmi出错")


def checkenv():
    if checkifinrebalance() or time.sleep(60) and checkifinrebalance():
        return True
    else:
        return False


def checkstonode():
    '''
    如果有存储节点不能连通则返回false
    :return:
    '''
    for ip in range(203, 206):
        cmd_exit_code = os.system("ping -c 1 10.10.160.%s" % ip)
        if cmd_exit_code != 0:
            logging.info("ping存储节点%s异常" % s)
            return False
        else:
            logging.info("所有存储节点都能正常连通")
            return True


def powerup_stor(ip=None):
    '''
    将之前测试时关机的机器开起来
    :param ip:
    :return:
    '''
    if ip != None:
        try:
            command = "ipmitool -I lanplus -H %s -U admin -P Password@_ power on" % ipmi_ip
            os.system(command)
            logging.info("带外IP %s 开机" % ip)
        except Exception as e:
            logging.error(e)
    else:
        logging.error("powerup_stor error ,var ip is " + ip)
        sys.exit(1)


def checkoralcedb():
    db = conndb()
    try:
        ddl = 'create table zntab(id number,val varchar2(20))'
        logging("创建oracle zntab表")
    except Exception as e:
        print(e)
    sel = 'select * from zntab'
    rs = SelectDB(db, sel)
    logging.info(rs)
    inst = 'insert into zntab values(06,\'zlf\')'
    logging.info("尝试插入数据")
    try:
        DMLDB_N(db, inst)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
    rs = SelectDB(db, sel)
    logging.info(rs)
    return True


def get_offline_stor_node():
    cmd = """linstor  n l | grep OFFLINE | awk '{print $6}' | awk -F : '{print $1}'"""
    offline_node_ip = os.popen(cmd).readlines()[0].rstrip("\n")
    cmd = """linstor  n l | grep OFFLINE | awk '{print $2}' | awk -F : '{print $1}'"""
    offline_node_name = os.popen(cmd).readlines()[0].rstrip("\n")
    if offline_node_name and offline_node_ip:
        return offline_node_ip, offline_node_name


def clear_qlink(node_name=''):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.10.160.201', port=22, username='root', password='cljslrl0620')
    stdin, stdout, stderr = ssh.exec_command('api-qdatamgr qlink delete -s %s' % node_name)
    logging.info(stdout.read().decode())


def clear_cfile(ip=''):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=22, username='root', password='cljslrl0620')
    stdin, stdout, stderr = ssh.exec_command('qdatamgr conf sync -g -i 10.10.160.201')
    logging.info(stdout.read().decode())


def clear_com_nvme_controller():
    '''
    写死计算节点为201 202
    :return:
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.10.160.201', port=22, username='root', password='cljslrl0620')
    stdin, stdout, stderr = ssh.exec_command('/bin/bash /root/clear.sh')
    logging.info("计算节点一清理nvme控制器")
    logging.info(stdout.read().decode())
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='10.10.160.202', port=22, username='root', password='cljslrl0620')
    stdin, stdout, stderr = ssh.exec_command('/bin/bash /root/clear.sh')
    logging.info("计算节点二清理nvme控制器")
    logging.info(stdout.read().decode())


if __name__ == '__main__':
    while True:
        if checkenv() and checkstonode() and checkoralcedb():
            logging.info('-------------------------------')
            a = shutdownstornode()
            logging.info('sleep 60s ，等待掉线节点linstor状态转换为offline')
            time.sleep(60)
            offline_node_ip, offline_node_name = get_offline_stor_node()
            logging.info("此次断掉的节点为%s，ip为%s" % (offline_node_name, offline_node_ip))
            if checkenv():
                logging.info("等待重平衡结束后执行api-qdatamgr qlink delete -s ")
                clear_qlink(node_name=offline_node_name)
        while True:
            if checkenv():
                powerup_stor(ip=a)
                logging.info('等待服务器开机,sleep 200s')
                time.sleep(200)
                logging.info('尝试ping掉线节点')
                com_return = os.system('ping -c %s' % offline_node_ip)
                if com_return == 0:
                    logging.info('清理掉线节点%s cfile' % offline_node_ip)
                    clear_qlink(ip=offline_node_ip)
                    clear_com_nvme_controller()
                    break
                else:
                    continue
            else:
                logging.info("sleep 60s，等待重平衡")
                time.sleep(60)
