"""
@author: Alfons
@contact: alfons_xh@163.com
@file: __slots__.py
@time: 19-1-25 下午9:14
@version: v1.0 
"""
import sys


class Human:
    # __slots__ = ["name"]
    pass


class Employer(Human):
    # __slots__ = ["__dict__", "salary"]
    pass


e = Employer()

e.name = "alfons"
print("name is -> ", e.name)

e.salary = 1000
print("salary is -> ", e.salary)

e.sex = "male"
print("sex is -> ", e.sex)

print("\n\n")

if __name__ == '__main__':
    import sys


    class TestObj:
        # __slots__ = ["age"]

        def __init__(self, age):
            self.age = age

    print(sys.getsizeof(TestObj(12)))

    for length in range(1120, 1122):
        l_list = [TestObj(i) for i in range(length)]
        print("len is -> {l}, sys.getsizeof(l_list) -> {s}".format(s = sys.getsizeof(l_list), l = len(l_list)))       # 计算整个list的大小

        s = sum(sys.getsizeof(l) for l in l_list)       # 统计list中所有元素的大小
        print("len is -> {l}, sys.getsizeof(obj_in_list) -> {s}".format(s = s, l = len(l_list)))
