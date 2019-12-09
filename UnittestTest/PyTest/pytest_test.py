"""
@file: PyTest.py
@time: 2019/11/25
@author: alfons
"""
from unittest.mock import patch, MagicMock, Mock

mock = Mock()
print(mock())
values = dict(a=1, b=2, c=3)


def side_effect(arg):
    return values[arg]


# mock.side_effect = side_effect
mock.return_value = "finish"
print(mock())
print(mock('a'), mock('b'), mock('c'))

mock.side_effect = [1, 23, 4]
print(mock(), mock(), mock())  # 如果side_effect是可迭代对象，则mock()会调用next()方法


class ClassName1:
    pass


class ClassName2:
    pass


@patch('__main__.ClassName2')
@patch('__main__.ClassName1')
def test(MockClass1, MockClass2):
    MockClass1.return_value = "fils"
    print(ClassName1())
    ClassName2()
    assert MockClass1 is ClassName1
    assert MockClass2 is ClassName2
    assert MockClass1.called
    assert MockClass2.called
    print(MockClass1.call_count)


class Foo:
    def method(self):
        return "hello"


def some_function():
    instance = Foo()
    return instance.method()


with patch('__main__.Foo') as mock:
    instance = mock.return_value.method.return_value = 'the result'
    result = some_function()
    assert result == 'the result'
