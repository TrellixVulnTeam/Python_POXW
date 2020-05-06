#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: cProfileDec.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/4/11 15:28
# History:
#=============================================================================
"""
import cProfile
import pstats


# 性能分析装饰器定义
def do_cprofile(filename, do_prof=True, sort_by="cumtime", print_stat=False, print_stat_count=100):
    """
    Decorator for function profiling.
    """

    def wrapper(func):
        def profiled_func(*args, **kwargs):
            # Flag for do profiling or not.
            if do_prof:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()

                ps = pstats.Stats(profile).sort_stats(sort_by)
                ps.dump_stats(filename)
                if print_stat:
                    ps.print_stats(print_stat_count)
            else:
                result = func(*args, **kwargs)
            return result

        return profiled_func

    return wrapper
