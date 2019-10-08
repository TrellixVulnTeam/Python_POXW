"""
@author: Alfons
@contact: alfons_xh@163.com
@file: 2-3.context.py
@time: 2019/8/11 上午10:04
@version: v1.0 
"""


class ManageFile:
    def __init__(self, name, way):
        self.name = name
        self.way = way

    def __enter__(self):
        print("In __enter__, name is {n}, way is {w}".format(n=self.name, w=self.way))
        self.file = open(self.name, self.way)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("In __exit__")
        if self.file:
            self.file.close()


with ManageFile("1.txt", "w") as f:
    f.write("hello")
    f.write("world")

with ManageFile("1.txt", "r") as f:
    print(f.read())


class Indenter:
    def __init__(self):
        self.level = 0

    def __enter__(self):
        self.level += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.level -= 1

    def print(self, text):
        print("\t" * self.level + text)


with Indenter() as indent:
    indent.print("hi")
    with indent:
        indent.print("Alfons")
        with indent:
            indent.print("Welcome")
    indent.print("Good Bye")
