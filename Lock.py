"""
@file: Lock.py
@time: 2020/4/2
@author: alfons
"""
import os
import time
from threading import Lock
import os
import fcntl


class LockUseFile:
    filename = "/root/.rebalance.lock"

    def __init__(self):
        self.handle = open(self.filename, 'w')

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

    def acquire(self):
        fcntl.flock(self.handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.flock(self.handle, fcntl.LOCK_UN)

    def __del__(self):
        self.handle.close()


#
# class my_lock(Lock):
#
#     def __init__(self):
#         super(my_lock, self).__init__()
#         self.lock_file = "./rebalance.lock"
#
#     def release(self) -> None:
#
#         if self.lock:
#             os.remove(self.lock_file)
#
#     def locked(self) -> bool:
#         if os.path.exists(self.lock_file):
#             return False
#         else:
#             with open(self.lock_file, 'w') as f:
#                 f.write("1")
#             self.lock = True
#             return True


# class my_lock:
#     lock_file = "./rebalance.lock"
#
#     def __init__(self):
#         self.lock = False
#
#     def __enter__(self):
#         if os.path.exists(self.lock_file):
#             return False
#         else:
#             with open(self.lock_file, 'w') as f:
#                 f.write("1")
#             self.lock = True
#             return True
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self.lock:
#             os.remove(self.lock_file)


def func_a(name):
    with my_lock():
        print("{}: i'm used\n".format(name))
        time.sleep(5)
    time.sleep(1)
    print("{}: i'm out\n".format(name))


if __name__ == '__main__':
    from multiprocessing.pool import ThreadPool

    t_pool = ThreadPool(10)
    res = t_pool.map_async(func_a, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(res.get())

    func_a("hello")
