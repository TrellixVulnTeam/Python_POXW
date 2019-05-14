"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Wandoujia.py.py
 @Time    : 2018/8/22 16:05
"""
import frida
import time
import os


def on_message(message, data):
    if message["type"] == "error":
        print("[*]Message: ")
        for key, value in message.items():
            print(key, ":", value)
    elif message["type"] == "send":
        print("[*]", message["payload"])
    else:
        print("[*]Message: ", message)
        print("[*]Payload: ", data)


device = frida.get_usb_device()  # 获取usb设备

processId = device.spawn("com.wandoujia.phoenix2")  # 重启应用，返回进程ID
device.resume(processId)  # 防止附着后进程失效，重启一下
time.sleep(3)
attachSession = device.attach(processId)  # 附着微信的进程，并返回进程的会话
# attachSession = device.attach("com.tencent.mm")  # 附着微信的进程，并返回进程的会话

with open(os.listdir("./")[0], "r", encoding="utf-8") as f:
    jscode = f.read()
script = attachSession.create_script(jscode)  # 创建一个新的js脚本
script.on("message", on_message)  # 设置 message 回调函数

print('[*] Running CTF')

script.load()  # 加载js脚本运行结果

input("Press enter to continue...\n")  # 此句必须的，防止进程结束而无法展示结果
