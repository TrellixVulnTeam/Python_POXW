"""
@author: Alfons
@contact: alfons_xh@163.com
@file: audioBroadPlayback.py
@time: 2019/6/21 下午8:32
@version: v1.0 
"""
import os

import re
import fileinput
import time
import subprocess
import threading

output_file_name = "./output.wav"
os.remove(output_file_name) if os.path.isfile(output_file_name) else ...

input_device_str = subprocess.check_output("pactl list | sed -n \"/状态：RUNNING/,/采样规格/p\"", shell=True).decode("utf-8")
input_device_info_str_list = input_device_str.split("状态：RUNNING")
input_device_info_str_list = [i for i in input_device_info_str_list if "alsa_output" in i]

ffmpeg_cmd_list = list()
for device_info_str in input_device_info_str_list:
    # print(re.search(r".*名称：(.*?)\n\t.*采样规格:.*\n\t", device_info_str).groups())
    device, _, ac, ar = re.search(r"名称：(.*?)(\n\t.*)*采样规格：s16le ([\d]+)ch ([\d]+)Hz", device_info_str, re.A).groups()
    ffmpeg_cmd_list.append("-f pulse -ac {ac} -ar {ar} -i {device}".format(ac=ac, ar=ar, device=device))

ffmpeg_cmd = "ffmpeg {sub} -filter_complex amix=inputs={dev_num} {output}".format(sub=" ".join(ffmpeg_cmd_list),
                                                                                  dev_num=len(ffmpeg_cmd_list),
                                                                                  output=output_file_name)
p = subprocess.Popen(ffmpeg_cmd, shell=True)

while True:
    if os.path.isfile(output_file_name):
        break

seek_offset = 0
while True:
    with open(output_file_name, "rb") as f:
        new_offset = len(f.read())
        if seek_offset == new_offset:
            continue

        f.seek(seek_offset)
        b_str = f.read()
        seek_offset += len(b_str)
        print(seek_offset)

import ffmpeg