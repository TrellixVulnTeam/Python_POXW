"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : DistributedClient.py
 @Time    : 2018/6/26 10:18
"""
import time, sys, queue
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


if __name__ == "__main__":
    QueueManager.register("get_task_queue")
    QueueManager.register("get_result_queue")

    server_addr = "192.168.2.53"
    print('Connect to server %s...' % server_addr)

    manager = QueueManager(address=(server_addr, 5000), authkey=b"chick")

    manager.connect()

    task = manager.get_task_queue()
    result = manager.get_result_queue()

    while not task.empty():
        try:
            n = task.get(timeout=1)
            print('run task %d * %d...' % (n, n))
            r = '%d * %d = %d' % (n, n, n * n)
            result.put(r)
            time.sleep(5)
        except queue.Empty:
            print('task queue is empty.')
    # 处理结束:
    print('worker exit.')
