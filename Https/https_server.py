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
import BaseHTTPServer
import SimpleHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import ssl

class S(SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


# httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), SimpleHTTPServer.SimpleHTTPRequestHandler)
httpd = BaseHTTPServer.HTTPServer(('192.168.2.40', 4443), S)
httpd.socket = ssl.wrap_socket(httpd.socket, certfile = './server.pem', server_side = True)
httpd.serve_forever()
