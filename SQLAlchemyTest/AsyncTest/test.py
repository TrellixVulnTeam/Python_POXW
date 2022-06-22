#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: test.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2022/3/17 4:43 PM
# History:
#=============================================================================
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.orm import selectinload, Query
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import concurrent.futures
import os
import typing
from typing import Any
import time
from multiprocessing.pool import ThreadPool

from SQLAlchemyTest.AsyncTest.models.qdata import QDataCluster, QDataNode, RacCluster
from SQLAlchemyTest.AsyncTest.base import create_all_table, create_database, open_session, open_async_session

from sqlalchemy.util.concurrency import greenlet_spawn

# 线程执行器，线程数量 = CPU数量 * 10
thread_executor = concurrent.futures.ThreadPoolExecutor(max_workers=(os.cpu_count() or 10) * 10)


# ====================== 同步方法转换为异步方法 ======================
async def run_as_async(func: typing.Any, *args: Any, **kwargs: Any) -> Any:
    """
    在异步方法中，使用await改造同步方法

    使用方法:
        def func_A(timeout: int):
            time.sleep(timeout)

        async def func_B(timeout: int):
            await run_as_async(func_A, timeout)
            await run_as_async(func_A, timeout=timeout)

    :param func: 执行的同步方法
    :param args: 请求参数
    :param kwargs: 请求参数
    :return:
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(thread_executor, lambda: func(*args, **kwargs))


async def run_parallel(
        async_funcs,
        loop=None,
        return_exceptions: bool = False,
) -> Any:
    """
    并发执行多个异步方法，以节省时间消耗。

    需要注意的是，并发执行多个异步方法，在执行结束之后不会返回全部的结果。需要通过传入的参数进行获取

    async def func(a):
        ...

    await run_parallel(coros_or_futures=[func(i) for i in range(100)])

    :param async_funcs: 异步方法
    :param loop: 事件循环
    :param return_exceptions: 是否在执行异常时返回
    :return:
    """
    return await asyncio.gather(
        *async_funcs,
        loop=loop,
        return_exceptions=return_exceptions,
    )


# ====================== sync 测试 ======================
async def test_sync_sql():
    with open_session() as sync_session:
        query = sync_session.query(QDataCluster)

        # print(await run_parallel([
        #     greenlet_spawn(sync_session.query(QDataNode).filter(QDataNode.cluster_id == cluster_obj.id, QDataNode.type.in_(["compute", "sanfree"])).all)
        #     for cluster_obj in await greenlet_spawn(query.all)
        # ]))

        # print(await run_parallel([
        #     run_as_async(sync_session.query(QDataNode).filter(QDataNode.cluster_id == cluster_obj.id, QDataNode.type.in_(["compute", "sanfree"])).all)
        #     for cluster_obj in await run_as_async(query.all)
        # ]))

        for cluster_obj in query.all():
            rac_clusters = sync_session.query(RacCluster).all()     #type: RacCluster
            for rac_cluster in rac_clusters:
                print(rac_cluster.nodes)
        pass


# ====================== sync 并发 测试 ======================
def test_sync_sql_single():
    with open_session() as sync_session:
        query = sync_session.query(QDataCluster).options(
            selectinload(QDataCluster.nodes),
        )

        for cluster_obj in query.all():
            print(sync_session.query(QDataNode).filter(QDataNode.cluster_id == cluster_obj.id, QDataNode.type.in_(["compute", "sanfree"])).all())
    pass


def test_sync_sql_performance():
    total_num = 1
    start_time = time.time()
    with ThreadPool(1000) as pool:
        for i in range(total_num):
            pool.apply_async(test_sync_sql_single)
        pool.close()
        pool.join()

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


# ====================== async 测试 ======================
async def async_test(async_session: AsyncSession):
    # result = await async_session.execute(
    #     select(QDataCluster).options(
    #         selectinload(QDataCluster.nodes),  # 必须
    #     ))
    #
    # print(await run_parallel([
    #     async_session.execute(
    #         select(QDataNode).filter(QDataNode.cluster_id == cluster_obj.id, QDataNode.type.in_(["compute", "sanfree"]))
    #     ) for cluster_obj in result.scalars()
    # ]))

    all_cluster = await async_session.execute(async_session.sync_session.query(QDataCluster).options(
        selectinload(QDataCluster.nodes),
    ).statement)

    print([res.scalars().first() for res in await run_parallel([
        async_session.execute(
            async_session.sync_session.query(QDataNode).filter(QDataNode.cluster_id == cluster_obj.id, QDataNode.type.in_(["compute", "sanfree"])).statement
        ) for cluster_obj in all_cluster.scalars().all()
    ])])


async def test_async_sql():
    total_num = 10 ** 1
    start_time = time.time()
    async with open_async_session() as async_session:  # type: AsyncSession
        await run_parallel([async_test(async_session) for _ in range(total_num)])

    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")


if __name__ == '__main__':
    total_num = 10 ** 0
    start_time = time.time()
    asyncio.run(run_parallel(
        [
            test_sync_sql()
            for _ in range(total_num)
        ]
    ))
    print("\n\nTotal time use: {:.2f}'s.".format(time.time() - start_time))
    print(f"Total number: {total_num}")

    # asyncio.run(test_async_sql())

    # test_sync_sql_performance()
