"""
@file: datetime_test.py
@time: 2019/11/12
@author: alfons
"""
import datetime
import time
import json

# s = sum([])
# print s
# pass
#
# list_a = [
#     ['port', 'target_id', 'target_name', 'target_state', 'driver', 'acl', 'lun_id', 'lun_path', 'lun_size', 'external'],
#     ['3261', 1, 's01.3261.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN1\x1b[0m', '8592 MB', 'NO'],
#     ['3262', 1, 's01.3262.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN2\x1b[0m', '1395868 MB', 'NO'],
#     ['3264', 1, 's01.3264.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN4\x1b[0m', '1395868 MB', 'NO'],
#     ['3265', 1, 's01.3265.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN5\x1b[0m', '1395868 MB', 'NO'],
#     ['3266', 1, 's01.3266.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN6\x1b[0m', '1395868 MB', 'NO'],
#     ['3268', 1, 's01.3268.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN8\x1b[0m', '1395868 MB', 'NO'],
#     ['3270', 1, 's01.3270.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN10\x1b[0m', '1395868 MB', 'NO'],
#     ['3276', 1, 's01.3276.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN16\x1b[0m', '1395868 MB', 'NO'],
#     ['3278', 1, 's01.3278.01', 'ready', 'nvmf', '172.16.129.0/24\n172.16.128.0/24', '1', '\x1b[92m/dev/qdisk/LUN18\x1b[0m', '1395868 MB', 'NO']
# ]
#
# print list_a[0][0]
#
# dict_a = {
#     "controller_ip": "10.10.100.11",
#     "nodes": [{
#         "node_id": 9,
#         "node_name": "qdata-sto35-dev",
#         "address": "10.10.160.35"
#     }]
# }
# print json.dumps(dict_a, indent=4)
#
# d_a = {
#     "node_id": 7,
#     "pool_id": 7,
#     "vg_name": "ls",
#     "sp_name": "ls_ls",
#     "disk_name": "n00005e000"
# }
#
# a = datetime.datetime.strptime("2020-02-18 21:05:34.118000", '%Y-%m-%d %H:%M:%S.%f')
# b = a.strftime('%Y-%m-%d')
#
# print time.time()
# print datetime.datetime.fromtimestamp(time.time())
#

import pytz
# now = datetime.datetime.now(tz=pytz.timezone(u'Asia/Shanghai'))
# print(f"now -> {now}")
# print("now.date() -> {}".format(now.date()))
# print("now.time() -> {}".format(now.time()))
# print("now.ctime() -> {}".format(now.ctime()))
#
# print("now -> {}".format(now))
# print("now + datetime.timedelta(hours=3.6) -> {}".format(now + datetime.timedelta(hours=3.6)))

tz = pytz.timezone(u'Asia/Shanghai')
print(f"Shanghai -> {datetime.datetime.now(tz=pytz.timezone(u'Asia/Shanghai'))}")
print(f"UTC -> {datetime.datetime.now(tz=pytz.utc)}")
