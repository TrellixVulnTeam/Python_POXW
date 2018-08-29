"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : FindAppList.py
 @Time    : 2018/8/27 9:33
"""
import os
import re
import threading
import time
import traceback
from subprocess import call, PIPE

APK_DIR = "D:\downloads\\apps"
JADX_PATH = "E:\APK反汇编\工具\jadx-0.6.1\\bin\\jadx.bat"
JADX_CMD = "{jadx} -d {dst_dir} -r --export-gradle --show-bad-code {apk_path}"
DECOMPILE_DIR = "D:\downloads\\apps\\Decompile"
MANUAL_WORK_DIR = "D:\downloads\\apps\\Manual"
LOG_FILE = os.path.join(os.path.dirname(DECOMPILE_DIR), "process.log")

os.makedirs(DECOMPILE_DIR, exist_ok=True)


def Log(log_info):
    with open(LOG_FILE, "a", encoding="GBK") as f:
        f.write(log_info)


def ApkRename(apk_path: str):
    """
    重命名apk包名，防止jadx无法解析apk
    :param apk_path: apk全路径
    :return: 新的apk包名
    """
    if not os.path.isfile(apk_path) or not apk_path.endswith(".apk") or "-" not in apk_path:
        return apk_path

    apk_name = apk_path[:apk_path.find("-")] + ".apk"
    os.rename(apk_path, apk_name)
    return apk_name


def FindInstalledPackageCode(file):
    """
    查找关键代码
    :param file: 目标java代码文件
    :return:
    """
    with open(file, "rb") as f:
        java_codes = f.read()

    # if b".getInstalledPackages(" not in java_codes or b".getRunningAppProcesses(" not in java_codes:  # 如果没有找到目标代码，则不进行下面的操作
    if b".getInstalledPackages(" not in java_codes:  # 如果没有找到目标代码，则不进行下面的操作
        return

    # target_index = java_codes.find(b".getInstalledPackages(")
    # begin_index = java_codes.rfind(b"\r\n\r\n", 0, target_index)
    # end_index = java_codes.find(b"\r\n\r\n", target_index)
    # target_codes = java_codes[begin_index: end_index].strip()

    file = file[file.find(os.path.basename(DECOMPILE_DIR)) + len(os.path.basename(DECOMPILE_DIR)) + 1:].replace("\\",
                                                                                                                "_")
    dir_name = file[:file.find("_")]
    file_name = file[file.find("_") + 1:]

    # manual_work_filename = os.path.join(MANUAL_WORK_DIR, dir_name, file_name[:file_name.find(".java")] + "_" + str(target_index) + ".java")  # 构建含有目标代码的新的文件名
    manual_work_filename = os.path.join(MANUAL_WORK_DIR, dir_name, file_name)
    os.makedirs(os.path.dirname(manual_work_filename), exist_ok=True)

    if os.path.isfile(manual_work_filename):
        return

    with open(manual_work_filename, "wb") as f:
        f.write(java_codes)


def Analysis(decompile_dir):
    """
    递归文件夹，分析java代码
    :param decompile_dir: 反编译后的文件夹
    :return:
    """
    file_list = [os.path.join(decompile_dir, base_name) for base_name in os.listdir(decompile_dir)]
    for file in file_list:
        if os.path.isdir(file):
            Analysis(file)

        if os.path.isfile(file) and os.path.basename(file).endswith(".java"):
            FindInstalledPackageCode(file)


def AnalysisApkPackage(apk_list):
    """
    分析apk包
    :param apk_list: apk文件列表
    :return:
    """
    for apk_package in map(ApkRename, apk_list):
        if os.path.isdir(apk_package):
            continue

        dst_dir = os.path.join(DECOMPILE_DIR, os.path.basename(apk_package)[:os.path.basename(apk_package).find(".")])

        # todo: 分线程进行下面两步
        if not os.path.exists(dst_dir):  # 如果已经反编译过了，则无需再次进行
            try:
                Log("Begin decompile {apk}.\n".format(apk=apk_package))
                start_decompile_time = time.time()
                call(JADX_CMD.format(jadx=JADX_PATH,
                                     dst_dir=dst_dir,
                                     apk_path=apk_package),
                     timeout=180,
                     shell=True)
                end_decompile_time = time.time()
                Log("End decompile {apk}. Use time {decompile_time}'s.\n".format(apk=apk_package,
                                                                                 decompile_time=end_decompile_time - start_decompile_time))
            except:
                traceback.print_exc()

        Log("\nBegin analysis {apk}.\n".format(apk=apk_package))
        start_analysis_time = time.time()
        Analysis(dst_dir)
        end_analysis_time = time.time()
        Log("End analysis {apk}.Use time {analysis_time}'s.\n\n".format(apk=apk_package,
                                                                        analysis_time=end_analysis_time - start_analysis_time))


def main():
    apk_list = [os.path.join(APK_DIR, apk) for apk in os.listdir(APK_DIR) if apk.endswith(".apk")]
    AnalysisApkPackage(apk_list)


if __name__ == "__main__":
    main()
