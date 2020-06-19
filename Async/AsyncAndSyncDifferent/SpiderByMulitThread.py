"""
@file: SpiderByMulitThread.py
@time: 2018/12/12
@author: sch
"""
import requests
import time
from threading import Thread
from lxml import etree


def ResponseParse(content):
    root_node = etree.HTML(content)
    book_list = root_node.xpath("/html/body/div[2]/div[5]/div[2]/div[2]/div/table/tbody/tr")
    for book_info in book_list:
        man_type = book_info.xpath(".//a[@class='type']/text()")[0]
        sub_type = book_info.xpath(".//a[@class='go-sub-type']/text()")[0]
        novel_name = book_info.xpath(".//a[@class='name']/text()")[0]
        novel_link = "https:" + book_info.xpath(".//a[@class='name']/@href")[0]
        novel_id = book_info.xpath(".//a[@class='name']/@data-bid")[0]
        author_name = book_info.xpath(".//a[@class='author']/text()")[0]
        author_link = "https:" + book_info.xpath(".//a[@class='author']/@href")[0]
        author_id = author_link.split('/')[-1]

        print("{novel_name} [{man_type}*{sub_type}]".format(novel_name=novel_name, man_type=man_type, sub_type=sub_type))


def Spider(url):
    try:
        with requests.get(url) as resp:
            # content = resp.content
            # ResponseParse(content)
            print(url, "over")
            pass
    except:
        print(url, "Exception")
        pass


def MulitThreadSpider():
    start_time = time.time()

    spider_list = list()
    for page in range(1, 1000):
        page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page=page)
        spider = Thread(target=Spider, args=(page_url,), name="Spider {page}".format(page=page))
        spider.start()
        spider_list.append(spider)

    for spider in spider_list:
        spider.join()

    print("Use time: ", time.time() - start_time)


if __name__ == '__main__':
    MulitThreadSpider()
