"""
@author: Alfons
@contact: alfons_xh@163.com
@file: 2-1.assert.py
@time: 2019/8/10 上午11:07
@version: v1.0 
"""

try:
    # a = True
    a = False

    assert a, ValueError("value error")
    # assert a

except Exception as e:
    print(str(e))