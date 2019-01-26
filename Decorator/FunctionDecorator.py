"""
@file: FunctionDecorator.py
@time: 2019/01/25
@author: sch
"""
from functools import wraps


# ---------------------------------斐波那契数列-----------------------
def Memoization(fn):
    cache = dict()

    @wraps(fn)
    def Wrapper(*args):
        result = cache.get(args)

        if result is None:
            result = fn(*args)
            cache[args] = result

        return result

    return Wrapper


@Memoization
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# ---------------------------------html标签----------------------------
def AddHtmlTag(tag, *args, **kwargs):
    def Decorator(fn):
        css_class = "class=\"{}\"".format(kwargs["css_class"]) if "css_class" in kwargs else ""

        def Wrapper(*args):
            print(fn.__name__)
            print(fn(*args))
            return "<{tag} {css}>{fn}</{tag}>".format(tag = tag, css = css_class, fn = fn(*args))

        return Wrapper

    return Decorator


@AddHtmlTag(tag = 'div', css_class = "center")
@AddHtmlTag(tag = 'b', css_class = "black")
def Hello(name):
    return "hello world! " + name


if __name__ == '__main__':
    print(fib(100))
    print(Hello("tmo"))
