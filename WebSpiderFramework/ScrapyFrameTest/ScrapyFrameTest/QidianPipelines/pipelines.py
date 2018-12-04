"""
@file: pipelines.py
@time: 2018/11/30
@author: sch
"""
from items import ScrapyframetestItem
from QidianPipelines.qidianSql import QidianDb
from scrapy.exceptions import DropItem


class ScrapyframetestPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ScrapyframetestItem):
            novel_id = item["novel_id"]
            novel_name = item["novel_name"]
            novel_link = item["novel_link"]
            man_type = item["man_type"]
            sub_type = item["sub_type"]
            author_id = item["author_id"]
            author_name = item["author_name"]
            author_link = item["author_link"]

            QidianDb.insert_table(novel_id = novel_id,
                                  novel_name = novel_name,
                                  novel_link = novel_link,
                                  man_type = man_type,
                                  sub_type = sub_type,
                                  author_id = author_id,
                                  author_name = author_name,
                                  author_link = author_link)
            return item
        else:
            raise DropItem("Item type not allow!")

    def open_spider(self, spider):
        print("Begin Spider!")
        QidianDb.OpenDB()

    def close_spider(self, spider):
        print("End Spider!")
        QidianDb.CloseDB()
