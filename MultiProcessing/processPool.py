    #!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: processPool.py
@time: 2019/6/22 下午5:12
@version: v1.0 
"""
from multiprocessing.pool import Pool


class Test:
    def func_a(self, a, b):
        return a + b

    def func_pool(self):
        p = Pool(processes=4)
        for i in range(10000):
            r = p.apply_async(self.func_a, args=(i, i+1))
        print(p.get())


if __name__ == '__main__':
    t = Test()
    t.func_pool()
