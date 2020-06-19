"""
@file: AsyncioTest.py
@time: 2018/12/11
@author: sch
"""
import time
import asyncio
import socket


async def DoSomeWork(index, sleep_time):
    print("{index} start time {sleep_time}'s".format(index = index, sleep_time = time.time()))
    await asyncio.sleep(sleep_time)
    print("{index} end time {sleep_time}'s".format(index = index, sleep_time = time.time()))


loop = asyncio.get_event_loop()


class callback(asyncio.Protocol):
    def data_received(self, data):
        """Called when some data is received.

        The argument is a bytes object.
        """
        print("data is ", data)
        pass

    def eof_received(self):
        print("eof_received.")
        pass


def callbackfunc(*args, **kwargs):
    pass


coro_getaddinfo = loop.getaddrinfo("www.baidu.com", port = 80, proto = socket.IPPROTO_TCP)
coro_creatcon = loop.create_connection(callback, host = "192.168.2.41", port = 80)

work_list = [coro_getaddinfo, coro_creatcon]

result = loop.run_until_complete(asyncio.wait(work_list))
result = loop.run_until_complete(coro_getaddinfo)
print(result)
pass

# work_list = list()
#
# for i in range(5):
#     work_list.append(DoSomeWork(i, 1))
#
# loop.run_until_complete(asyncio.wait(work_list))
# print("I'm end.")
