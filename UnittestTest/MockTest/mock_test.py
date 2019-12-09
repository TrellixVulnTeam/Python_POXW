"""
@file: mock_test.py
@time: 2019/12/3
@author: alfons
"""
from unittest import mock


# ================================基本使用===================================
# mock_obj = mock.Mock(name="Foo")
# print(mock_obj)         # <Mock name='Foo' id='2432161031368'>
# print(mock_obj.method)      # <Mock name='Foo.method' id='2432161067080'>
# print(mock_obj.method())    # <Mock name='Foo.method()' id='2432161089800'>
# print(mock_obj.attr.do_something())     # <Mock name='Foo.attr.do_something()' id='2566035702728'>
# print(mock_obj.mock_calls)  # [call.method(), call.attr.do_something()] 打印所有的mock调用方法情况

# class TestCls:
#     pass
#
#
# test_cls = TestCls()
# test_cls.method = mock.Mock(name="method")  # 猴子补丁
# print(test_cls.method(1, 2, 3))  # <Mock name='method()' id='2871714420232'>


# class TestCls:
#     def method(self):
#         self.do_something(1, 2, 3)
#
#     def do_something(self, a, b, c):
#         print(a, b, c)
#
#
# test_cls = TestCls()
# test_cls.do_something = mock.Mock()
# test_cls.method()
# test_cls.do_something.assert_called_once_with(1, 2)  # do_something的属性called会被设置成True，这里传入参数为 (1,2)，没有被调用，会抛出异常


# class TestCls:
#     def method(self, do_something):
#         do_something.close(1, 2, 3)     # 2 此处如果传入的是mock对象，则会使用mock对象自动生成的close方法进行调用
#
#
# test_cls = TestCls()
# mock = mock.Mock()      # 1 mock对象当作对象传入
# test_cls.method(mock)
# mock.close.assert_called_with(1, 2, 3)      # 3 此处由于调用了mock.close，所以断言会通过


class TestCls:
    def do_something(self, a):
        print("hello", a)


mock_obj = mock.Mock(spec=TestCls)
print(mock_obj.do_something("alfons"))   # <Mock name='mock.do_something()' id='2137460940360'>
# print(mock_obj.method())        # AttributeError: Mock object has no attribute 'method'       # spec标准模板中，没有method方法

# ===================模拟返回===================
# mock_obj = mock.Mock()
# mock_cursor = mock_obj.connection.cursor.return_value.execute.return_value = ["Foo"]
#
# print(mock_obj.connection.cursor().execute("select * from ASM_INFO"))
# print(mock_obj.mock_calls)  # [call.connection.cursor(), call.connection.cursor().execute('select * from ASM_INFO')]


# ===================patch使用==================
# class Foo:
#     def method(self):
#         return "hello"
#
#
# def do_something():
#     instance = Foo()
#     return instance.method()
#
#
# with mock.patch("__main__.Foo") as mock:  # 将Foo类模拟成mock类
#     mock.return_value.method.return_value = "mock return"  # mock.return_value实际等于 Foo() 返回的实例，method.return_value实际等于 method()，此处将method方法调用后返回的结果设置为 "mock return"
#     result = do_something()
#     assert result == "mock return"  # 上面已经将返回的结果设置成了 "mock return"，所以断言通过
