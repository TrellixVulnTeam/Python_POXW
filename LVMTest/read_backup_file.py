#!/usr/bin/env python
# -*- coding: utf-8 -*-


import string
import json


def convert_value(value):
    """
    根据传入的字符串类型进行转换
    :param str value: 传入字符串
    :return:
    """
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    if  value.startswith('[') and value.endswith(']'):
        return json.loads(value)

    if value.isdigit():
        return int(value)


def get_attr(attr_lines):
    attr_dict = dict()
    attr_lines_length = len(attr_lines)
    index = 0
    while index < attr_lines_length:
        line_str = attr_lines[index].strip()

        if '=' in line_str:
            attr_key, attr_value = line_str.split('=', 1)
            attr_key = attr_key.strip()
            attr_value = convert_value(attr_value.split('#')[0].strip())
            attr_dict.update({attr_key: attr_value})

        if line_str.endswith('{'):
            attr_key = line_str.split()[0]
            offset_index, attr_value = get_attr(attr_lines[index + 1:])
            index += offset_index
            attr_dict.update({attr_key: attr_value})

        if line_str.endswith('}'):
            return index + 1, attr_dict

        index += 1
    return index + 1, attr_dict

    # back_file_content=back_file_content.replace('\n', '')
    # value_begin_index = back_file_content.find('{')
    # value_end_index = back_file_content.rfind('}')
    #
    # key = back_file_content[:value_begin_index]
    # value = back_file_content[value_begin_index + 1: value_end_index]
    pass


if __name__ == '__main__':
    with open("./backup_file", "r") as f:
        content_lines = f.readlines()

    _, vg_info = get_attr(content_lines)
    print json.dumps(vg_info, indent=4)
