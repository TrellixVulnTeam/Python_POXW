"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : NumpyTest.py
 @Time    : 2019/1/7 11:21
"""
import numpy as np

array = np.array([1, 2, 3, 4, 5])

print("array -> \n", array)
print("array.ndim -> ", array.ndim)
print("array.shape -> ", array.shape)
print("array.size -> ", array.size)
print("array.dtype -> ", array.dtype)

array = np.array([[1, 2, 3],
                  [4, 5, 6]],
                 dtype=np.int)

print("\narray -> \n", array)
print("array.ndim -> ", array.ndim)
print("array.shape -> ", array.shape)
print("array.size -> ", array.size)
print("array.dtype -> ", array.dtype)

print("np.zeros((3, 4)) -> \n", np.zeros((3, 4)))
print("np.ones((3, 4)) -> \n", np.ones((3, 4)))
print("np.arange(12).reshape(3, 4) -> \n", np.arange(12).reshape(3, 4))
print("np.linspace(1, 10, 20) -> \n", np.linspace(1, 10, 20))

a = np.arange(12).reshape(3, 4)
b = np.arange(12).reshape(4, 3)

print("a -> \n", a)
print("b -> \n", b)
print("np.matmul(a, b) -> \n", np.matmul(a, b))
print("np.matmul(b, a) -> \n", np.matmul(b, a))
print("a * a -> ", a * a)
