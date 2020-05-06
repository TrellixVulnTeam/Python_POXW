#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: main.py
@time: 2019/9/11
@author: alfons
"""
import os

nvme_clean_cmd = """
                echo '#!/bin/sh' > /tmp/clean.sh;
                echo 'for i in {0..255}' >> /tmp/clean.sh;
                echo 'do' >> /tmp/clean.sh;
                echo 'if [ -c /dev/nvme$i ]' >> /tmp/clean.sh;
                echo 'then' >> /tmp/clean.sh;
                echo 'if [ ! -b /dev/nvme${i}n1 ]' >> /tmp/clean.sh;
                echo 'then' >> /tmp/clean.sh;
                echo 'echo \"/dev/nvme\"$i' >> /tmp/clean.sh;
                echo '/usr/local/sbin/nvme disconnect -d /dev/nvme$i' >> /tmp/clean.sh;
                echo 'fi' >> /tmp/clean.sh;
                echo 'fi' >> /tmp/clean.sh;
                echo 'done' >> /tmp/clean.sh;"""

os.popen(nvme_clean_cmd)


class a(object):
    def __init__(self):
        print("Hello world")

    def __del__(self):
        print("Goodbye world")


a_obj = a()

count_dist = [0.175664186478,
              0.00166893005371,
              0.628134012222,
              0.000432968139648,
              0.0789358615875,
              0.00590300559998,
              0.105345964432,
              0.00390410423279,
              0.0270540714264,
              0.000189065933228,
              0.000387907028198,
              0.00542712211609,
              0.00162410736084,
              0.0449039936066,
              0.0873229503632]

print("count -> {}".format(sum(count_dist)))

list_a = ["1_0", "1_1", "1_2"]
list_b = ["2_0", "2_1", "2_2"]
list_c = list()
[list_c.append([a, b]) for a in list_a for b in list_b]
# print list_c

from collections import defaultdict

dict_a = defaultdict(list)
pass

list_a = ["bo", "ao"]
str_a = str(list_a)
# print ','.join(set(list_a))
pass
