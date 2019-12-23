"""
@file: redisTest.py
@time: 2018/12/05
@author: sch
"""
import redis

redis_object = redis.Redis(host="192.168.1.52")
r = redis_object.keys("*")
redis_object.set("rebalance_after_del_disk_task", 43)
r_get= redis_object.get("rebalance_aer_del_disk_task")
pass