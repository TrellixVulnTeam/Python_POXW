"""
@file: apscheduler_test.py
@time: 2019/8/21
@author: alfons
"""
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

import os
import pytz
import thread
import threading
import time
import datetime

lock = threading.Lock()
num = 0
tid_list = list()


def tick(num):
    with lock:
        global tid_list

        tid = thread.get_ident()
        print "tick({n})".format(n=num)
        if tid not in tid_list:
            print "tid={tid}, pid={pid}".format(tid=tid, pid=os.getpid())
            tid_list.append(tid)

        print("Time is -> {}\n".format(datetime.datetime.now()))
        time.sleep(2)


def block_run():
    scheduler.add_job(tick, 'interval', coalesce=True, seconds=3)
    # scheduler.add_job(tick, 'cron', hour=17, minute=7)

    from datetime import date
    # scheduler.add_job(tick, "date", run_date="2019-8-22 9:37:00")


def background_interval_run():
    print("add task background_interval_run")
    scheduler.add_job(tick, 'interval', seconds=3)


def background_date_run():
    # print(datetime.datetime.now())
    global num

    num += 1
    scheduler.add_job(tick, 'date', args=(num,), run_date=datetime.datetime.now() + datetime.timedelta(seconds=1))
    pass


if __name__ == '__main__':
    # scheduler = BlockingScheduler()
    executors = {
        'default': ThreadPoolExecutor(2),
        'processpool': ProcessPoolExecutor(2)
    }

    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
    # scheduler = BackgroundScheduler(timezone=pytz.timezone(u'Asia/Shanghai'))
    scheduler.start()

    # block_run()
    # background_interval_run()
    # for i in range(10):
    scheduler.add_job(background_date_run, 'interval', seconds=0.1)

    while True:
        time.sleep(1)
