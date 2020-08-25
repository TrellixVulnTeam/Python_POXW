#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
import operator

print(any([]))
from enum import Enum



import asyncio

print(hash((1,2)))
print(hash((1,2)))
print(hash((1,3)))
async def func_a():
    await asyncio.sleep(3)
    print("I'm sleep 10's.")


def func_b():
    asyncio.run(func_a())

func_b()


class ReplaceDiskWebsocketStepEnum(int, Enum):
    pre_check = 2 ** 0
    user_confirm = 2 ** 1
    disk_delete_from_ASM = 2 ** 2
    ASM_rebalance_before_replace = 2 ** 3
    delete_lun = 2 ** 4
    unload_physical_device = 2 ** 5
    replace_disk = 2 ** 6
    load_physical_device = 2 ** 7
    format_physical_device = 2 ** 8
    add_lun = 2 ** 9
    qlink_mount = 2 ** 10
    disk_add_to_ASM = 2 ** 11
    ASM_rebalance_after_replace = 2 ** 12

print(int(ReplaceDiskWebsocketStepEnum.pre_check))

for i in ReplaceDiskWebsocketStepEnum:
    # print(dir(i))
    print(f"{i.name}={i.value}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.pre_check=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.user_confirm=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.disk_delete_from_ASM=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.ASM_rebalance_before_replace=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.delete_lun=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.unload_physical_device=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.replace_disk=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.load_physical_device=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.format_physical_device=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.add_lun=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.qlink_mount=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.disk_add_to_ASM=}")
print(f"{35 & ReplaceDiskWebsocketStepEnum.ASM_rebalance_after_replace=}")

import os
import re
from collections import defaultdict

ws_map = defaultdict(list)

for _ in ws_map[1]:
    print(_)
print(ws_map)

#
# print("{:.1f}x".format(2.26))
#
# list_a = ['a', 'b']
# list_b = ['a', 'c', 'd']
#
# print(bool(set(list_b) - set(list_b)))
#
# print('a' in (list_b + list_a))
#
# EVENT_SCHEDULER_STARTED = EVENT_SCHEDULER_START = 2 ** 0
# EVENT_SCHEDULER_SHUTDOWN = 2 ** 1
# EVENT_SCHEDULER_PAUSED = 2 ** 2
# EVENT_SCHEDULER_RESUMED = 2 ** 3
# EVENT_EXECUTOR_ADDED = 2 ** 4
# EVENT_EXECUTOR_REMOVED = 2 ** 5
# EVENT_JOBSTORE_ADDED = 2 ** 6
# EVENT_JOBSTORE_REMOVED = 2 ** 7
# EVENT_ALL_JOBS_REMOVED = 2 ** 8
# EVENT_JOB_ADDED = 2 ** 9
# EVENT_JOB_REMOVED = 2 ** 10
# EVENT_JOB_MODIFIED = 2 ** 11
# EVENT_JOB_EXECUTED = 2 ** 12
# EVENT_JOB_ERROR = 2 ** 13
# EVENT_JOB_MISSED = 2 ** 14
# EVENT_JOB_SUBMITTED = 2 ** 15
# EVENT_JOB_MAX_INSTANCES = 2 ** 16
#
# from datetime import datetime
# print(str(datetime.now()))
# print(f"all([]) -> {all([])}")
# print(f"EVENT_SCHEDULER_STARTED -> {EVENT_SCHEDULER_STARTED}: The scheduler was started")
# print(f"EVENT_SCHEDULER_START -> {EVENT_SCHEDULER_START}: The scheduler was started")
# print(f"EVENT_SCHEDULER_SHUTDOWN -> {EVENT_SCHEDULER_SHUTDOWN}: The scheduler was shut down")
# print(f"EVENT_SCHEDULER_PAUSED -> {EVENT_SCHEDULER_PAUSED}: Job processing in the scheduler was paused")
# print(f"EVENT_SCHEDULER_RESUMED -> {EVENT_SCHEDULER_RESUMED}: Job processing in the scheduler was resumed")
# print(f"EVENT_EXECUTOR_ADDED -> {EVENT_EXECUTOR_ADDED}: An executor was added to the scheduler")
# print(f"EVENT_EXECUTOR_REMOVED -> {EVENT_EXECUTOR_REMOVED}: An executor was removed to the scheduler")
# print(f"EVENT_JOBSTORE_ADDED -> {EVENT_JOBSTORE_ADDED}: A job store was added to the scheduler")
# print(f"EVENT_JOBSTORE_REMOVED -> {EVENT_JOBSTORE_REMOVED}: A job store was removed from the scheduler")
# print(f"EVENT_ALL_JOBS_REMOVED -> {EVENT_ALL_JOBS_REMOVED}: All jobs were removed from either all job stores or one particular job store")
# print(f"EVENT_JOB_ADDED -> {EVENT_JOB_ADDED}: A job was added to a job store")
# print(f"EVENT_JOB_REMOVED -> {EVENT_JOB_REMOVED}: A job was removed from a job store")
# print(f"EVENT_JOB_MODIFIED -> {EVENT_JOB_MODIFIED}: A job was modified from outside the scheduler")
# print(f"EVENT_JOB_EXECUTED -> {EVENT_JOB_EXECUTED}: A job was executed successfully")
# print(f"EVENT_JOB_ERROR -> {EVENT_JOB_ERROR}: A job raised an exception during execution")
# print(f"EVENT_JOB_MISSED -> {EVENT_JOB_MISSED}: 	A job’s execution was missed")
# print(f"EVENT_JOB_SUBMITTED -> {EVENT_JOB_SUBMITTED}: A job was submitted to its executor to be run")
# print(f"EVENT_JOB_MAX_INSTANCES -> {EVENT_JOB_MAX_INSTANCES}: A job being submitted to its executor was not accepted by the executor because the job has already reached its maximum concurrently executing instances")
