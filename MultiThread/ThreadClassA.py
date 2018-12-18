"""
@author: Alfons
@contact: alfons_xh@163.com
@file: ThreadClassA.py 
@time: 17-6-14 下午5:23 
@version: v1.0 
"""
from threading import Thread


class myThreadA(Thread):
    all_Thread = []

    def __init__(self, name, param):
        Thread.__init__(self, name = name)
        self.__param = param
        self.isRunning = True
        myThreadA.all_Thread.append(self)
        # myThreadA.all_Thread.append(self)

    def run(self):
        FuncA(self.name, self.__param)

    def stop(self):
        self.isRunning = False


def FuncA(name, param):
    for thread in myThreadA.all_Thread:
        if thread.name == name:
            print(name)
            thread.stop()
            myThreadA.all_Thread.remove(thread)


if __name__ == "__main__":
    SER = "yes" if 5 > 22 else "no"
    pass
    para = 1
    thread_1 = myThreadA("First1 thread", para)
    thread_1.start()
