# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyframetestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    man_type = scrapy.Field()  # 主类型
    sub_type = scrapy.Field()  # 副类型
    novel_name = scrapy.Field()  # 小说名称
    novel_link = scrapy.Field()  # 小说链接
    novel_id = scrapy.Field()  # 小说ID标识
    author_name = scrapy.Field()  # 作者名称
    author_link = scrapy.Field()  # 作者链接
    author_id = scrapy.Field()  # 作者ID标识

    # def Init(self, man_type, sub_type, novel_name, novel_link, novel_id, author_name, author_link, author_id):
    #     self.man_type = man_type.
    #     self.sub_type = sub_type
    #     self.novel_name = novel_name
    #     self.novel_link = novel_link
    #     self.novel_id = novel_id
    #     self.author_name = author_name
    #     self.author_link = author_link
    #     self.author_id = author_id
