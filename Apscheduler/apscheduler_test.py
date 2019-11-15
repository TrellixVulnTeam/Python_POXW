"""
@file: apscheduler_test.py
@time: 2019/8/21
@author: alfons
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

import os
import time
import datetime


def tick():
    print("Time is -> {}".format(datetime.datetime.now()))


def block_run():
    scheduler.add_job(tick, 'interval', coalesce=True, seconds=3)
    # scheduler.add_job(tick, 'cron', hour=17, minute=7)

    from datetime import date
    # scheduler.add_job(tick, "date", run_date="2019-8-22 9:37:00")


def background_interval_run():
    print("add task background_interval_run")
    scheduler.add_job(tick, 'interval', seconds=3)


def background_date_run():
    print(datetime.datetime.now())
    scheduler.add_job(tick, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
    pass


if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.start()

    # block_run()
    # background_interval_run()
    background_date_run()

    time.sleep(10)
