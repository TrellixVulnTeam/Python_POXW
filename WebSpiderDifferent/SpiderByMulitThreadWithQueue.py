"""
@file: SpiderByMulitThread.py
@time: 2018/12/12
@author: sch
"""
import requests
import time
from queue import Queue
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

        print("{novel_name} [{man_type}*{sub_type}]".format(novel_name = novel_name, man_type = man_type, sub_type = sub_type))


url_queue = Queue()
run = True
thread_num = 1000


def Spider():
    while run:
        if url_queue.qsize() != 0:
            url = url_queue.get()
            with requests.get(url) as resp:
                content = resp.content
                ResponseParse(content)


def MulitThreadSpider():
    spider_pool = list()
    for i in range(thread_num):
        spider = Thread(target = Spider, args = (), name = "Thread {}.".format(i))
        spider.start()
        spider_pool.append(spider)

    start_time = time.time()

    for page in range(1, 1000):
        page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page = page)
        url_queue.put(page_url)

    while url_queue.qsize() != 0:
        time.sleep(0.01)

    global run
    run = False

    for spider in spider_pool:
        spider.join()

    print("Use time: ", time.time() - start_time)


if __name__ == '__main__':
    MulitThreadSpider()
