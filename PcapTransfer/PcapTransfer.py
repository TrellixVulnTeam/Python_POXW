#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: PcapTransfer.py 
@time: 2018/4/3 11:06 
@version: v1.0 
"""
import os
import shutil
import time

pcap_src_dir = "Z:/"
pcap_dst_dir = "E:\SignatureAnalysis\pcap"
while True:
    file_list = sorted(os.listdir(pcap_src_dir), key = lambda k: k[k.rfind('_') + 1:k.rfind('.')])[:-1]
    for file_name in file_list:
        try:
            file_src_path = os.path.join(pcap_src_dir, file_name)
            file_dst_path = os.path.join(pcap_dst_dir, file_name)
            shutil.move(file_src_path, file_dst_path)
            print("Copy {srcFile} to {dstFile} success。".format(srcFile = file_src_path, dstFile = file_dst_path))
        except:
            print("ATTENTION: Copy {file_name} fail!".format(file_name = file_name))
    time.sleep(600)
