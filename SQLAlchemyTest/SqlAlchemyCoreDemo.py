"""
@file: SQLAlchemyDemo.py
@time: 2018/09/27
@author: sch
"""
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()
users = Table("users", metadata,
              Column("id", Integer, primary_key = True),
              Column("name", String),
              Column("fullname", String),
              )

addresses = Table("addresses", metadata,
                  Column("id", Integer, primary_key = True),
                  Column("user_id", None, ForeignKey("users.id")),
                  Column("email_address", String, nullable = False)
                  )

engine = create_engine("sqlite:///:memory:", echo=True)

metadata.create_all(engine)