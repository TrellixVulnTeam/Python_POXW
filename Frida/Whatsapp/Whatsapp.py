"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Whatsapp.py
 @Time    : 2018/12/28 15:45
"""
import frida
import time
import os
import threading
import traceback
from queue import Queue

message_queue = Queue()
host_file = "./host.txt"


def on_message(message, data):
    if message["type"] == "error":
        print("[*]Message: ")
        for key, value in message.items():
            print(key, ":", value)
    elif message["type"] == "send":
        message_queue.put(message["payload"])
        print("[*] Receive message: ", message["payload"])
    else:
        print("[*]Message: ", message)
        print("[*]Payload: ", data)


def demo_for_message_parse():
    """
    信息接收守护进程
    :return:
    """
    server_cache = list()
    if os.path.isfile(host_file):
        with open(host_file, "r") as f:
            server_cache = [server for server in f.readlines() if server]

    while True:
        try:
            message = message_queue.get()
            message_list = message.split('|')
            server = "{ip}:{port}\n".format(ip=message_list[0], port=message_list[1])

            if server in server_cache:
                continue

            with open(host_file, "a") as f:
                f.write(server)
        except:
            print("[*] Something error when receive message.")
            traceback.print_exc()


if __name__ == '__main__':
    receive_thread = threading.Thread(target=demo_for_message_parse, name="Demo for receive.")
    receive_thread.start()

    device = frida.get_usb_device()  # 获取usb设备

    processId = device.spawn("com.whatsapp")  # 重启应用，返回进程ID
    device.resume(processId)  # 防止附着后进程失效，重启一下
    time.sleep(1)
    attachSession = device.attach(processId)  # 附着微信的进程，并返回进程的会话
    # attachSession = device.attach("com.tencent.mm")  # 附着微信的进程，并返回进程的会话

    with open(os.listdir("./")[0], "r", encoding="utf-8") as f:
        jscode = f.read()
    script = attachSession.create_script(jscode)  # 创建一个新的js脚本
    script.on("message", on_message)  # 设置 message 回调函数

    print('[*] Running CTF')

    script.load()  # 加载js脚本运行结果

    input("Press enter to continue...\n")  # 此句必须的，防止进程结束而无法展示结果
