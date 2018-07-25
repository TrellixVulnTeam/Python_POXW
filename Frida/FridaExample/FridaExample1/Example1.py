"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : Example1.py
 @Time    : 2018/7/24 15:30
"""
import frida

device = frida.get_usb_device()
pid = device.spawn("com.example.a11x256.frida_test")
session = device.attach(pid)
device.resume(pid)          # 附着完了之后，有可能进程会停止工作，需要重新开启一下

with open("Example1.js", "r") as f:
    script = session.create_script(f.read())

script.load()

input("Press enter to continue...")
