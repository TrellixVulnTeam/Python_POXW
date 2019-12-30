"""
@file: webhook.py
@time: 2019/12/30
@author: alfons
"""
import requests
import subprocess

with open("./webhook_url", 'r') as f:
    webhook_url = f.read()

f = subprocess.Popen(['tail', '-F', "./http.log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while True:
    line = f.stdout.readline()
    content = requests.post(webhook_url, json={
        "msgtype": "helloworld",
        "text": {
            "content": "hello world",
            "mentioned_list": ["@all"],
        }
    })
pass
