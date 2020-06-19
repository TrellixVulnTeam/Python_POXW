#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: import_test.py
@time: 2020/4/14
@author: alfons
"""
import sys
import time
#
# sys.path.insert(0, "/tmp/pycharm_project_755/src")
is_importlib = True

if is_importlib:
    import importlib


    class MetaPathFinder:

        def find_module(self, fullname, path=None):
            # print('find_module {}'.format(fullname))
            return MetaPathLoader()


    class MetaPathLoader:

        def load_module(self, fullname):
            # ``sys.modules`` 中保存的是已经导入过的 module
            if fullname in sys.modules:
                return sys.modules[fullname]

            finder = sys.meta_path.pop(0)
            module = None
            try:

                start_time = time.time()
                # print("load_module {}".format(fullname))
                module = importlib.import_module(fullname)
                print("load_module {} time use: {}'s".format(fullname, time.time() - start_time))

            except Exception as e:
                # print str(e)
                module = None
            finally:
                sys.meta_path.insert(0, finder)
                return module


    sys.meta_path.insert(0, MetaPathFinder())
    # sys.meta_path.append(MetaPathFinder())

else:
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

            try:
                start_time = time.time()
                print "load_module {}， path -> {}".format(name, self.path)
                module_info = imp.find_module(name, self.path)
                module = imp.load_module(name, *module_info)
                print("load_module {} time use: {}'s".format(name, time.time() - start_time))

                sys.modules[name] = module
                return module
            except:
                return None


    sys.meta_path.insert(0, ImportHook())


def unhook():
    sys.meta_path.pop(0)
