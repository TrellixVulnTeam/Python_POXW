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
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', coalesce=True, seconds=3)
    # scheduler.add_job(tick, 'cron', hour=17, minute=7)

    from datetime import date
    # scheduler.add_job(tick, "date", run_date="2019-8-22 9:37:00")

    scheduler.start()


def background_run():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)

    scheduler.start()
    time.sleep(10)


if __name__ == '__main__':
    block_run()
    # background_run()
