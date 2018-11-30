"""
@file: quote_spider.py
@time: 2018/11/29
@author: sch
"""
import scrapy


class QuoteSpider(scrapy.spiders.Spider):
    name = "quote"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # def start_requests(self):
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #
    #     for url in urls:
    #         yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        response.urljoin("1")
        page = response.url.split("/")[-2]
        filename = "quote-{page}.html".format(page = page)
        with open(filename, "wb") as f:
            f.write(response.body)
        self.log('Save file {name}'.format(name = filename))
