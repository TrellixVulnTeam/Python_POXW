"""
@file: AiohttpTest.py
@time: 2018/12/13
@author: sch
"""
import asyncio
import aiohttp
import socket
import traceback

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36)"
}


async def AiohttpTest(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url, timeout = 10, verify_ssl = False) as resp:
                print("stataus:", resp.status)
                # print("text: ", await resp.text())
    except ConnectionRefusedError:
        print("ConnectionRefusedError")
    except socket.error as e:
        if hasattr(e, "os_error"):
            print(type(e.os_error))

        print(type(e))
    except:
        traceback.print_exc()


for i in range(10):
    url = "https://{ip}:{port}".format(ip = "108.173.200.174", port = 61878)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(AiohttpTest(url))
    loop.close()
