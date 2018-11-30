"""
@file: sql.py
@time: 2018/11/30
@author: sch
"""
import pymysql

sql_host = "127.0.0.1"
sql_username = "root"
sql_password = "ygwifidb_password"
sql_port = "3306"
sql_dbname = "qidian"
sql_charset = "utf8"

db = pymysql.connect(host = sql_host,
                     port = int(sql_port),
                     db = sql_dbname,
                     user = sql_username,
                     passwd = sql_password,
                     charset = sql_charset)
