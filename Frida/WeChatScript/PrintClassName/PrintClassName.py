"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : PrintClassName.py
 @Time    : 2018/7/25 17:01
"""
import frida
import json


def MessageHandle(message, payload):
    if message["type"] == "error":
        print("[*]Message: ")
        for key, value in message.items():
            print(key, ":", value)
    elif message["type"] == "send":
        classname = json.loads(message["payload"])["classname"]
        if "tencent" in classname:
            print("[*]", classname)
    else:
        print("[*]Message: ", message)
        print("[*]Payload: ", payload)


device = frida.get_usb_device()
pid = device.spawn("com.tencent.mm")
session = device.attach(pid)
device.resume(pid)

with open("PrintClassName.js", "r", encoding="utf-8") as f:
    script = session.create_script(f.read())

script.on("message", MessageHandle)  # 添加返回错误的回调显示函数
script.load()

input("Press enter to continue...")
