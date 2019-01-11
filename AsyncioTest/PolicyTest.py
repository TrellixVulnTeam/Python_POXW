"""
@file: PolicyTest.py
@time: 2019/01/11
@author: sch
"""
import sys
import asyncio

loop_policy = asyncio.get_event_loop_policy()
print("loop_policy -> ", loop_policy)

loop = asyncio.get_event_loop()
print("loop -> ", loop)

select_loop = asyncio.SelectorEventLoop()
print("select_loop - > ", select_loop)

abstract_loop = asyncio.AbstractEventLoop()
print("abstract_loop - > ", abstract_loop)

if sys.platform == 'win32':
    proactor_loop = asyncio.ProactorEventLoop()
    print("proactor_loop -> ", proactor_loop)

asyncio.set_event_loop(abstract_loop)
print(asyncio.get_event_loop())

asyncio.new_event_loop()
print(asyncio.get_event_loop())
