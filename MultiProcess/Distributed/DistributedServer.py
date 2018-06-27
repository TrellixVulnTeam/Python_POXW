"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : DistributedServer.py
 @Time    : 2018/6/26 10:17
"""
import random, time, queue
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()


class QueueManager(BaseManager):
    pass


def get_task_queue():
    global task_queue
    return task_queue


def get_result_queue():
    global result_queue
    return result_queue


if __name__ == "__main__":
    QueueManager.register("get_task_queue", callable=get_task_queue)
    QueueManager.register("get_result_queue", callable=get_result_queue)

    manager = QueueManager(address=("192.168.2.53", 5000), authkey=b"chick")

    manager.start()

    task = manager.get_task_queue()
    result = manager.get_result_queue()

    for i in range(10):
        n = random.randint(1, 1000)
        print("Add new task:", n)
        task.put(n)

    print("Try get results........")
    for i in range(10):
        r = result.get(timeout=100)
        print("Result is ", r)

    time.sleep(10)
    manager.shutdown()
    print("Manager exit.")
