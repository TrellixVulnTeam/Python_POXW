"""
@file: pipelines.py
@time: 2018/11/30
@author: sch
"""
from items import ScrapyframetestItem

class ScrapyframetestPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ScrapyframetestItem):
            novel_id = item["novel_id"]

        return item
