"""
@file: run.py.py
@time: 2018/11/29
@author: sch
"""
from scrapy import cmdline

name = 'qidian'
cmd = 'scrapy crawl {0} --nolog'.format(name)
#
# cmd = 'scrapy bench'

cmdline.execute(cmd.split())
