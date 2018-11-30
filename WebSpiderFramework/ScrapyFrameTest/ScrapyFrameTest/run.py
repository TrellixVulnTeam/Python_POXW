"""
@file: run.py.py
@time: 2018/11/29
@author: sch
"""
from scrapy import cmdline

name = 'qidian'
cmd = 'scrapy crawl {0}'.format(name)

cmdline.execute(cmd.split())
