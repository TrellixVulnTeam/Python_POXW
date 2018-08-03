"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FridaTest.py
 @Time    : 2018/7/20 9:36
"""
import frida
import time


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


enumerate_devices = frida.enumerate_devices()  # 获取所有的设备
get_local_device = frida.get_local_device()  # 获取本地设备
get_remote_device = frida.get_remote_device()  # 获取远程设备
device = frida.get_usb_device()  # 获取usb设备

# device_manager = frida.get_device_manager()  # 获取设备管理员
# device_list = device_manager.enumerate_devices()  # 从设备管理员处拿到所有设备的列表
# device_a = device_manager.add_remote_device("127.0.0.1")  #
# device_manager.remove_remote_device("127.0.0.1")
# device_b = device_manager.get_device("ZX1G222TZL")

# processInfo = device.get_process("com.tencent.mm")  # 获取微信的进程信息

# 下面两个函数 get_process attach 都需要在设备上启动了程序后，才能获取到进程状态
processId = device.spawn("com.tencent.mm")  # 重启应用，返回进程ID
device.resume(processId)  # 防止附着后进程失效，重启一下
time.sleep(5)
attachSession = device.attach(processId)  # 附着微信的进程，并返回进程的会话
# attachSession = device.attach("com.tencent.mm")  # 附着微信的进程，并返回进程的会话

# script = attachSession.create_script('console.log("[*] Starting script");')
with open("FridaAPIMode.js", "r", encoding="utf-8") as f:
    jscode = f.read()
script = attachSession.create_script(jscode)  # 创建一个新的js脚本
script.on("message", on_message)  # 设置 message 回调函数

print('[*] Running CTF')

script.load()  # 加载js脚本运行结果

# device.kill(processInfo.pid)        # 杀死对应的进程，参数可以是进程名称或者进程号

# processList = device.enumerate_processes()
# for process in processList:
#     print(process)

input("Press enter to continue...\n")  # 此句必须的，防止进程结束而无法展示结果
