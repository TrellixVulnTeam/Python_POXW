#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: GzipDemo.py 
@time: 2018/2/6 18:17 
@version: v1.0 
"""
import gzip
header = b"""HTTP/1.1 200 OK
Server: Tengine
Content-Type: application/json
Transfer-Encoding: chunked
Connection: keep-alive
Date: Mon, 29 Jan 2018 11:11:49 GMT
Vary: Accept-Encoding
X_TT_LOGID: 20180129191149010011040146191322
X-TT-LOGID: 20180129191149010011040146191322
Vary: Accept-Encoding
Content-Encoding: gzip
Vary: Accept-Encoding
X-SS-REQ-TICKET: 1517224309159
Vary: Accept-Encoding
X-TT-TIMESTAMP: 1517224309.226
Via: cache13.l2nu16-1[29,0], cache7.cn579[70,0]
Timing-Allow-Origin: *
EagleId: 7ae4facf15172243091678869e"""
content = b"""{"message": "success", "data": {"tip_version_name": "6.4.8", "pre_download_max_wait_seconds": 3600, "real_version_name": "6.5.6", "whats_new": "\u4fee\u590d\u5df2\u77e5\u95ee\u9898\uff0c\u4f18\u5316\u7528\u6237\u4f53\u9a8c", "latency": 10, "title": "\u68c0\u6d4b\u5230\u66f4\u65b0", "already_download_tips": "\u4fee\u590d\u5df2\u77e5\u95ee\u9898\uff0c\u4f18\u5316\u7528\u6237\u4f53\u9a8c", "pre_download": 0, "force_update": 0, "download_url": "http://lf3-ttcdn-tos.pstatp.com/obj/rocketpackagebackup/bugfix_online/1517212840NewsArticle_update_v6.5.6_7609b89.apk", "inhouse": 0, "real_version_code": 65674, "verbose_name": "\u4eca\u65e5\u5934\u6761", "tip_version_code": 648}}"""
with open("news_article.gz", "wb") as f:
    encode = gzip.compress(content)
    header = header.replace(b'\n', b'\r\n')
    f.write(header)
    f.write(b"\r\n\r\n")
    f.write(str(hex(len(encode))).encode()[2:])
    f.write(b"\r\n")
    f.write(encode)
    f.write(b"\r\n0\r\n\r\n")


header_a = b"""HTTP/1.1 200 OK
Server: nginx/1.6.0
Date: Wed, 31 Jan 2018 02:19:29 GMT
Content-Type: text/xml; charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive
X-Powered-By: PHP/5.4.27"""
content_a = """<?xml version="1.0" encoding="utf-8"?>
<listpack upflag="0">
<gamelist>
<glist sid="205" gid="20000" gver="9" glvl="1" gfup="0" gname="真人斗地主2" glib="com.mas.wawagame.HLlord.uc" gpath="http://wwhotupsrc.wawagame.cn/origapk/10007/205/gver9/lvl1/10007_205_9.1_com.mas.wawagame.HLlord.uc.obb" gsize="1451651" patch="0" omd5="" nmd5="" dmd5="d41d8cd98f00b204e9800998ecf8427e" flag="68" notifytitle="" notifymsg=""/>
</gamelist>
</listpack>"""

with open("HLlord.txt", "wb") as f:
    header_a = header_a.replace(b'\n', b'\r\n')
    f.write(header_a)
    f.write(b"\r\n\r\n")
    f.write(str(hex(len(content_a.encode()))).encode()[2:])
    f.write(b"\r\n")
    f.write(content_a.encode())
    f.write(b"\r\n0\r\n\r\n")

header_b = b"HTTP/1.1 200 OK\r\n\
Date: Tue, 30 Jan 2018 02:37:04 GMT\r\n\
Content-Type: text/html; charset=UTF-8\r\n\
Transfer-Encoding: chunked\r\n\
Connection: keep-alive\r\n\
Vary: Accept-Encoding\r\n\
Server: nginx/1.6.2\r\n\
X-Powered-By: PHP/7.0.17\r\n\
Set-Cookie: PHPSESSID=tvsaprcllf8tgiod39c2bcp8r0; path=/\r\n\
Expires: Thu, 19 Nov 1981 08:52:00 GMT\r\n\
Cache-Control: no-store, no-cache, must-revalidate\r\n\
Content-Encoding: gzip"

content_b = b"""{"ignore_btn":"\u7a0d\u540e\u66f4\u65b0","update_btn":"\u9a6c\u4e0a\u66f4\u65b0","update_msg":"\u5927\u5409\u5927\u5229\uff0c\u4eca\u665a\u5403\u9e21\uff01","update_title":"\u7248\u672c\u66f4\u65b0","update_url":"http:\/\/img-ys011.didistatic.com\/static\/apprel\/theone\/android\/didi_psngr_5.5.30.apk","version":"5.5.30","version_code":506,"is_force":1,"images":[],"errno":0,"errmsg":"SUCCESS","exp_user":0}"""
with open("didichuxing.gz", "wb") as f:
    encode = gzip.compress(content_b)
    f.write(header_b)
    f.write(b"\r\n\r\n")
    f.write(str(hex(len(encode))).encode()[2:])
    f.write(b"\r\n")
    f.write(encode)
    f.write(b"\r\n0\r\n\r\n")


header_c = b"""HTTP/1.1 200 OK
Server: Tengine
Date: Tue, 30 Jan 2018 06:37:09 GMT
Content-Length: 699
Connection: keep-alive
Content-Encoding: gzip"""

content_c = b"""{"coll_inert_duration":"300000","repo_url_new":"http://config.mobile.meituan.com/download/locatejar","interval":"1990000","fs_upload_apps_min":"20","enable_megrez_module":"false","enable_megrez_1":"true","repo_url":"http://config.mobile.meituan.com/download/locatejar","enable_alog_write":"true","coll_wifiscan_duration":"300000","coll_wifi_interval":"23","alog_upload_limit":"100","enable_report":"true","crash_upload_limit":"5","vaild_platform":"com.sankuai.moma;com.sankuai.meituan;com.sankuai.meituan.takeoutnew;com.sankuai.movie;com.sankuai.meituan.merchant;com.sankuai.meituan.pai;com.sankuai.breakfast.workbench;com.sankuai.meituan.waimai.bee;com.sankuai.meituan.waimai.sunflower;com.sankuai.xmpp;com.meituan.mars;com.meituan.tower;com.dianping.moma;com.dianping.v1;com.sankuai.moviepro;com.dianping.dppos;com.sankuai.meituan.dispatch.crowdsource;com.dianping.crm;com.sankuai.meituan.dispatch.homebrew;com.dianping.iris;com.sankuai.poscashier;com.dianping.luna;com.meituan.mars.compareapp;com.meituan.phoenix;com.mooyoo.r2;com.meituan.xm;com.sankuai.hardware.mtconnectservice;com.sankuai.arm.moma;locate.meituan.com.collectatpos;com.sankuai.ssp.saori.android;com.example.zhangdi.locatetest;com.meituan.sankuai.seagull;com.meituan.beeRN;com.meituan.retail.c.android;com.meituan.qcs.c.android;com.baobaoaichi.iretail;com.sankuai.mhotel;com.meituan.sankuai.erpboss;com.sankuai.conch.discount;com.meituan.xgfe.android.camelbd;com.meituan.b2b.camelbd.ep;com.sankuai.meituan.pai;com.meituan.iStoreCollection.ep;com.meituan.phoenix.keeper.android;com.dianping.dpposwed;com.sankuai.erp.lineup;com.meituan.lottery.merchant;com.meituan.tripBizApp;com.sankuai.erp.mcashier;com.sankuai.conch;com.dianping.roc","gps_mode":"0","update_time":"1418278799030","loc_wifi_interval":"24","coll_inert_interval":"30000","enable_alog_upload":"true","clear_collector_jar":"false","enable_subprocess_megrez":"true"}"""
with open("dazhongdianping.gz", "wb") as f:
    encode = gzip.compress(content_c)
    header_c = header_c.replace(b'\n', b'\r\n')
    f.write(header_c)
    f.write(b"\r\n\r\n")
    f.write(encode)
    f.write(b"\r\n\r\n")

header_d = b"""HTTP/1.1 200 OK
Server: Tengine
Date: Tue, 30 Jan 2018 09:43:55 GMT
Content-Type: application/json;charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
M-Appkey: com.sankuai.wpt.eva.evaapi
M-SpanName: PluginsController.hydraList
M-Host: 10.23.75.184
Content-Encoding: gzip"""
content_d = b"""[{"name":840,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/840_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"},{"name":843,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/843_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"},{"name":854,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/854_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"},{"name":878,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/878_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"},{"name":882,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/882_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"},{"name":1341,"url":"http://s3.meituan.net/v1/mss_e63d09aec75b41879dcb3069234793ac/patch/1341_6149d4e704c356ba843762eb4c5d448f.apk","md5":"d41d8cd98f00b204e9800998ecf8427e"}]"""
with open("meituan.gz", "wb") as f:
    encode = gzip.compress(content_d)
    header_d = header_d.replace(b'\n', b'\r\n')
    f.write(header_d)
    f.write(b"\r\n\r\n")
    f.write(str(hex(len(encode))).encode()[2:])
    f.write(b"\r\n")
    f.write(encode)
    f.write(b"\r\n0\r\n\r\n")

header_e = """HTTP/1.1 200 OK
Date: Fri, 09 Feb 2018 03:36:13 GMT
Content-Type: text/xml; charset=utf-8
Content-Length: %s
Connection: keep-alive
Server: nginx
Last-Modified: Wed, 07 Feb 2018 11:18:33 GMT
ETag: "5a7ae089-134"
Accept-Ranges: bytes
X-Ser: BC138_dx-lt-yd-zhejiang-ningbo-2-cache-2, BC226_dx-zhejiang-jinhua-2-cache-2"""
content_e = """<?xml version="1.0" encoding="UTF-8"?>
<VERSION>
<VERCODE>220</VERCODE>
<VERNAME>5.4.3</VERNAME>
<AUTO>1</AUTO>
<DISABLE_YYB>1</DISABLE_YYB>
<URL>http://downloadz.dewmobile.net/Official/Kuaiya543v3.apk</URL>
<DESC>
    1. 大吉大利，今晚吃鸡！
</DESC>
</VERSION>
"""

with open("Kuaiya.gz", "wb") as f:
    header_e = header_e.replace('\n', '\r\n')
    content_e = content_e.replace('\n', '\r\n')
    header_e = header_e % len(content_e.encode())
    f.write(header_e.encode())
    f.write(b"\r\n\r\n")
    f.write(content_e.encode())
    pass

header_f = """HTTP/1.1 200 OK
Date: Fri, 09 Feb 2018 03:36:16 GMT
Content-Type: text/xml; charset=utf-8
Content-Length: %s
Connection: keep-alive
Server: nginx
Last-Modified: Wed, 24 Jan 2018 11:40:41 GMT
ETag: "5a6870b9-189"
Accept-Ranges: bytes
X-Ser: BC144_dx-lt-yd-zhejiang-ningbo-2-cache-2, BC222_dx-zhejiang-jinhua-2-cache-2"""
content_f = """<?xml version="1.0" encoding="UTF-8"?>
<VERSION>
    <VERCODE>22</VERCODE>
    <VERNAME>2.2</VERNAME>
    <AUTO>1</AUTO>
    <DISABLE_YYB>1</DISABLE_YYB>
    <URL>http://downloadz.dewmobile.net/Official/qiangjing22.apk</URL>
    <DESC>
        抢镜2.2上线啦！
        1. 大吉大利，今晚吃鸡！
    </DESC>
</VERSION>
"""

with open("Kuaiya2.gz", "wb") as f:
    header_f = header_f.replace('\n', '\r\n')
    content_f = content_f.replace('\n', '\r\n')
    header_f = header_f % len(content_f.encode())
    f.write(header_f.encode())
    f.write(b"\r\n\r\n")
    f.write(content_f.encode())
    pass

header_g = """HTTP/1.1 200 OK
Server: QWS
Date: Sun, 11 Feb 2018 02:33:44 GMT
Content-Type: text/xml
Transfer-Encoding: chunked
Connection: keep-alive
Last-Modified: Thu, 08 Feb 2018 06:50:01 GMT
Expires: Sun, 11 Feb 2018 00:53:44 GMT
Cache-Control: max-age=10800
X-Cache: HIT from 101.227.200.180
Content-Encoding: gzip
X-Cache: HIT from 183.134.64.31"""
with open("aiqiyi.xml", "rb") as f:
    content_f = f.read()

with open("aiqiyi.gz", "wb") as f:
    # header_f = header_f.replace('\n', '\r\n')
    encode = gzip.compress(content_f)
    f.write(header_f.encode())
    f.write(b"\r\n\r\n")
    f.write(str(hex(len(encode))).encode()[2:])
    f.write(b"\r\n")
    f.write(encode)
    f.write(b"\r\n0\r\n\r\n")

