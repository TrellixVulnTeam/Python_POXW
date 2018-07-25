"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FridaMode.py
 @Time    : 2018/7/24 14:15
"""

import frida

# 注入的js代码
jscode = """
"""


# message 的回调函数
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] {0}".format(message['payload']))
    else:
        print(message)


session = frida.get_usb_device().attach('app full name')  # 附着的usb设备的对应的程序的进程，返回会话
script = session.create_script(jscode)  # 创建执行的脚本
script.on('message', on_message)  # 回调函数
script.load()  # 加载js脚本执行的结果
input("Press enter to continue...")  # 此句必须的，防止进程结束而无法展示结果
