"""
@file: scrapy_example_spider.py
@time: 2018/11/30
@author: sch
"""
import scrapy


class QuoteSpider(scrapy.Spider):
    name = "scrapy_example"
    start_urls = ['https://doc.scrapy.org/en/latest/_static/selectors-sample1.html']

    def parse(self, response):
        print(response.xpath('//a[contains(@href, "image")]/@href').extract())
