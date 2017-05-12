#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: https_server.py 
@time: 2017/5/10 11:03 
@version: v1.0 
"""
"""heldsldf"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import BaseHTTPServer
import SimpleHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl
import json

class S(SimpleHTTPRequestHandler):
    RecvData = ""
    RecvNum = 0
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        length = int(self.headers.getheader('content-length'))
        data = json.loads(self.rfile.read(length))
        datalen = len(data)
        data2 = json.dumps(data, ensure_ascii = False)
        data2len = len(data2)
        if length:
            self.wfile.write("success!")
        else:
            self.wfile.write("empty data!")


# str_test = "hello"
# str_1 = str_test.read(3)
# str_2 = str_test[3:]
# print str_1
# print str_2

# httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)

httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), S)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile = './server.pem', server_side = True)
httpd.serve_forever()
