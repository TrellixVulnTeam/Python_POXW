#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: cx_oracle_pool_by_sessionpool.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/2/23 3:48 PM
# History:
#=============================================================================
"""
import cx_Oracle
import logging as log


class OraclePool(object):
    def __init__(self, db_msg, isomerism=False, thread=False):
        """
        创建池
        :param db_msg: 数据库信息   (user, password, dsn)
        :param isomerism: 是否异构
        :param thread: 是否线程
        """
        self.__isomerism = isomerism
        self.__thread = thread
        self.__pool = self.__get_pool(db_msg)
        log.debug(db_msg)

    def __get_pool(self, db_msg):
        """ 创建连接池 """

        if self.__isomerism is True:
            pool = cx_Oracle.SessionPool(dsn=db_msg[2],
                                         homogeneous=False,
                                         min=20, max=50, increment=0,
                                         encoding='UTF-8', threaded=self.__thread)
        else:
            pool = cx_Oracle.SessionPool(db_msg[0], db_msg[1], db_msg[2],
                                         homogeneous=False,
                                         min=20, max=50, increment=0,
                                         encoding='UTF-8', threaded=self.__thread)

        return pool

    def __get_conn(self, voucher=None):
        """ 获取连接 """
        if voucher is None:
            connection = self.__pool.acquire()
            # connection.mode = cx_Oracle.SYSDBA
        else:
            user, password = voucher
            connection = self.__pool.acquire(user, password)
            # connection.mode = cx_Oracle.SYSDBA

        cursor = connection.cursor()

        return connection, cursor

    def __reset_conn(self, connection):
        """ 将连接放回连接池 """
        self.__pool.release(connection)

    def __execute(self, sql, data=None, voucher=None):
        """ 获取连接, 执行sql """
        if voucher is None:
            connection, cursor = self.__get_conn()
        else:
            connection, cursor = self.__get_conn(voucher)

        if data is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, data)

        return connection, cursor

    def fetch_one(self, sql, voucher=None):
        """ 查询一条结果 """
        try:
            if self.__isomerism is True:
                connection, cursor = self.__execute(sql=sql, voucher=voucher)
            else:
                connection, cursor = self.__execute(sql)

            result = cursor.fetchone()
            self.__reset_conn(connection)
            return result
        except Exception as e:
            log.error('FetchOne:' + str(e) + 'SQL:' + sql)

    def fetch_no_result(self, sql, voucher=None):
        """ 查询所有结果 """
        try:
            if self.__isomerism is True:
                connection, cursor = self.__execute(sql=sql, voucher=voucher)
            else:
                connection, cursor = self.__execute(sql)

            cursor.fetchall()
            self.__reset_conn(connection)
            return 'True'
        except Exception as e:
            log.error('FetchAll:' + str(e) + 'SQL:' + sql)

    def fetch_all(self, sql, data=None, voucher=None):
        """ 查询所有结果 """
        try:
            if self.__isomerism is True:
                connection, cursor = self.__execute(sql=sql, data=data, voucher=voucher)
            else:
                if data is None:
                    connection, cursor = self.__execute(sql)
                else:
                    connection, cursor = self.__execute(sql, data)

            result = cursor.fetchall()
            self.__reset_conn(connection)
            return result
        except Exception as e:
            log.error('fetch_all_Binding_variables:' + str(e) + 'SQL:' + sql + str(data))

    def execute_sql(self, sql, data=None, voucher=None):
        """ 执行SQL语句 """
        try:
            if self.__isomerism is True:
                connection, cursor = self.__execute(sql=sql, data=data, voucher=voucher)
            else:
                connection, cursor = self.__execute(sql, data)
            connection.commit()
            self.__reset_conn(connection)
            return True
        except Exception as e:
            log.error('ExecuteSql:' + str(e) + 'SQL:' + sql)

    def executemany_sql(self, sql_template, data_list):
        try:
            connection, cursor = self.__get_conn()
            cursor.executemany(sql_template, data_list)
            connection.commit()
            self.__reset_conn(connection)
            return True
        except Exception as e:
            log.error('executemany_sql:' + str(e) + 'SQL:' + sql_template)

    def __del__(self):
        self.__pool.close()


if __name__ == '__main__':
    # test1 = OraclePool(db_msg='1', thread=True)
    # result = test1.fetch_one('select 1 from dual')
    # print(result)
    #
    # test2 = OraclePool(db_msg='1', isomerism=True)
    # result = test2.fetch_one('select 1 from dual', ('db', 'db'))
    # print(result)

    oracle_pool = OraclePool(('c##test', 'test', '(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.10.90.83)(PORT=1521))(CONNECT_DATA=(SID=yxy1)))'), thread=True)
    # result = oracle_pool.fetch_one("select '11'||to_char(db.SVC_NUMBER_IDSEQ.nextval, 'FM000000000') from dual")
    # print(result)
    sql = """
    SELECT 
    dg.group_number as group_id, 
     dg.name as group_name, 
     d.disk_number as disk_id, 
     d.name as disk_name, 
     d.failgroup as fail_group, 
     d.mode_status as mode_status, 
     d.path as com_path, 
     d.total_mb as total_mb, 
     min(d.free_mb) as free_mb 
    FROM 
     gv$asm_disk d,
     gv$asm_diskgroup dg 
    WHERE 
     d.group_number = dg.group_number 
     AND d.inst_id = dg.inst_id 
    GROUP BY 
     dg.group_number,
     dg.name,
     d.disk_number,
     d.name,
     d.failgroup,
     d.mode_status,
     d.path,
     d.total_mb 
    ORDER BY 
     d.name"""
    print(oracle_pool.fetch_all(sql))
