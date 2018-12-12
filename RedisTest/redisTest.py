"""
@file: redisTest.py
@time: 2018/12/05
@author: sch
"""
import redis

redis_object = redis.Redis(db=1)
redis_object.mset({"zzzzzzz": "hello1", "zz": "hello2"})
