"""
@file: DNSParserTest.py
@time: 2018/12/17
@author: sch
"""
import dns
import socket
import struct
from dns import resolver


def IPInt2Str(ipInt):
    return socket.inet_ntoa(struct.pack('I', socket.htonl(ipInt)))


server = IPInt2Str(3703406444)
# server = "114.114.114.114"
port = 53

dns_query = dns.message.make_query("www.baidu.com", "A")
response = dns.query.udp(dns_query, server, timeout = 60, port = port)

for i in response.answer:
    print(i.to_text())
