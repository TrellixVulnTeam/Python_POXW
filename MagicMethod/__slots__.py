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


    l_list = [TestObj(i) for i in range(2 ** 20)]

    print("sys.getsizeof(l_list) -> ", sys.getsizeof(l_list))

    s = sum(sys.getsizeof(l) for l in l_list)

    print("sys.getsizeof(obj_in_list)", s)
