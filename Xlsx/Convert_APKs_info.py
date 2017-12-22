#!/usr/bin/env python  
# encoding: utf-8  
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: Convert_APKs_info.py 
@time: 2017/12/22 14:23 
@version: v1.0 
"""
import json
import xlwt

with open("test_softs_info.json", "r") as f:
    softs_info_dict = json.loads(f.read())

workbook = xlwt.Workbook()
sheet = workbook.add_sheet("Top100_communication_apk")

style1 = xlwt.XFStyle()
style1.alignment.horz = style1.alignment.HORZ_CENTER
style1.font.bold = True

title_list = ["Packagename", "Version", "Version_code", "Filesize", "Fetched_at",  "md5", "Singn up", "User", "Password", "IsNeedVPN"]
for i in range(len(title_list)):
    sheet.write(0, i, title_list[i], style1)

col_width_list = [len(title) for title in title_list]

style2 = xlwt.XFStyle()
style2.alignment.horz = style2.alignment.HORZ_RIGHT

row_index = 1
for soft_name, single_info in softs_info_dict.items():
    sheet.write(row_index, 0, single_info["packagename"])
    sheet.write(row_index, 1, single_info["version"], style2)
    sheet.write(row_index, 2, single_info["version_code"], style2)
    sheet.write(row_index, 3, single_info["filesize"], style2)
    sheet.write(row_index, 4, single_info["fetched_at"], style2)
    sheet.write(row_index, 5, single_info["md5"])
    col_width_list[0] = max(len(single_info["packagename"]), col_width_list[0])
    col_width_list[1] = max(len("1" if not single_info["version"] else single_info["version"]), col_width_list[1])
    col_width_list[2] = max(len(str(single_info["version_code"])), col_width_list[2])
    col_width_list[3] = max(len(single_info["filesize"]), col_width_list[3])
    col_width_list[4] = max(len("1" if not single_info["fetched_at"] else single_info["fetched_at"]), col_width_list[4])
    col_width_list[5] = max(len(single_info["md5"]), col_width_list[5])
    row_index += 1

for i in range(len(title_list)):
    sheet.col(i).width = 256 * (col_width_list[i] + 1)

workbook.save("Top100_APKs.xls")
pass