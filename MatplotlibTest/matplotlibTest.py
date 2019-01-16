"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : matplotlibTest.py
 @Time    : 2019/1/14 11:48
"""
import numpy as np
from matplotlib import (
    pyplot as plt
)

x = np.arange(0, 5, 0.01)
y = np.sin(x)
plt.plot(x, y)
plt.show()
