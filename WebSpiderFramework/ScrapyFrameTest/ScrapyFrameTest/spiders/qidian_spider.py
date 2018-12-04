"""
@file: qidian_spider.py
@time: 2018/11/30
@author: sch
"""
import scrapy
from items import ScrapyframetestItem
from QidianPipelines import qidianSql


class QidianSpider(scrapy.Spider):
    name = "qidian"
    start_urls = [
        "https://www.qidian.com/all?orderId=&page=1&style=2&pageSize=20&siteid=1&pubflag=0&hiddenField=0"
    ]

    def start_requests(self):
        begin_url = "https://www.qidian.com/all?orderId=&page=1&style=2&pageSize=20&siteid=1&pubflag=0&hiddenField=0"
        yield scrapy.Request(url = begin_url, callback = self.parse)

    def parse(self, response):
        max_page = response.css(".lbf-pagination-item").xpath("./a/text()")[-2].extract()

        for page in range(1, int(max_page) + 1):
            page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page = page)
            yield scrapy.Request(url = page_url, callback = self.parse_page)

    def parse_page(self, response):
        book_list = response.css(".all-book-list").xpath(".//tbody/tr")
        for book_info in book_list:
            man_type = book_info.xpath(".//a[@class='type']/text()").extract()[0]
            sub_type = book_info.xpath(".//a[@class='go-sub-type']/text()").extract()[0]
            novel_name = book_info.xpath(".//a[@class='name']/text()").extract()[0]
            novel_link = "https:" + book_info.xpath(".//a[@class='name']/@href").extract()[0]
            novel_id = book_info.xpath(".//a[@class='name']/@data-bid").extract()[0]
            author_name = book_info.xpath(".//a[@class='author']/text()").extract()[0]
            author_link = "https:" + book_info.xpath(".//a[@class='author']/@href").extract()[0]
            author_id = author_link.split('/')[-1]

            # todo: 使用redis替代数据库查询
            if qidianSql.IsNovelExist(novel_id):
                self.log("{id} 重复，跳过数据库插入过程。".format(id = novel_id))
                continue

            qidianItem = ScrapyframetestItem(man_type = man_type, sub_type = sub_type, novel_name = novel_name, novel_link = novel_link,
                                             novel_id = novel_id, author_name = author_name, author_link = author_link, author_id = author_id)

            yield qidianItem

    def parse_novel(self, response):
        # todo: 小说目录分析
        pass

    def parse_author(self, response):
        # todo： 作者信息分析
        pass
