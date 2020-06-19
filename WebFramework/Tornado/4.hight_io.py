"""
@file: 4.hight_io.py
@time: 2019/8/29
@author: alfons
"""
import json
import time
import threading

from functools import wraps

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options

from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from tornado.options import define
from tornado.options import options
from tornado.web import URLSpec as U
from tornado.web import Finish

define("port", default=8000, help="run on the given port", type=int)
define("debug", default=True, help="start debug mode", type=bool)
SLEEP_TIME = 1
COOKIE_SECRET = "seekplum"


def time_of_use(func):
    """统计函数使用时间
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        use_time = end_time - start_time
        print("=" * 100)
        print("%s use time: %fs" % (func.__name__, use_time))
        print("=" * 100)
        return result

    return decorator


def _get_node_ids(cluster_id):
    """查询集群中节点id列表

    :param cluster_id 集群id
    :type cluster_id int
    :example cluster_id 1

    :return 节点id集合
    :rtype list
    :example [1, 2, 3, 4]
    """
    return [1, 2, 3, 4]


def _get_switch_ids(cluster_id):
    """查询集群中交换机id列表

    :param cluster_id 集群id
    :type cluster_id int
    :example cluster_id 1

    :return 交换机id集合
    :rtype list
    :example [1, 2, 3, 4]
    """
    return [1, 2, 3, 4]


def _get_node_info_sleep_with_time(nodes_id):
    """查询节点信息

    :param nodes_id 集群id集合
    :type nodes_id iter
    :example nodes_id [1, 2, 3, 4]

    :rtype list
    :return 节点详细信息
    """
    data = []
    for node_id in nodes_id:
        time.sleep(SLEEP_TIME)
        node_info = {
            "node_id": node_id
        }
        data.append(node_info)
    return data


def _get_switch_info_sleep_with_time(switches_id):
    """查询交换机信息

    :param switches_id id集合
    :type switches_id iter
    :example switches_id [1, 2, 3, 4]

    :rtype list
    :return 交换机详细信息
    """
    data = []
    for switch_id in switches_id:
        time.sleep(SLEEP_TIME)
        switch_info = {
            "switch_id": switch_id
        }
        data.append(switch_info)
    return data


def _get_node_info_sleep_with_gen(nodes_id):
    """查询节点信息

    :param nodes_id 集群id集合
    :type nodes_id iter
    :example nodes_id [1, 2, 3, 4]

    :rtype list
    :return 节点详细信息
    """
    data = []
    for node_id in nodes_id:
        yield from gen.sleep(SLEEP_TIME)
        node_info = {
            "node_id": node_id
        }
        data.append(node_info)
    return data


def _get_switch_info_sleep_with_gen(switches_id):
    """查询交换机信息

    :param switches_id id集合
    :type switches_id iter
    :example switches_id [1, 2, 3, 4]

    :rtype list
    :return 交换机详细信息
    """
    data = []
    for switch_id in switches_id:
        yield from gen.sleep(SLEEP_TIME)
        switch_info = {
            "switch_id": switch_id
        }
        data.append(switch_info)
    return data


# @time_of_use
def get_cluster_info1(clusters_id):
    """查询集群id

    :param clusters_id 集群id集合
    :type clusters_id iter
    :example clusters_id [1, 2, 3, 4]

    :rtype list
    :return 集群详细信息
    """

    def _get_cluster_info1():
        nodes_id = _get_node_ids(cluster_id)
        switches_id = _get_switch_ids(cluster_id)

        node_info = _get_node_info_sleep_with_time(nodes_id)
        switch_info = _get_switch_info_sleep_with_time(switches_id)

        cluster_info = {
            "cluster_id": cluster_id,
            "nodes": node_info,
            "switches": switch_info
        }
        data.append(cluster_info)

    data = []
    thread_list = []
    for cluster_id in clusters_id:
        thread = threading.Thread(target=_get_cluster_info1)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    return data


def get_cluster_info2(clusters_id):
    """查询集群id

    :param clusters_id 集群id集合
    :type clusters_id iter
    :example clusters_id [1, 2, 3, 4]

    :rtype list
    :return 集群详细信息
    """

    def _get_cluster_info2():
        nodes_id = _get_node_ids(cluster_id)
        switches_id = _get_switch_ids(cluster_id)

        node_info = yield from _get_node_info_sleep_with_gen(nodes_id)
        switch_info = yield from _get_switch_info_sleep_with_gen(switches_id)

        cluster_info = {
            "cluster_id": cluster_id,
            "nodes": node_info,
            "switches": switch_info
        }
        data.append(cluster_info)

    data = []
    for cluster_id in clusters_id:
        yield from _get_cluster_info2()
    return data


class BaseRequestHandler(tornado.web.RequestHandler):
    """Base RequestHandler"""

    # thread pool executor
    executor = ThreadPoolExecutor(10)

    def write_json(self, data):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data, indent=4))

    def success_response(self, data=None, message="", finish=True):
        response = {
            "error_code": 0,
            "message": message,
            "data": data
        }
        self.write_json(response)
        if finish:
            raise Finish

    def error_response(self, error_code, message="", data=None, status_code=202, finish=True):
        self.set_status(status_code)
        response = {
            "error_code": error_code,
            "data": data,
            "message": message,
        }
        self.write_json(response)
        if finish:
            raise Finish

    def options(self, *args, **kwargs):
        """
        避免前端跨域options请求报错
        """
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "POST, GET, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers",
                        "CONTENT-TYPE, Access-Control-Allow-Origin, cache-control, Cache-Control, x-access-token")
        self.set_header("Access-Control-Expose-Headers", "X-Resource-Count")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "POST, GET, PUT, DELETE, OPTIONS")
        self.set_header("Access-Control-Max-Age", 1000)
        self.set_header("Access-Control-Allow-Headers",
                        "CONTENT-TYPE, Access-Control-Allow-Origin, cache-control, Cache-Control, x-access-token")
        self.set_header("Access-Control-Expose-Headers", "X-Resource-Count")


class TestHandler(BaseRequestHandler):
    """测试使用的handler
    """

    @run_on_executor
    def _get_cluster_info1(self):
        clusters_id = [1, 2, 3, 4]
        result = get_cluster_info1(clusters_id)
        return result

    def _get_cluster_info2(self):
        clusters_id = [1, 2, 3, 4]
        result = yield from get_cluster_info2(clusters_id)
        return result

    @gen.coroutine
    def get(self):
        #data = yield self._get_cluster_info1()        # thread
        data = yield from self._get_cluster_info2()  # no thread
        self.success_response(data)


class TestHandler2(BaseRequestHandler):
    """测试使用的handler
    """

    @run_on_executor
    def get(self):
        print(self.executor)
        for i in range(20 ** 20):
            pass
        self.write("Hello world, TestHandler2")


class TestHandler3(BaseRequestHandler):
    """测试使用的handler
    """

    @gen.coroutine
    def get(self):
        print(self.executor)
        self.write("Hello world, TestHandler3")


# 相关API
handlers = [
    U(r"/test", TestHandler),
    U(r"/test2", TestHandler2),
    U(r"/test3", TestHandler3),
]


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = dict(
            cookie_secret=COOKIE_SECRET,
            debug=options.debug
        )

        super(Application, self).__init__(handlers, **app_settings)


def main():
    """tornado入口函数
    """
    tornado.options.parse_command_line()
    app = Application()

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("Server start on port %s" % options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
