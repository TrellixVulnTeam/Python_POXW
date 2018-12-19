"""
@file: SqlAlchemyCoreDemo.py
@time: 2018/09/27
@author: sch
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

# 创建引擎
engine = create_engine("sqlite:///./memory.db", echo = True)

# 元数据绑定引擎
metadata = MetaData(engine)

# 创建表结构
users = Table("users", metadata,
              Column("id", Integer, autoincrement = True, default = 0, primary_key = True, comment = "用户ID"),
              Column("name", String, comment = "用户名"),
              Column("fullname", String, comment = "用户全名"))

addresses = Table("addresses", metadata,
                  Column("id", Integer, primary_key = True, comment = "地址ID"),
                  Column("user_id", None, ForeignKey("users.id"), comment = "关联的用户ID"),
                  Column("email_address", String, nullable = False, comment = "邮箱地址"))


def GetTables():
    from sqlalchemy.engine import reflection

    insp = reflection.Inspector.from_engine(engine)
    print(insp.get_table_names())


def DropTables():
    metadata.drop_all(engine)


def CreateTables():
    # 创建表，方式一
    users.create(checkfirst = True)
    addresses.create(checkfirst = True)

    # 创建表，方式二
    # metadata.create_all(engine)


def InsertData():
    conn = engine.connect()

    ins1 = users.insert(values = [dict(name = "alfons", fullname = "alfons_xh"), {"id": 1, "name": "alfons", "fullname": "alfons_xh"}])
    conn.execute(ins1)

    ins2 = users.insert().values([dict(id = 2, name = "alfons", fullname = "alfons_xh"), {"id": 3, "name": "alfons", "fullname": "alfons_xh"}])
    conn.execute(ins2)

    ins3 = users.insert()
    ins3.execute(dict(id = 4, name = "alfons", fullname = "alfons_xh"), {"id": 5, "name": "alfons", "fullname": "alfons_xh"})

    conn.execute("insert into users (name, fullname) values ('alfons', 'alfons_xh'), ('alfons', 'alfons_xh')")

    conn.execute("insert into users (name, fullname) values (?, ?)", ('alfons', 'alfons_xh'), ('alfons', 'alfons_xh'))

    conn.execute(users.insert(), dict(id = 10, name = "alfons", fullname = "alfons_xh"), {"id": 11, "name": "alfons", "fullname": "alfons_xh"})
    conn.execute(users.insert(), [dict(id = 12, name = "alfons", fullname = "alfons_xh"), {"id": 13, "name": "alfons", "fullname": "alfons_xh"}])

    from sqlalchemy.sql import insert

    ins4 = insert(users).values([dict(id = 14, name = "alfons", fullname = "alfons_xh"), {"id": 15, "name": "alfons", "fullname": "alfons_xh"}])
    conn.execute(ins4)


def InsertAllData():
    conn = engine.connect()

    conn.execute(users.insert(), [
        dict(id = 101, name = "Tom", fullname = "Tom Jhon"),
        dict(id = 102, name = "Peter", fullname = "Peter Jhon"),
        dict(id = 103, name = "Jim", fullname = "Jim Jhon"),
        dict(id = 104, name = "Sofar", fullname = "Sofar jhon"),
        dict(id = 105, name = "Alfons", fullname = "Alfons xh"),
    ])

    conn.execute(addresses.insert(), [
        dict(id = 4, user_id = 101, email_address = "tom@gmail.com"),
        dict(id = 3, user_id = 102, email_address = "peter@gmail.com"),
        dict(id = 2, user_id = 103, email_address = "jim@gmail.com"),
        dict(id = 1, user_id = 104, email_address = "sofar@gmail.com"),
        dict(id = 5, user_id = 105, email_address = "alfons@gmail.com"),
    ])


def SelectEasyData():
    conn = engine.connect()

    sel1 = users.select(whereclause = "id < 5 order by name")
    rows = conn.execute(sel1).fetchall()
    print(rows)

    from sqlalchemy.sql import select
    sel2 = select([users], whereclause = "id > 5")
    rows = conn.execute(sel2).fetchall()
    print(rows)


def SelectDifficulteData():
    print("\n")
    from sqlalchemy.sql import select, and_

    conn = engine.connect()

    # SELECT users.id, users.name, users.fullname, addresses.id, addresses.user_id, addresses.email_address FROM users, addresses WHERE users.id = addresses.user_id AND users.id = ? ORDER BY users.name
    # sel = select([users, addresses]).where(and_(users.c.id == addresses.c.user_id, users.c.id == 102)).order_by(users.c.name)
    # sel = select([users, addresses]).where((users.c.id == addresses.c.user_id) & (users.c.id == 102)).order_by(users.c.name)
    sel = select([users, addresses]).where(users.c.id == addresses.c.user_id).order_by(addresses.c.id, users.c.name)
    resultProxy = conn.execute(sel)
    for result in resultProxy:
        print(result)


def UseTextSql():
    print("\n")
    from sqlalchemy.sql import text
    from sqlalchemy.sql import bindparam

    sel = text("select * from users where users.id < :a").bindparams(bindparam('a', value=1000, type_= Integer))
    res = engine.execute(sel).fetchall()
    # res = engine.execute(sel, a = 1000).fetchall()
    for c in res:
        print(c.id, c.name)


def UsePureTextSql():
    print("\n")

    sel = "select * from users where users.id < 1000"
    res = engine.execute(sel).fetchall()
    for c in res:
        print(c.id, c.name)     # 效果一样


if __name__ == '__main__':
    GetTables()
    DropTables()
    CreateTables()
    InsertData()
    InsertAllData()
    SelectEasyData()
    SelectDifficulteData()
    UseTextSql()
    UsePureTextSql()
