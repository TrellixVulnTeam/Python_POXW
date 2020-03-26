"""
@file: apscheduler_max_instance_test.py
@time: 2020/1/19
@author: alfons
"""
import time
import tornado.ioloop
from apscheduler.triggers.date import DateTrigger
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()


def child_job():
    print("start")
    time.sleep(60)
    print("end")


def main_job():
    sched.add_job(child_job, trigger=DateTrigger(), id="123")


sched.add_job(main_job, 'interval', seconds=5)

sched.start()
tornado.ioloop.IOLoop.instance().start()
