"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : assert——test.py
 @Time    : 2019/5/7 15:49
"""
func_dict = dict()


def Decorate(func_name):
    def Wrapper(f):
        func_dict.update({func_name: f})
        return f

    return Wrapper


@Decorate('A')
def FuncA():
    print("Func A")


@Decorate('B')
def FuncB():
    print("Func B")


if __name__ == '__main__':
    a_func = func_dict['A']
    a_func()

    b_func = func_dict['B']
    b_func()
