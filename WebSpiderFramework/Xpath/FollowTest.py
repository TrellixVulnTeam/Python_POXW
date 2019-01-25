"""
@author: Alfons
@contact: alfons_xh@163.com
@file: FollowTest.py
@time: 19-1-13 上午10:56
@version: v1.0 
"""
from lxml import etree

content = """
<div id="info">
        <span class="pl">制片国家/地区:</span> 美国<br/>
        <span class="pl">语言:</span> 英语<br/>
        <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="2014-01-18(圣丹斯电影节)">2014-01-18(圣丹斯电影节)</span> / <span property="v:initialReleaseDate" content="2015-09-18(美国)">2015-09-18(美国)</span><br/>
        <span class="pl">片长:</span> <span property="v:runti/following::*me" content="88">88分钟</span><br/>
        <span class="pl">又名:</span> 虱子<br/>
        <span class="pl">IMDb链接:
            <a href="http://www.imdb.com/title/tt2490326" target="_blank" rel="nofollow">tt2490326</a><br>
        </span> 
</div>
"""

root_node = etree.HTML(content)

country_1 = root_node.xpath("//div[contains(@id, 'info')]/span[contains(@class, 'pl') and contains(text(), '制片国家/地区:')]/following::text()")
print(country_1)

country_2 = root_node.xpath("//div[contains(@id, 'info')]/span[contains(@class, 'pl') and contains(text(), '制片国家/地区:')]/following-sibling::text()")
print(country_2)

imdb_url = root_node.xpath("//div[contains(@id, 'info')]//child::a")
print(imdb_url)
pass
