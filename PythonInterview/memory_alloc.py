"""
@author: Alfons
@contact: alfons_xh@163.com
@file: memory_alloc.py
@time: 2019/4/5 下午4:30
@version: v1.0 
"""
# id() 函数返回的为 等号右边的 对象的地址
# 下面会为list_a 分配新的对象地址
list_a = list((1, 2, 3))
print("id of list_a: ", id(list_a))
list_a = list((4, 5, 6))
print("id of list_a: ", id(list_a))

# 每次创建变量，解释器会为对象 申请新的内存空间
list_b = list((1, 2, 3))
list_c = list((1, 2, 3))
print("id(list_b) -> {}, id(list_c) -> {}".format(id(list_b), id(list_c)))

# 对于小的int类型或者字符类型的对象，有固定的内存空间
int_a = 255.0 * 1
int_b = 255.0 * 1
print("id(int_a) -> {}, id(int_b) -> {}".format(id(int_a), id(int_b)))
chr_a = '这只是测试代码'
chr_b = '这只是测试代码'
print("id(chr_a) -> {}, id(chr_b) -> {}, {}".format(id(chr_a), id(chr_b), id(chr_a) == id(chr_b)))
chr_c = '这只是测试代码. ' * 5
chr_d = '这只是测试代码. ' * 5
print("id(chr_c) -> {}, id(chr_d) -> {}, {}".format(id(chr_c), id(chr_d), id(chr_c) == id(chr_d)))

big_int_a = 55 * 1
big_int_b = 55 * 1
print("id(big_int_a) -> {}, id(big_int_b) -> {}".format(id(big_int_a), id(big_int_b)))


def func():
    int_c = 257
    float_c = 2.0
    str_c = "hellolllllllllllll#llllllllllllllllllllllllllllll"
    list_c = [1, 2, 3, 4]
    tuple_c = tuple((1, 2, 3, 4))
    dict_c = {'a': 1}
    set_c = {1, 2}
    print(id(int_c), id(float_c), id(str_c), id(list_c), id(tuple_c), id(dict_c), id(set_c))


print("\nid(int_c), id(float_c), id(str_c), id(list_c), id(tuple_c), id(dict_c), id(set_c)")
func()

int_d = 257
float_d = 2.0
str_d = "hellolllllllllllll#llllllllllllllllllllllllllllll"
list_d = [1, 2, 3, 4]
tuple_d = tuple((1, 2, 3, 4))
dict_d = {'a': 1}
set_d = {1, 2}
print(id(int_d), id(float_d), id(str_d), id(list_d), id(tuple_d), id(dict_d), id(set_d))

int_e = 257
float_e = 2.0
str_e = "hellolllllllllllll#llllllllllllllllllllllllllllll"
list_e = [1, 2, 3, 4]
tuple_e = tuple((1, 2, 3, 4))
dict_e = {'a': 1}
set_e = {1, 2}
print(id(int_e), id(float_e), id(str_e), id(list_e), id(tuple_e), id(dict_e), id(set_e))

tuple_f = (list_e, 123)
tuple_g = tuple_f + (1, 2)
print(id(tuple_f), id(tuple_g), tuple_f == tuple_g)
tuple_f[0].append(1)
print(tuple_f)
print(tuple_g)
print(id(tuple_f), id(tuple_g), tuple_f == tuple_g)
