"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : HookLauncherUI.py
 @Time    : 2018/7/25 17:26
"""
import frida


def MessageHandle(message, payload):
    if message["type"] == "error":
        print("[*]Message: ")
        for key, value in message.items():
            print(key, ":", value)
    elif message["type"] == "send":
        print("[*]", message["payload"])
    else:
        print("[*]Message: ", message)
        print("[*]Payload: ", payload)


device = frida.get_usb_device()
pid = device.spawn("com.tencent.mm")  # 重新启动应用
session = device.attach(pid)  # 附着的usb设备的对应的程序的进程，返回会话
device.resume(pid)

# session = device.attach("com.tencent.mm")

with open("HookLauncherUI.js", "r", encoding="utf-8") as f:
    script = session.create_script(f.read())  # 创建执行的脚本

script.on("message", MessageHandle)  # 添加返回错误的回调显示函数
script.load()  # 加载js脚本执行的结果

input("Press enter to continue...\n")
