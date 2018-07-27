"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FridaTest.py
 @Time    : 2018/7/20 9:36
"""
import frida

jscode = """
console.log("[*] Starting script");
Java.perform(function () {              // 生成java虚拟机的环境
    Java.enumerateLoadedClasses(
    {
    "onMatch": function(className){
            console.log(className);
        },
    "onComplete":function(){}
    });
});
console.log("[*] Stoping script");
"""


def on_message(message, data):
    try:
        print("[*]message:", message)
        print("[*]data:", data)
    except:
        print("[*]on_message except!")


enumerate_devices = frida.enumerate_devices()  # 获取所有的设备
get_local_device = frida.get_local_device()  # 获取本地设备
get_remote_device = frida.get_remote_device()  # 获取远程设备
device = frida.get_usb_device()  # 获取usb设备

# 启动应用，并返回对应的进程号
# processId = device.spawn("com.tencent.mm")
# session = device.attach(processId)

# 下面两个函数 get_process attach 都需要在设备上启动了程序后，才能获取到进程状态
processInfo = device.get_process("com.tencent.mm")  # 获取微信的进程信息
attachSession = device.attach(processInfo.pid)  # 附着微信的进程，并返回进程的会话
device.resume(processInfo.pid)  # 防止附着后进程失效，重启一下

# script = attachSession.create_script('console.log("[*] Starting script");')
script = attachSession.create_script(jscode)    # 创建一个新的js脚本
script.on("message", on_message)    # 设置 message 回调函数

print('[*] Running CTF')

script.load()       # 加载js脚本运行结果

# device.kill(processInfo.pid)        # 杀死对应的进程，参数可以是进程名称或者进程号

# processList = device.enumerate_processes()
# for process in processList:
#     print(process)

input("Press enter to continue...")  # 此句必须的，防止进程结束而无法展示结果

