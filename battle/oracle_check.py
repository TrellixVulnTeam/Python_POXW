"""
@file: oracle_check.py
@time: 2020/4/3
@author: alfons
"""
import os
import logging


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


def check_oralce_db():
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
