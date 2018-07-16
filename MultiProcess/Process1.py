"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Process1.py
@time: 18-6-25 下午11:25
@version: v1.0 
"""
with open('xxx', 'w') as f:
    while True:
        data = input('Enter some text:')
        f.seek(0)
        f.write(data)
        f.truncate()
        f.flush()
