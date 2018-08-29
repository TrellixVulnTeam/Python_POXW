"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FindImportClass.py
 @Time    : 2018/8/28 14:08
"""
import os

PROJECT_PATH = "D:\downloads\\apps\Decompile\点心桌面"
TARGET_CLASS = b"com.lody.virtual.client.hook.proxies.pm.MethodProxies"
TARGET_FUNCTION = b"getMethodName"


def FindTargetFunction(file_path):
    with open(file_path, "rb") as f:
        codes = f.read()

    if TARGET_CLASS not in codes:
        return

    if TARGET_FUNCTION in codes:
        print("Target function {func} in {file}.".format(func=TARGET_FUNCTION.decode(), file=file_path))


def Analysis(target_dir):
    file_list = [os.path.join(target_dir, base_name) for base_name in os.listdir(target_dir)]
    for file in file_list:
        if os.path.isdir(file):
            Analysis(file)

        if os.path.isfile(file) and os.path.basename(file).endswith(".java"):
            FindTargetFunction(file)


Analysis(PROJECT_PATH)
