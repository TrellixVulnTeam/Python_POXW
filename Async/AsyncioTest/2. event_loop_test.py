"""
@file: 2. event_loop_test.py
@time: 2019/01/28
@author: sch
"""
import asyncio

event_loop = asyncio.get_event_loop()
print(id(event_loop))

new_event_loop = asyncio.new_event_loop()
print(id(new_event_loop))
pass
