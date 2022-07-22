import asyncio
import databases
from contextlib import asynccontextmanager, contextmanager
from copy import deepcopy
from datetime import datetime
from typing import Any, ContextManager, Dict, Optional, Tuple, Union

from sqlalchemy import JSON, Column, DateTime, Enum, Integer, create_engine, desc, func
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import QueuePool, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from loguru import logger

mysql = {
    'host': "10.10.100.65",
    'port': 3306,
    'username': "root",
    'password': "letsg0",
    'database_name': "qdata_cloud"
}

# qdata_asyncmy_url = 'mysql+asyncmy://{username}:{password}@{host}:{port}/{database_name}'.format(**mysql)
# qdata_asyncmy_engine = create_async_engine(qdata_asyncmy_url, connect_args={"use_unicode": True, "charset": "UTF8MB4"})
# qdata_asyncmy_databases = databases.Database(qdata_asyncmy_url)

qdata_async_url = 'mysql+aiomysql://{username}:{password}@{host}:{port}/{database_name}'.format(**mysql)
qdata_async_engine = create_async_engine(
    qdata_async_url,
    echo=True,
    # echo_pool=True,
    # poolclass=AsyncAdaptedQueuePool,
    # pool_pre_ping=True,
    # pool_size=250,
    # max_overflow=300,
    # pool_recycle=3600,
    connect_args={"use_unicode": True, "charset": "UTF8MB4"},
)
QDataAsyncSession = sessionmaker(bind=qdata_async_engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False)

qdata_sync_url = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}'.format(**mysql)
qdata_sync_engine = create_engine(
    qdata_sync_url,
    echo=True,
    # echo_pool=True,
    # poolclass=QueuePool,
    # pool_pre_ping=True,
    # pool_size=250,
    # max_overflow=300,
    # pool_recycle=3600,
    connect_args={"use_unicode": True, "charset": "UTF8MB4"},
)
QDataSyncSession = sessionmaker(bind=qdata_sync_engine, class_=Session, autocommit=False, autoflush=False, expire_on_commit=False)


# ======================== 项目中表结构继承的基类 =======================
class CloudSqlAlchemyEnum(str, Enum):  # type: ignore
    def __contains__(self, item: Any) -> bool:
        return item in self.enums


# ======================== 项目中表结构继承的基类 =======================
# @as_declarative(bind=qdata_async_engine)
@as_declarative(bind=qdata_sync_engine)
class CloudEntity:
    """
    自带两个时间戳字段的base model
    Ref: https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/table_config.html?highlight=__table_args__
    """
    __table_args__: Union[Dict[str, Any], Tuple[Any]] = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",  # utf8 vs utf8mb4,使用utf8mb4
    }

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    attr = Column(JSON, default=dict(), doc="属性，保存一些额外的在设计时未考虑到的参数")
    create_time = Column(DateTime, default=datetime.utcnow, doc="创建时间utc")
    update_time = Column(DateTime, default=None, onupdate=datetime.utcnow, doc="修改时间utc")

    __repr_columns__ = ["id"]  # 调试时展示的参数

    def __repr__(self) -> str:
        repr_attr_list = getattr(self, "__repr_columns__", list())
        repr_attr_str = ', '.join(f"{attr}={getattr(self, attr)}" for attr in repr_attr_list)
        return f"<{self.__tablename__}({repr_attr_str})>"  # type: ignore

    def get_attr(self, key: str, default: Any = None) -> Any:
        """
        获取attr中的属性
        :param key: 属性的索引
        :param default: 未获取到的默认值
        :return:
        """
        return self.attr.get(key, default)

    def set_attr(self, key: str, value: Any) -> None:
        """
        设置attr中的属性
        :param key: 自定义的key值
        :param value: 待存储的value
        :return:
        """
        attr = deepcopy(self.attr)
        attr.update({key: value})
        self.attr = attr

    @classmethod
    def get_by_id(cls, session: Session, id_: int) -> Any:
        try:
            instance = session.query(cls).filter_by(id=id_).one()
        except NoResultFound:
            raise Exception(f"{cls.__tablename__}中未找到对应的记录")  # type: ignore
        return instance

    @classmethod
    def get_first(cls, session: Session, key: str, value: Any) -> Any:
        obj = session.query(cls).filter(getattr(cls, key) == value).first()
        return obj

    @classmethod
    def get_last(cls, session: Session, key: str, value: Any) -> Any:
        obj = session.query(cls).filter(getattr(cls, key) == value).order_by(desc(cls.id)).first()
        return obj

    @classmethod
    def get_one(cls, session: Session, key: str, value: Any) -> Any:
        obj = session.query(cls).filter(getattr(cls, key) == value).one()
        return obj

    @classmethod
    async def get_all(cls, session: Session, key: Optional[str] = None, value: Any = None) -> Any:
        if key:
            objs = session.query(cls).filter(getattr(cls, key) == value).all()
        else:
            objs = session.query(cls).all()
        return objs

    @classmethod
    def get_count(cls, session: Session, key: Optional[str] = None, value: Any = None) -> int:
        if key:
            counts = session.query(cls).filter(getattr(cls, key) == value).count()
        else:
            # session.query(cls).count()
            # SQLAlchemy先是取出符合条件的所有行集合，然后再通过SELECT count(*)来统计有多少行。
            # 表达式func.count()直接使用count函数。-----这个就是相当于数据库中的直接count()。大数据量下更加快速
            counts = session.query(func.count(cls.id)).scalar()
        return counts


# ===================== 开启一个会话 =========================
@asynccontextmanager  # type: ignore
async def open_async_session(qf: bool = False) -> ContextManager[AsyncSession]:  # type: ignore
    """
    可以使用with 上下文，在with结束之后自动commit
    """
    async_session = QDataAsyncSession()
    try:
        yield async_session
        await async_session.commit()
    except Exception as e:
        await async_session.rollback()
        logger.exception(e)
        raise e
    finally:
        await async_session.close()


@contextmanager  # type: ignore
def open_session(qf: bool = False) -> ContextManager[Session]:  # type: ignore
    """
    可以使用with 上下文，在with结束之后自动commit
    """
    session = QDataSyncSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(e)
        raise e
    finally:
        session.close()


# ===================== 对表相关操作 ==============================
def clean_all_table() -> None:
    """ 清除所有的表 """
    metadata = CloudEntity.metadata  # type: ignore
    metadata.drop_all()
    metadata.create_all()


def drop_all_table() -> None:
    """ 删除所有的表 """
    metadata = CloudEntity.metadata  # type: ignore
    metadata.drop_all()


# create table
def create_database() -> None:
    """ 创建所有的表，如果已经存在，则不创建 """
    _engine = create_engine('mysql+pymysql://{username}:{password}@{host}:{port}'.format(**mysql),
                            echo=True,
                            echo_pool=True,
                            poolclass=QueuePool,
                            pool_pre_ping=True,
                            pool_size=5,
                            max_overflow=10,
                            pool_recycle=3600,
                            connect_args={"use_unicode": True, "charset": "UTF8MB4"})
    _engine.execute("create database if not exists qdata_cloud DEFAULT CHARACTER SET UTF8MB4")  # create db


# create table
async def create_all_table() -> None:
    """ 创建所有的表，如果已经存在，则不创建 """
    metadata = CloudEntity.metadata  # type: ignore
    async with qdata_async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all, checkfirst=True)
