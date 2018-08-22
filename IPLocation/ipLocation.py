"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : ipLocation.py
 @Time    : 2018/8/15 16:16
"""
import requests
import json
import traceback
import asyncio
import aiohttp


async def lookup(ip):
    URL = 'http://ip.taobao.com/service/getIpInfo.php?ip=' + ip
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL, timeout=30) as response:
                assert response.status == 200
                data = await response.read()
                json_data = json.loads(data)
                if json_data[u'code'] == 0:
                    print("\nIP -> ", ip)
                    print('所在国家： ' + json_data[u'data'][u'country'])
                    print('所在地区： ' + json_data[u'data'][u'area'])
                    print('所在省份： ' + json_data[u'data'][u'region'])
                    print('所在城市： ' + json_data[u'data'][u'city'])
                    print('所属运营商：' + json_data[u'data'][u'isp'])
    except:
        print("\n\nSomething error")
        traceback.print_exc()

with open("ip.txt", "r") as f:
    ipList = json.load(f).keys()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([lookup(ip) for ip in ipList]))
