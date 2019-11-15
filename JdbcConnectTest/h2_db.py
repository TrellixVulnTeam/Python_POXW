"""
@file: h2_db.py
@time: 2019/11/15
@author: alfons
"""
import jaydebeapi

url = "jdbc:h2:tcp://10.10.160.13:9092//var/lib/linstor/linstordb"
user = 'linstor'
password = 'linstor'
dirver = 'org.h2.Driver'
jar = './h2-1.4.196.jar'
##jconn = _jdbc_connect(jclassname, url, driver_args, jars, libs)
conn = jaydebeapi.connect(dirver, url, [user, password], jar)
curs = conn.cursor()

select = "select * from linstordb.linstor.resources"
curs.execute(select)
fundname = curs.fetchall()

curs.close()
conn.close()
