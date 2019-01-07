"""
@file: JsonParserError.py
@time: 2019/01/05
@author: sch
"""
import json

error_json = '{"name": "Tom\0"}'
# json_result = json.loads(error_json)
json_result = json.loads(error_json, strict = False)

from queue import Queue

TASK_QUEUE = Queue()

i = TASK_QUEUE.get(timeout = 1)