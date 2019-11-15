"""
@file: datetime_test.py
@time: 2019/11/12
@author: alfons
"""
import datetime

now = datetime.datetime.now()
print("now -> {}".format(now))
print("now.date() -> {}".format(now.date()))
print("now.time() -> {}".format(now.time()))
print("now.ctime() -> {}".format(now.ctime()))

print("now -> {}".format(now))
print("now + datetime.timedelta(hours=3.6) -> {}".format(now + datetime.timedelta(hours=3.6)))

import json

r_list = dict(sto1=dict(sp0=["r0_0", "r0_1"]), sto2=dict(sp0=["r0_0", "r0_1"]), sto3=dict(sp0=["r0_0", "r0_1"]))
print(json.dumps(r_list, indent=4))

r_list_2 = dict(r0_0=dict(sp0=["sto1", "sto2", "sto3"]), r0_1=dict(sp0=["sto1", "sto2", "sto3"]))
print(json.dumps(r_list_2, indent=4))