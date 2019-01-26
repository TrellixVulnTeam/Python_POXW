"""
@file: ClassDecorator.py
@time: 2019/01/25
@author: sch
"""


class MyApp:
    def __init__(self):
        self.__func_map = dict()

    def Register(self, name):
        def Wrapper(fn):
            self.__func_map[name] = fn
            return fn

        return Wrapper

    def Call(self, name):
        func = self.__func_map.get(name, None)
        if func is not None:
            return func()

        raise Exception("No func exist. -> {}".format(name))


app = MyApp()


@app.Register("/")
def man_page():
    return "This is man page."


@app.Register("/sec")
def sec_page():
    return "This is sec page"


if __name__ == '__main__':
    print(app.Call("/"))
    print(app.Call("/sec"))
    # print(app.Call("/third"))
