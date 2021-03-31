#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: Test_loguru.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2021/3/28 10:35 下午
# History:
#=============================================================================
"""
import sys
from datetime import datetime
from loguru import logger

# logger.add("file.log", format="{extra[ip]} {extra[user]} {message}")
# context_logger = logger.bind(ip="192.168.0.1", user="someone")
# context_logger.info("Contextualize your logger easily")
# context_logger.bind(user="someone_else").info("Inline binding of extra attribute")
# context_logger.info("Use kwargs to add context during formatting: {user}", user="anybody")

logger.add("special.log", filter=lambda record: "special" in record["extra"])
logger.debug("This message is not logged to the file")
logger.bind(special=True).info("This message, though, is logged to the file!")

# logger.add(sys.stderr, format="{extra[utc]} {message}")
# logger = logger.patch(lambda record: record["extra"].update(utc=datetime.utcnow()))
# logger.debug("This message is not logged to the file")

# logger.opt(lazy=True).debug("If sink level <= DEBUG: {x}", x=lambda: 2**64)
#
# # By the way, "opt()" serves many usages
# logger.opt(exception=True).info("Error stacktrace added to the log message (tuple accepted too)")
# logger.opt(colors=True).info("Per message <blue>colors</blue>")
# logger.opt(record=True).info("Display values from the record (eg. {record[thread]})")
# logger.opt(raw=True).info("Bypass sink formatting\n")
# # logger.opt(depth=1).info("Use parent stack context (useful within wrapped functions)")
# logger.opt(capture=False).info("Keyword arguments not added to {dest} dict", dest="extra")
#
# new_level = logger.level("SNAKY", no=38, color="<yellow>", icon="🐍")
# logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
# logger.log("SNAKY", "Here we go!")

# import logging
# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = logger.level(record.levelname).name
#         except ValueError:
#             level = record.levelno
#
#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1
#
#         logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
#
# logging.basicConfig(handlers=[InterceptHandler()], level=0)
# logging.info("helloworld")