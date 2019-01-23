"""
@file: SpiderByAiohttp.py
@time: 2018/12/12
@author: sch
"""
import asyncio
import aiohttp
import socket
import time
import traceback
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

        print(
            "{novel_name} [{man_type}*{sub_type}]".format(novel_name=novel_name, man_type=man_type, sub_type=sub_type))


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36)"
}


async def Spider(index, url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, verify_ssl=False) as resp:
                # async with session.get(url, timeout = 10, verify_ssl = False, proxy="http://192.168.2.53:1080") as resp:
                # ResponseParse(await resp.text())
                print(url, "over")

        except aiohttp.client_exceptions.ClientConnectorError:
            print(url, "ClientConnectorError")
        except asyncio.TimeoutError:
            print(url, "Timeout")


def AsyncSpider(start=0, end=1000):
    tasks = list()

    loop = asyncio.get_event_loop()
    for page in range(start, end):
        page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page=page)
        tasks.append(Spider(page, page_url))

    loop.run_until_complete(asyncio.wait(tasks))


def AsyncWithMultiProcess():
    from multiprocessing import Process

    process_list = list()
    for i in range(4):
        p = Process(target=AsyncSpider, args=(i * 250, (i + 1) * 250), name="Process {}".format(i))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()


if __name__ == '__main__':
    start_time = time.time()

    # AsyncSpider(0, 500)
    # AsyncSpider(500, 1000)

    AsyncWithMultiProcess()

    print("Use time: ", time.time() - start_time)
