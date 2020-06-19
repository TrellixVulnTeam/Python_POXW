"""
@file: AsyncioSocket.py
@time: 2018/12/25
@author: sch
"""
import ntplib
import time
import datetime
import socket


def ntp_request(host, version = 2, port = 'ntp', timeout = 5):
    """Query a NTP server.

    Parameters:
    host    -- server name/address
    version -- NTP version to use
    port    -- server port
    timeout -- timeout on socket operations

    Returns:
    NTPStats object
    """
    # lookup server address
    addrinfo = socket.getaddrinfo(host, port)[0]
    family, sockaddr = addrinfo[0], addrinfo[4]

    # create the socket
    s = socket.socket(family, socket.SOCK_DGRAM)

    try:
        s.settimeout(timeout)

        # create the request packet - mode 3 is client
        # query_packet = ntplib.NTPPacket(mode = 3, version = version,
        #                          tx_timestamp = system_to_ntp_time(time.time()))

        # send the request
        # s.sendto(query_packet.to_data(), sockaddr)
        s.sendto(b"hello", sockaddr)

        # wait for the response - check the source address
        src_addr = None,
        while src_addr[0] != sockaddr[0]:
            response_packet, src_addr = s.recvfrom(256)

        # build the destination timestamp
        dest_timestamp = ntplib.system_to_ntp_time(time.time())
    except socket.timeout:
        raise Exception("No response received from %s." % host)
    finally:
        s.close()

    # construct corresponding statistics
    stats = ntplib.NTPStats()
    stats.from_data(response_packet)
    stats.dest_timestamp = dest_timestamp

    return stats


dst_ip = "130.105.186.16"
dst_port = 29591



# client = ntplib.NTPClient()
# res = datetime.datetime.fromtimestamp(client.request(dst_ip).tx_time)

res = datetime.datetime.fromtimestamp(ntp_request(host = dst_ip, port = dst_port))

print(res)
