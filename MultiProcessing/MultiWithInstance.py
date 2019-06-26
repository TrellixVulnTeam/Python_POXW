"""
@author: Alfons
@contact: alfons_xh@163.com
@file: MultiWithInstance.py
@time: 2019/6/26 下午9:24
@version: v1.0 
"""
import multiprocessing


# class SingleCls:
#     def __init__(self):
#         self.__info_list = list()
#         # self.__info_list = multiprocessing.Manager().list()
#
#     def AddMessage(self, message):
#         self.__info_list.append("Hello %s" % message)
#
#     def __repr__(self):
#         return str(self.__info_list)

class SingleCls:
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(SingleCls, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.__info_list = list()

    def AddMessage(self, message):
        self.__info_list.append("Hello %s" % message)

    def __repr__(self):
        return str(self.__info_list)


single_obj = SingleCls()


def func(m):
    single_obj.AddMessage(m)
    print("single_obj {m} -> ".format(m=m), single_obj)


func("1")
func("2")
func("3")
pool = multiprocessing.Pool(4)
pool.apply(func, args=("First",))
pool.apply(func, args=("Second",))
pool.apply(func, args=("Third",))
# pool.apply(single_obj.AddMessage, args=("First",))
# pool.apply(single_obj.AddMessage, args=("Second",))
# pool.apply(single_obj.AddMessage, args=("Third",))
pool.close()
pool.join()

print(single_obj)
