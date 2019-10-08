"""
@file: SqlAlchemyOrmDemo.py
@time: 2018/12/18
@author: sch
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 创建引擎
engine = create_engine("sqlite:///./memory.db", echo = True)

# 声明基类，并绑定引擎
Base = declarative_base(engine)


class User(Base):
    __tablename__ = "users_orm"

    id = Column(Integer, autoincrement = True, default = 0, primary_key = True, comment = "用户ID")
    name = Column(String, comment = "用户名")
    fullname = Column(String, comment = "用户全名")
    password = Column(String, comment = "用户密码")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


print(repr(User.__table__))
Base.metadata.create_all()

Session = sessionmaker(bind=engine)
session = Session()
res = session.query(User).filter(User.name.in_(['hell', 'hh'])).one()
pass