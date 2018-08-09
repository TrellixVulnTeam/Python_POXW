"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : HttpClient.py
 @Time    : 2018/8/7 9:45
"""
import requests

resp = requests.get(url="http://127.0.0.1:5000/ %OD%OAhelloworld%0D%0Amain")
content = resp.content
pass