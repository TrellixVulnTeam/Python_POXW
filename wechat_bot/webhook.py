#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: webhook.py
@time: 2019/12/30
@author: alfons
"""
import json
import requests
import urllib2
import subprocess
import paramiko
import time

webhook_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7440f764-7b9c-4421-955c-eab3475fb907"


def urllib_post(url, message):
    data = {
        "msgtype": "text",
        "text": {
            "content": message,
            "mentioned_list": ["@all"],
        }
    }

    post_data = json.dumps(data)
    request = urllib2.Request(url, post_data)
    request.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(request)
    result = response.read()
    print result


def request_post(url, message):
    data = {
        "msgtype": "text",
        "text": {
            "content": message,
            "mentioned_list": ["@all"],
        }
    }

    requests.post(url, json=data)


if __name__ == '__main__':

    line_filter = set()

    with open("./webhook_url", 'r') as f:
        webhook_url = f.read()

    # # file_path = "./http.log.log"
    # f = subprocess.Popen('tail -f %s| grep -v -e "10.10.160.*"| grep -v "10.10.100.11"| awk \'{print $1}\'' % file_path, stdout=subprocess.PIPE,
    #                      stderr=subprocess.PIPE, shell=True)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(hostname='10.10.100.11', port=22, username='root', password='cljslrl0620')
    ssh.connect(hostname='192.168.1.70', port=22, username='root', password='cljslrl0620')

    file_path = "/var/log/linstor-controller/rest-access.log"

    while True:
        try:
            stdin, stdout, stderr = ssh.exec_command('tail -100 %s | grep -v -e "10.10.160.*"| grep -v "192.168.1.70"| awk \'{print $1}\'' % file_path)

            line = stdout.readline()

            if not line or line in line_filter:
                continue
            else:
                line_filter.add(line)

            msg = "貌似({l})正在使用 吴亦凡 的环境！！！".format(l=line)

            urllib_post(url=webhook_url, message=msg)
            print msg
        except Exception as e:
            print str(e)
        finally:
            time.sleep(0.7)
