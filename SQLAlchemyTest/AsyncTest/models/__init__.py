#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: __init__.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/7/7 下午3:44
# History:
#=============================================================================
"""
__doc__ = """
移植原始项目中的表，项目中其他地方导入表结构时，使用此处的表结构

表中类方法，建议以下面的形式进行创建：

    class Example:

        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

        @classmethod
        def get_by_id(cls, session: Session, id_):
            try:
                instance = session.query(cls).filter_by(id=id_).one()
            except NoResultFound:
                raise Exception(f"{cls.__tablename__}中未找到对应的记录")
            return instance

调用时通过具体表的方法进行调用：

    with open_session() as session:
        obj = Example.get_by_id(session=session, id_=10)

"""