#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: cx_oracle_pool_byu_sessionpool_self.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/2/24 4:00 PM
# History:
#=============================================================================
"""
import abc
import os
import datetime
import concurrent.futures
import asyncio
from typing import (
    Any,
    Union,
    Dict,
    Tuple,
    AsyncContextManager,
    Iterator,
    Optional,
    List,
)
import loguru
from enum import Enum
import cx_Oracle
from contextlib import asynccontextmanager

logger = loguru.logger
thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=(os.cpu_count() or 10) * 10)


async def run_as_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(thread_executor, lambda: func(*args, **kwargs))


class Excep(Exception):
    def __init__(self, *args, **kwargs):
        pass


DatabaseError = SQLTimeoutError = ORAError = ProcedureCallError = DatabaseNotConnected = Excep


class oracle_config:
    call_timeout = 60


TIMEOUT_ORACLE_DB_CONN = 3


# ====================== 数据结构 ======================
class OracleAuthEnum(str, Enum):
    """Oracle连接权限枚举"""

    DEFAULT_AUTH = cx_Oracle.DEFAULT_AUTH
    SYSDBA = cx_Oracle.SYSDBA
    SYSOPER = cx_Oracle.SYSOPER
    SYSASM = cx_Oracle.SYSASM
    SYSBKP = cx_Oracle.SYSBKP
    SYSDGD = cx_Oracle.SYSDGD
    SYSKMT = cx_Oracle.SYSKMT
    SYSRAC = cx_Oracle.SYSRAC


# ====================== Oracle连接池 ======================
class OraclePoolMetaclass(type):
    __doc__ = """
    用于存放Oracle连接池子的池子的类
    使用元类实现，每次新建 OraclePool 对象时，将 OraclePool 添加到 _ocean 中
    """

    _ocean: Dict[str, "OraclePool"] = dict()  # 存放 OraclePool 的池子

    def __call__(  # type: ignore
            cls,
            username: str,
            password: str,
            dsn: str,
            min_session: int = 1,
            max_session: int = 10,
            session_increment: int = 1,
            encoding: str = "UTF-8",
            timeout: int = 3600,
            max_lifetime_session: int = 86400,
            ping_interval: int = 3,
            **kwargs: Any,
    ) -> "OraclePool":

        # 此处必须指定cls，否则会导致不同cls映射到相同的单例中
        key = '#'.join(str(k) for k in [
            username,
            password,
            dsn,
        ])
        if key not in cls._ocean:
            cls._ocean[key] = super(OraclePoolMetaclass, cls).__call__(
                username=username,
                password=password,
                dsn=dsn,
                min_session=min_session,
                max_session=max_session,
                session_increment=session_increment,
                encoding=encoding,
                timeout=timeout,
                max_lifetime_session=max_lifetime_session,
                ping_interval=ping_interval,
                **kwargs,
            )
            logger.debug(f"Oracle connect '{key}' create new cache pool -> {cls._ocean[key]}!")
        else:
            logger.debug(f"Oracle connect '{key}' use cache pool -> {cls._ocean[key]}!")

        return cls._ocean[key]


class OraclePool(metaclass=OraclePoolMetaclass):
    def __init__(
            self,
            username: str,
            password: str,
            dsn: str,
            min_session: int = 2,
            max_session: int = 5,
            session_increment: int = 1,
            encoding: str = "UTF-8",
            timeout: int = 3600,
            max_lifetime_session: int = 86400,
            ping_interval: int = 3,
    ) -> None:
        """
        根据输入内容，返回 oracle 连接池

        :param username: 登陆用户名
        :param password: 登陆密码
        :param dsn: 登陆的dsn，data source name
        :param min_session: 最小会话数
        :param max_session: 最大会话数
        :param session_increment: 会话每次增加的个数
        :param encoding: 编码格式
        :param timeout: 池中的空间会话终止时间，超过该时间的空闲会话将会终止。0 表示不终止空闲会话。单位秒
        :param max_lifetime_session: 会话最大的存活时间，超过该时间的会话将会被关闭，正在使用的会话不会因为超时被关闭。0 表示不终止会话。单位秒
        :param ping_interval: 会话从 pool 中 acquired 时，先进行ping操作，超过该时间，会返回异常
        """
        self._pool = cx_Oracle.SessionPool(
            user=username,
            password=password,
            dsn=dsn,
            min=min_session,
            max=max_session,
            increment=session_increment,
            threaded=True,
            getmode=cx_Oracle.SPOOL_ATTRVAL_FORCEGET,  # 如果池中没有可用的空闲会话，将返回一个新连接
            encoding=encoding,
            timeout=timeout,
            maxLifetimeSession=max_lifetime_session,
            # ping_interval=ping_interval,
        )

    def __repr__(self) -> str:
        return f"{id(self)}-{self._pool.dsn}"

    def __del__(self) -> None:
        if hasattr(self, "_pool"):
            self._pool.close()

    @property
    def count(self) -> int:
        return self._pool.opened

    async def acquire(self, purity: int = cx_Oracle.ATTR_PURITY_DEFAULT) -> Tuple[cx_Oracle.Connection, cx_Oracle.Cursor]:
        """
        从池子中获取一个连接

        :param purity: 连接的获取方式
                 cx_Oracle.ATTR_PURITY_DEFAULT - 默认方式，需要查找Oracle文档找到更多的信息
                 cx_Oracle.ATTR_PURITY_NEW - 获取一个新的连接，不保留之前的会话状态
                 cx_Oracle.ATTR_PURITY_SELF - 获取一个新的连接，保留之前的会话状态
        :return:
        """
        connection = await run_as_async(self._pool.acquire, purity=purity)
        cursor = await run_as_async(connection.cursor)
        return connection, cursor

    async def release(self, connection: cx_Oracle.Connection, cursor: cx_Oracle.Cursor) -> None:
        """
        释放连接到池子中

        :param connection: 待释放的连接
        :param cursor: 待释放的游标
        :return:
        """
        await run_as_async(cursor.close)  # 关闭游标
        await run_as_async(self._pool.release, connection=connection)  # 关闭连接


async def _open_oracle_connection(
        username: str,
        password: str,
        dsn: str,
        mode: OracleAuthEnum,
        encoding: str,
        connect_timeout: int = TIMEOUT_ORACLE_DB_CONN,
) -> "CloudOracleOperator":
    """
    使用 cx_Oracle.Connection 创建 Oracle 连接对象

    :param username: 登陆用户名
    :param password: 登陆密码
    :param dsn: 登陆的dsn，data source name
    :param mode: 连接模式
    :param encoding: 编码
    :param connect_timeout: 数据库连接超时时间，单位秒
    :return:
    """
    logger.info(f"连接 Oracle 使用直连 -> cx_Oracle.Connection(username={username},password={password},dsn={dsn},mode={mode},encoding={encoding})！")

    try:
        # 初始化 cx_Oracle.Connection 对象
        connection: cx_Oracle.Connection = await asyncio.wait_for(
            fut=run_as_async(
                cx_Oracle.connect,
                user=username,
                password=password,
                dsn=dsn,
                mode=mode.value,
                encoding=encoding,
                threaded=True,
            ),
            timeout=connect_timeout,
        )

        # 获取oracle连接及游标
        cursor: cx_Oracle.Cursor = connection.cursor()
        return CloudOracleOperator(
            connection=connection,
            cursor=cursor,
            username=username,
            password=password,
            dsn=dsn,
            mode=mode,
            encoding=encoding,
            connect_timeout=connect_timeout,
        )

        # oracle操作结束后，回收oracle connection 资源
        # # await run_as_async(cursor.close)
        # # await run_as_async(connection.close)

        # logger.info(f"回收 Oracle 连接 -> cx_Oracle.Connection(username={username},password={password},dsn={dsn},mode={mode},encoding={encoding})！")

    except asyncio.TimeoutError:
        logger.error(f"使用 cx_Oracle.Connection(username={username},password={password},dsn={dsn},mode={mode},encoding={encoding}) 创建Oracle连接超时(timeout={connect_timeout})！")
        raise ORAError(error='ORA-12170: Oracle连接超时')

    except Exception as e:
        logger.error(f"使用 cx_Oracle.Connection(username={username},password={password},dsn={dsn},mode={mode},encoding={encoding}) 创建Oracle连接发生异常！")
        raise e


async def _open_oracle_connection_use_pool(
        username: str,
        password: str,
        dsn: str,
        encoding: str,
        connect_timeout: int = TIMEOUT_ORACLE_DB_CONN,
) -> "CloudOracleOperator":
    """
    使用 cx_Oracle.SessionPool 创建 Oracle 连接对象

    :param username: 登陆用户名
    :param password: 登陆密码
    :param dsn: 登陆的dsn，data source name
    :param encoding: 编码
    :param connect_timeout: 数据库连接超时时间，单位秒
    :return:
    """
    logger.info(f"连接 Oracle 使用池子 -> cx_Oracle.SessionPool(username={username},password={password},dsn={dsn})！")

    try:
        # 初始化 Oracle 连接池 对象
        oracle_pool = await asyncio.wait_for(
            fut=run_as_async(
                OraclePool,
                username=username,
                password=password,
                dsn=dsn,
                encoding=encoding,
            ),
            timeout=connect_timeout,
        )  # type: OraclePool

        # 获取oracle连接及游标
        connection, cursor = await asyncio.wait_for(
            fut=oracle_pool.acquire(),
            timeout=connect_timeout,
        )

        return CloudOracleOperator(
            connection=connection,
            cursor=cursor,
            pool=oracle_pool,
            username=username,
            password=password,
            dsn=dsn,
            mode=OracleAuthEnum.DEFAULT_AUTH,
            encoding=encoding,
            connect_timeout=connect_timeout,
        )

        # oracle操作结束后，回收oracle connection 资源
        # await oracle_pool.release(connection=connection, cursor=cursor)

        # logger.info(f"回收 Oracle 连接 -> cx_Oracle.SessionPool(username={username},password={password},dsn={dsn})！")

    except asyncio.TimeoutError:
        logger.error(f"使用 cx_Oracle.SessionPool(username={username},password={password},dsn={dsn}) 创建Oracle连接超时(timeout={connect_timeout})！")
        raise ORAError(error='ORA-12170: Oracle连接超时')

    except Exception as e:
        logger.error(f"使用 cx_Oracle.SessionPool(username={username},password={password},dsn={dsn}) 创建Oracle连接发生异常！")
        raise e


# ====================== Oracle 操作对象 ======================
class CloudOracleOperator:

    def __init__(
            self,
            connection: cx_Oracle.Connection,
            cursor: cx_Oracle.Cursor,
            username: str,
            password: str,
            dsn: str,
            mode: OracleAuthEnum,
            encoding: str,
            pool: Optional[OraclePool] = None,
            connect_timeout: int = TIMEOUT_ORACLE_DB_CONN,
    ) -> None:
        """
        Cloud Oracle 操作 对象

        :param connection: 连接器
        :param cursor: 游标
        """
        # 创建连接
        self._connection: cx_Oracle.Connection = connection
        self._cursor: cx_Oracle.Cursor = cursor

        self._pool: Optional[OraclePool] = pool

        # 其他配置，判断连接是否存活时使用
        self._username = username
        self._password = password
        self._dsn = dsn
        self._mode = mode
        self._encoding = encoding
        self._connect_timeout = connect_timeout

    async def close(self) -> None:
        if self._pool is not None:
            await self._pool.release(connection=self._connection, cursor=self._cursor)
            logger.info(f"连接池({self._pool})回收连接成功，当前连接数 {self._pool.count}！")
        else:
            await run_as_async(self._cursor.close)  # 关闭游标
            await run_as_async(self._connection.close)  # 关闭连接

    # ----------------- 内部调用方法 -----------------
    @staticmethod
    def _dict_curs(
            cursor: cx_Oracle.Cursor,
            data_rows: Optional[List[Tuple[Any]]] = None,
            title_lower: bool = False,
            float_round: int = 0,
            datetime_format: Optional[str] = None
            # todo: 添加model
    ) -> List[Dict[str, Any]]:
        """
        返回[{},{}]数据格式
        :param cursor: 游标对象
        :param data_rows: 输入的数据行，通过输入数据进行解析
        :param title_lower: 是否将列名转化为小写
        :param float_round: 浮点型数据保留的小数位，四舍五入方式
        :param datetime_format: 日期格式化字符串
        :return:
        """

        def _lower(x: str) -> str:
            return x.lower() if title_lower else x

        if cursor.description is None:
            return list()

        title_list = [_lower(d[0]) for d in cursor.description]  # 获取字段名

        # 根据输入数据或者游标对象中的数据进行数据行的获取
        if isinstance(data_rows, tuple):
            data_rows = [data_rows]
        elif isinstance(data_rows, list):
            data_rows = data_rows
        else:
            data_rows = [row for row in cursor]

        # 进行数据转换
        result = list()
        for row in data_rows:
            values = list()

            # 行数据转换
            for column in row:
                if float_round > 0 and isinstance(column, float):
                    column = round(column, float_round)
                elif datetime_format and isinstance(column, datetime.datetime):
                    column = column.strftime(datetime_format)

                values.append(column)

            result.append(dict(zip(title_list, values)))

        return result

    # ----------------- 连接对象的成员信息 -----------------
    @property
    def connection(self) -> cx_Oracle.Connection:
        """Oracle连接对象"""
        return self._connection

    @property
    def cursor(self) -> cx_Oracle.Cursor:
        """游标"""
        return self._cursor

    @property
    def version(self) -> str:
        """Oracle 版本"""
        return self._connection.version

    @property
    def description(self) -> str:
        """"""
        return self._cursor.description

    @property
    def dsn(self) -> str:
        return self.connection.dsn

    # ----------------- 外部调用接口 -----------------
    def __iter__(self) -> Iterator[cx_Oracle.Cursor]:
        return iter(self._cursor)

    async def is_alive(self, raise_exception: bool = False) -> bool:
        """
        Oracle 连接是否存活，新建连接，测试Oracle连通性

        :return:
        """
        try:
            # 2022-04-15
            # # 新建连接，测试Oracle连通性
            # async with asyncio.Lock():
            #     new_operator = await _open_oracle_connection(
            #         username=self._username,
            #         password=self._password,
            #         dsn=self._dsn,
            #         mode=self._mode,
            #         encoding=self._encoding,
            #         connect_timeout=self._connect_timeout,
            #     )
            #     await new_operator.close()
            #
            # return True

            if self._pool:
                _connection, _cursor = await self._pool.acquire(purity=cx_Oracle.ATTR_PURITY_NEW)
                await run_as_async(_cursor.close)  # 关闭游标
                await run_as_async(_connection.close)  # 关闭连接

            return True
        except Exception as e:
            logger.error(f"判断连接是否存活发生错误！\n{e}")
            if raise_exception:
                if isinstance(e, DatabaseError):
                    raise ORAError(error=str(e))
                raise e

            return False

    def _execute(self, sql: str, timeout: int = oracle_config.call_timeout, *args: Any, **kwargs: Any) -> "CloudOracleOperator":
        """
        执行sql命令
        :param sql: oracle sql
        :param timeout: 执行oracle sql的超时时间，timeout为0时，不超时。默认60s
        """
        try:
            self._connection.callTimeout = timeout * 1000
            self._cursor.execute(sql, *args, **kwargs)
            return self
        except DatabaseError as e:
            # 执行超时异常 -> DPI-1067: call timeout of 3000 ms exceeded with ORA-3156
            if all(k in str(e) for k in ["DPI-1067", "call timeout", "ORA-3156"]):
                raise SQLTimeoutError()
            else:
                raise ORAError(error=str(e))
        finally:
            self._connection.callTimeout = 0

    async def async_execute(self, sql: str, timeout: int = oracle_config.call_timeout, *args: Any, **kwargs: Any) -> "CloudOracleOperator":
        """
        执行sql命令，异步方式
        :param sql: oracle sql
        :param timeout: 执行oracle sql的超时时间
        """
        try:
            logger.info(f"[{self._connection.dsn} {args} {kwargs} timeout={timeout}'s]:\n{sql}")
            return await run_as_async(self._execute, sql, timeout, *args, **kwargs)

        except DatabaseError as e:
            logger.exception(f"[{self._connection.dsn} {args} {kwargs} timeout={timeout}'s] 执行sql出现异常!{sql}")
            raise ORAError(error=str(e))

    async def fetchone(self, to_dict: bool = True, title_lower: bool = False, **kwargs: Any) -> Union[List[Dict[str, Any]], Tuple[Any]]:
        """
        拿出第一行的数据

        ①当 to_dict = True，返回 [{'DATABASE_ROLE': 'PRIMARY'}]
        ②当 to_dict = False，返回 ('PRIMARY', )

        :param to_dict: 以字典类型进行展示
        :param title_lower: 是否输出小写标题
        """
        data = await run_as_async(self._cursor.fetchone)
        return self._dict_curs(cursor=self._cursor, data_rows=data, title_lower=title_lower, **kwargs) if to_dict else data

    async def fetchall(self, to_dict: bool = True, title_lower: bool = False, **kwargs: Any) -> Union[List[Dict[str, Any]], List[Tuple[Any]]]:
        """
        拿出所有数据

        ①当 to_dict = True，返回 [{'DATABASE_ROLE': 'PRIMARY'}]
        ②当 to_dict = False，返回 [('PRIMARY', )]

        :param to_dict: 以字典类型进行展示
        :param title_lower: 是否输出小写标题
        """
        data = await run_as_async(self._cursor.fetchall)
        return self._dict_curs(cursor=self._cursor, data_rows=data, title_lower=title_lower, **kwargs) if to_dict else data

    async def commit(self) -> Any:
        return await run_as_async(self._connection.commit)

    async def callproc(self, procedure_name: str, *args: Any, **kwargs: Any) -> Any:
        """
        执行程序
        具体请参考：https://cx-oracle.readthedocs.io/en/latest/user_guide/plsql_execution.html#plsqlproc
        :param procedure_name: 执行的程序名
        """
        # todo logger.debug("[{sid} {args}, {kwargs}] {procedure_name}".format(
        #     procedure_name=procedure_name, sid=self.sid, args=args, kwargs=kwargs)
        # )
        try:
            return await run_as_async(self._cursor.callproc, procedure_name, *args, **kwargs)
        except DatabaseError as e:
            logger.exception(e)
            raise ProcedureCallError(proc_name=procedure_name)

    async def prepare(self, *args: Any, **kwargs: Any) -> Any:
        return await run_as_async(self._cursor.prepare, *args, **kwargs)

    async def change_session(self, container_name: str) -> None:
        """
        切换到容器数据库
        :param container_name: 容器名
        """
        if not self._connection:
            raise DatabaseNotConnected()
        logger.info(f"change db session to {container_name}")
        await self.async_execute("alter session set container={}".format(container_name))


# ====================== Oracle 管理对象 ======================
class CloudOracleManagerBase:

    def __init__(
            self,
            username: str,
            password: str,
            mode: OracleAuthEnum,
            with_pool: bool,
            encoding: str,
    ) -> None:
        """
        Oracle 连接管理员基类

        :param username: 连接oracle的用户名
        :param password: 连接oracle的密码
        :param mode: 连接的角色权限
        :param with_pool: 是否使用连接池的方式建立连接，具体参考open_oracle_connection方法介绍
        :param encoding: 编码
        """
        self._username = username
        self._password = self.decode_password(password=password)
        self._mode = mode

        self._with_pool = with_pool
        self._encoding = encoding

        self._operator: CloudOracleOperator

    @property
    @abc.abstractmethod
    def dsn(self) -> str:
        """data source name"""
        raise NotImplementedError

    @staticmethod
    def decode_password(password: str) -> str:
        """
        解密密码，部分密码在数据库中经过了加密处理

        :param password: 待解密的秘钥
        :return:
        """
        try:
            return password
        except Exception:
            logger.debug(f"解密秘钥({password})发生错误！直接使用password({password})!")
            return password

    async def __aenter__(self) -> "CloudOracleOperator":
        """
         PS：
             使用连接池进行连接时，建议只使用默认权限模式进行连接创建。
             需要特备权限时，才选择单一连接的方式
             参考：https://github.com/oracle/python-cx_Oracle/issues/511

         与oracle建立连接，使用方式如下：

         ① 使用连接池进行连接创建

             async with CloudOracleUseDsn(
                 username=xxxx,
                 password=xxxx,
                 dsn=xxxxxxxxx,
                 with_pool=True,
             ) as oracle_operator:
                 # do your work

             注：如果username为sys、或mode不为DEFAULT_AUTH，将使用单一连接的方式进行创建

         ② 使用单一连接进行连接创建，一般在 mode不为DEFAULT_AUTH 时使用

             async with CloudOracleUseDsn(
                     username=xxxx,
                     password=xxxx,
                     dsn=xxxxxxxxx,
                     with_pool=False,
                     mode=OracleAuthEnum.SYSDBA
                 ) as oracle_operator:
                     # do your work

         :return:
         """
        try:
            # 调整连接模式
            mode = OracleAuthEnum.SYSDBA if self._username.lower() == "sys" else self._mode

            # 调整连接方式
            with_pool = False if mode != OracleAuthEnum.DEFAULT_AUTH else self._with_pool

            if not with_pool:
                self._operator = await _open_oracle_connection(
                    username=self._username,
                    password=self._password,
                    dsn=self.dsn,
                    mode=mode,
                    encoding=self._encoding,
                )
            else:
                self._operator = await _open_oracle_connection_use_pool(
                    username=self._username,
                    password=self._password,
                    dsn=self.dsn,
                    encoding=self._encoding,
                )

            return self._operator

        except DatabaseError as e:
            logger.exception(f"数据库连接建立发生异常！\n{e}")
            raise ORAError(error=str(e))

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        await self._operator.close()


class CloudOracleUseSid(CloudOracleManagerBase):

    def __init__(
            self,
            *,
            username: str,
            password: str,
            host: str,
            sid: str,
            port: int = 1521,
            mode: OracleAuthEnum = OracleAuthEnum.DEFAULT_AUTH,
            with_pool: bool = True,
            encoding: str = "UTF-8",
    ) -> None:
        """
        使用 Sid 的方式进行 Oracle 连接

        :param username: 连接oracle的用户名
        :param password: 连接oracle的密码
        :param host: 连接oracle的地址
        :param sid: 连接oracle的sid，通过 ps -ef | grep pmon 获取
        :param port: scan 端口
        :param mode: 连接的角色权限
        :param with_pool: 是否使用连接池的方式建立连接，具体参考open_oracle_connection方法介绍
        :param encoding: 编码
        """
        super(CloudOracleUseSid, self).__init__(
            username=username,
            password=password,
            mode=mode,
            with_pool=with_pool,
            encoding=encoding,
        )

        self._host = host
        self._port = port
        self._sid = sid

    def __repr__(self) -> str:
        return f"{self._username}@{self._host}:{self._port}/{self._sid}"

    @property
    def dsn(self) -> str:
        return cx_Oracle.makedsn(self._host, self._port, sid=self._sid)


class CloudOracleUsePdb(CloudOracleUseSid):
    def __init__(
            self,
            *,
            username: str,
            password: str,
            host: str,
            sid: str,
            pdb_name: str,
            port: int = 1521,
            mode: OracleAuthEnum = OracleAuthEnum.DEFAULT_AUTH,
            with_pool: bool = True,
            encoding: str = "UTF-8",
    ) -> None:
        """
        连接pdb数据库
        :param pdb_name: pdb的名称
        """
        super(CloudOracleUsePdb, self).__init__(
            username=username,
            password=password,
            host=host,
            sid=sid,
            port=port,
            mode=mode,
            with_pool=with_pool,
            encoding=encoding,
        )
        self._pdb_name = pdb_name

    async def __aenter__(self) -> CloudOracleOperator:
        oracle_operator = await super(CloudOracleUsePdb, self).__aenter__()  # type: CloudOracleOperator
        await oracle_operator.change_session(container_name=self._pdb_name)
        return oracle_operator

    @property
    def pdb_name(self) -> str:
        return self._pdb_name


class CloudOracleUseDBName(CloudOracleManagerBase):
    def __init__(
            self,
            *,
            username: str,
            password: str,
            scan_ip: str,
            db_name: str,
            port: int = 1521,
            mode: OracleAuthEnum = OracleAuthEnum.DEFAULT_AUTH,
            with_pool: bool = True,
            encoding: str = "UTF-8",
    ) -> None:
        """
        使用 DBName 的方式进行 Oracle 连接

        :param username: 连接oracle的用户名
        :param password: 连接oracle的密码
        :param scan_ip: scan ip
        :param db_name: 连接的db名称
        :param port: scan 端口
        :param mode: 连接的角色权限
        :param with_pool: 是否使用连接池的方式建立连接，具体参考open_oracle_connection方法介绍
        :param encoding: 编码
        """
        super(CloudOracleUseDBName, self).__init__(
            username=username,
            password=password,
            mode=mode,
            with_pool=with_pool,
            encoding=encoding,
        )

        self._scan_ip = scan_ip
        self._port = port
        self._db_name = db_name

    def __repr__(self) -> str:
        return f"{self._username}/{self._password}@{self._scan_ip}:{self._port}/{self._db_name}"

    @property
    def dsn(self) -> str:
        return cx_Oracle.makedsn(self._scan_ip, self._port, service_name=self._db_name)


class CloudOracleUseDsn(CloudOracleManagerBase):
    """使用外部传入的dsn进行连接
    """

    def __init__(
            self,
            *,
            username: str,
            password: str,
            dsn: str,
            mode: OracleAuthEnum = OracleAuthEnum.DEFAULT_AUTH,
            with_pool: bool = True,
            encoding: str = "UTF-8",
    ) -> None:
        """
        使用 Dsn 的方式进行 Oracle 连接

        :param username: 连接oracle的用户名
        :param password: 连接oracle的密码
        :param dsn: 连接oracle的dsn连接串
        :param mode: 连接的角色权限
        :param with_pool: 是否使用连接池的方式建立连接，具体参考open_oracle_connection方法介绍
        :param encoding: 编码
        """
        super(CloudOracleUseDsn, self).__init__(
            username=username,
            password=password,
            mode=mode,
            with_pool=with_pool,
            encoding=encoding,
        )

        self._dsn = dsn

    def __repr__(self) -> str:
        return self._dsn

    @property
    def dsn(self) -> str:
        return self._dsn


# ====================== 测试代码 ======================
from itertools import chain


async def test_sql(with_pool: bool):
    async with CloudOracleUseDBName(
            username='test',
            password='test',
            db_name='rac',
            scan_ip="10.10.90.27",
            with_pool=with_pool,
    ) as oracle_operator:
        # sql = """
        #     SELECT
        #     dg.group_number as group_id,
        #      dg.name as group_name,
        #      d.disk_number as disk_id,
        #      d.name as disk_name,
        #      d.failgroup as fail_group,
        #      d.mode_status as mode_status,
        #      d.path as com_path,
        #      d.total_mb as total_mb,
        #      min(d.free_mb) as free_mb
        #     FROM
        #      gv$asm_disk d,
        #      gv$asm_diskgroup dg
        #     WHERE
        #      d.group_number = dg.group_number
        #      AND d.inst_id = dg.inst_id
        #     GROUP BY
        #      dg.group_number,
        #      dg.name,
        #      d.disk_number,
        #      d.name,
        #      d.failgroup,
        #      d.mode_status,
        #      d.path,
        #      d.total_mb
        #     ORDER BY
        #      d.name"""

        sql = "select database_role from v$database"

        # print(f"is_aliave = {await oracle_operator.is_alive()}")
        # await oracle_operator.async_execute(sql=sql)
        # print(await oracle_operator.fetchall(to_dict=True))
        # await oracle_operator.async_execute(sql=sql)
        # print(await oracle_operator.fetchall(to_dict=False))

        await oracle_operator.async_execute(sql=sql)
        fetchone_res_1 = await oracle_operator.fetchone(to_dict=True)
        print(fetchone_res_1)
        await oracle_operator.async_execute(sql=sql)
        fetchone_res_2 = await oracle_operator.fetchone(to_dict=False)
        print(fetchone_res_2)

        res_3 = chain(fetchone_res_2, fetchone_res_2)
        print(list(res_3))

    # print(f"is_aliave = {await oracle_operator.is_alive()}")


async def test_connect(
        index,
        username,
        password,
        dsn,
):
    "test#test#(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.10.99.20)(PORT=1521))(CONNECT_DATA=(SID=test2)))"
    async with CloudOracleUseDsn(
            username=username,
            password=password,
            dsn=dsn,
    ) as oracle_client:
        result = await oracle_client.is_alive()
        print(f"{index} - {dsn} is alive -> {result}")


async def performance_test(i):
    # await asyncio.gather(*[test_sql(with_pool=True) for _ in range(100)])
    await asyncio.gather(*[
        test_connect(index=i, username="test",password="test",dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.10.99.20)(PORT=1521))(CONNECT_DATA=(SID=test1)))"),
        test_connect(index=i, username="test", password="test", dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.10.99.20)(PORT=1521))(CONNECT_DATA=(SID=test2)))")
    ])

    await asyncio.sleep(0.1)

if __name__ == '__main__':
    for i in range(10 ** 5):
        asyncio.run(performance_test(i))
    # asyncio.run(performance_test())

    # asyncio.run(test_sql(with_pool=True))
    # logger.info('\n')
    #
    # asyncio.run(run(with_pool=False))
    # logger.info('\n')
    #
    # asyncio.run(run(with_pool=True))
    # logger.info('\n')
