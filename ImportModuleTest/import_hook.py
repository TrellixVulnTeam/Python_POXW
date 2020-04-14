#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: import_test.py
@time: 2020/4/14
@author: alfons
"""
import sys
import time

# import importlib
#
#
# class MetaPathFinder:
#
#     def find_module(self, fullname, path=None):
#         # print('find_module {}'.format(fullname))
#         return MetaPathLoader()
#
#
# class MetaPathLoader:
#
#     def load_module(self, fullname):
#         # ``sys.modules`` 中保存的是已经导入过的 module
#         if fullname in sys.modules:
#             return sys.modules[fullname]
#
#         finder = sys.meta_path.pop(0)
#
#         start_time = time.time()
#         module = importlib.import_module(fullname)
#         print("load_module {} time use: {}'s".format(fullname, time.time() - start_time))
#
#         sys.meta_path.insert(0, finder)
#
#         return module
#
#
# sys.meta_path.insert(0, MetaPathFinder())

import imp


class ImportHook(object):

    def find_module(self, fullname, path=None):
        if fullname not in sys.modules:
            self.path = path
            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        start_time = time.time()
        module_info = imp.find_module(name, self.path)
        module = imp.load_module(name, *module_info)
        print("load_module {} time use: {}'s".format(name, time.time() - start_time))

        sys.modules[name] = module
        return module


sys.meta_path.insert(0, ImportHook())
