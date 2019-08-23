"""
@file: 9.Async_asyncio.py
@time: 2019/8/23
@author: alfons
"""
import sys
import asyncio
import aiohttp

loop = asyncio.get_event_loop()


async def fetch(url):
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url) as response:
            response = await response.read()

            print(response)
            sys.stdout.flush()
            return response


if __name__ == '__main__':
    import time

    start_time = time.time()
    tasks = [fetch(url="https://www.baidu.com") for _ in range(10)]

    loop.run_until_complete(asyncio.gather(*tasks))
    print("Use time -> {}'s.".format(time.time() - start_time))
