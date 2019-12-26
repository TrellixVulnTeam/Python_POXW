"""
@file: lsblk.py
@time: 2019/12/26
@author: alfons
"""

import sys
from string import ascii_letters, digits


def parse(file_name):
    result = dict()
    physical_device = ""
    with open(file_name, 'rb') as input_file:
        for line in input_file:
            temp_arr = line.decode().split(' ')
            if temp_arr[0] and temp_arr[0][0] in list(ascii_letters + digits):
                physical_device = temp_arr[0]

            for item in temp_arr[1:]:
                if '└─' in item or '├─' in item:
                    block_device = item.replace('└─', '').replace('├─', '')
                    if block_device.startswith("drbd"):
                        block_num = int(block_device.replace('drbd', ''))
                        block_device = "LUN{}".format(block_num-1000+1)

                    result[block_device] = physical_device
    return result


if __name__ == '__main__':
    res = parse("./lsblk_output.txt")
    pass
