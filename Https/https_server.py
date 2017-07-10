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

import os
import BaseHTTPServer
import SimpleHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl
import json

res_dict_1 = {"changeAp": "0"}
res_dict_2 = {"changeAp": "1", "ssid": "wifimima:henhen1234567", "pt": "OPN", "p": ""}


class S(SimpleHTTPRequestHandler):
    RecvData = ""
    RecvNum = 0

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()

        if self.requestline == "POST /feadbackJson/ HTTP/1.1":
            print "feedbackJson:-------"
            length = int(self.headers.getheader('content-length'))
            data = json.loads(self.rfile.read(length))
            data2 = json.dumps(data, ensure_ascii = False)
            print data2
            self.wfile.write("OK")
        elif self.requestline == "POST /deviceStatus/ HTTP/1.1":
            print "-------------deviceStatus:-------"
            length = int(self.headers.getheader('content-length'))
            data = json.loads(self.rfile.read(length))
            data2 = json.dumps(data, ensure_ascii = False)
            print data2
            # self.wfile.write(json.dumps(res_dict_1))
            self.wfile.write(json.dumps(res_dict_1))
        elif "POST /feadbackEntity&DeviceID=" in self.requestline:
            length = int(self.headers.getheader('content-length'))
            data = self.rfile.read(length)
            path = "C:/Users/shangchenhui/Desktop/TransferData/"\
                   + self.requestline[self.requestline.find("filePath=")+len("filePath="):self.requestline.find(" HTTP/1.1")]
            dir_path = path[:path.rfind('/')]
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)
            with open(path, "wb") as f:
                f.write(data)
            self.wfile.write("OK")
        else:
            self.wfile.write("empty data!")


# str_test = "hello"
# str_1 = str_test.read(3)
# str_2 = str_test[3:]
# print str_1
# print str_2

# httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)

httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), S)
# httpd.socket = ssl.wrap_socket(httpd.socket, certfile = './server.pem', server_side = True)
httpd.serve_forever()
