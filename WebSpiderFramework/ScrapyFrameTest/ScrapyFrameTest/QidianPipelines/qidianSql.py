"""
@file: sql.py
@time: 2018/11/30
@author: sch
"""
import sys
import pymysql

sql_host = "127.0.0.1"
sql_username = "alfons"
sql_password = "xiaohui"
sql_port = "3306"
sql_dbname = "qidian"
sql_charset = "utf8"


class QidianDb:
    db = None
    cursor = None  # 游标

    @classmethod
    def OpenDB(cls):
        """
        打开数据库
        :return:
        """
        try:
            cls.db = pymysql.connect(host = sql_host,
                                     port = int(sql_port),
                                     db = sql_dbname,
                                     user = sql_username,
                                     passwd = sql_password,
                                     charset = sql_charset)

            cls.cursor = cls.db.cursor()  # 游标
        except:
            print("Open db fail!")
            sys.exit(0)

    @classmethod
    def CloseDB(cls):
        """
        关闭数据库
        :return:
        """
        cls.db.close()

    @classmethod
    def insert_table(cls, novel_id, novel_name, novel_link, man_type, sub_type, author_id, author_name, author_link):
        insert_sql = "insert into novel_info(`novel_id`, `novel_name`, `novel_link`, `man_type`, `sub_type`, `author_id`, `author_name`, `author_link`)" \
                     " values (%(novel_id)s, %(novel_name)s, %(novel_link)s, %(man_type)s, %(sub_type)s, %(author_id)s, %(author_name)s, %(author_link)s)"
        values = dict(novel_id = novel_id, novel_name = novel_name, novel_link = novel_link,
                      man_type = man_type, sub_type = sub_type,
                      author_id = author_id, author_name = author_name, author_link = author_link)

        cls.cursor.execute(insert_sql, values)
        cls.db.commit()

    @classmethod
    def select_unique_novel_id(cls, novel_id):
        select_sql = "select exists(select 1 from novel_info where novel_id=%(novel_id)s)"
        value = dict(novel_id = novel_id)
        cls.cursor.execute(select_sql, value)
        target = cls.cursor.fetchall()[0]
        return target


def IsNovelExist(novel_id):
    """
    判断小说ID是否在数据库中存在
    :param novel_id: 小说编号
    :return: 存在返回True，不存在返回False
    """
    return QidianDb.select_unique_novel_id(novel_id)[0] == 1


if __name__ == '__main__':
    QidianDb.insert_table("213", "haoya", "heep://baidu.com", "休闲", "网络", "21321", "jk", "heet://google")
