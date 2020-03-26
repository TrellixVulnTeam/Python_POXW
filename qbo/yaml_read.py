"""
@file: yaml_read.py
@time: 2020/3/16
@author: alfons
"""
import yaml
import json

print json.dumps({'QBOP0B00S02': {'physical_used_size': 4512776192, 'physical_name': 'P0B00S02', 'logical_total_size': '800G', 'logical_path': '/dev/mapper/QBOP0B00S02', 'space_saving': 'N/A', 'physical_path': '/dev/qdisk/P0B00S02', 'physical_total_size': '372G', 'physical_used_percent': 1, 'qbo_is_start': True}, 'QBOP0B00S03': {'physical_used_size': 83857670144, 'physical_name': 'P0B00S03', 'logical_total_size': '800G', 'logical_path': '/dev/mapper/QBOP0B00S03', 'space_saving': 75, 'physical_path': '/dev/qdisk/P0B00S03', 'physical_total_size': '372G', 'physical_used_percent': 20, 'qbo_is_start': True}, 'QBOP0B00S08': {'physical_used_size': 4512776192, 'physical_name': 'P0B00S08', 'logical_total_size': '800G', 'logical_path': '/dev/mapper/QBOP0B00S08', 'space_saving': 'N/A', 'physical_path': '/dev/qdisk/P0B00S08', 'physical_total_size': '372G', 'physical_used_percent': 1, 'qbo_is_start': True}, 'QBOP0B00S04': {'physical_used_size': 83710894080, 'physical_name': 'P0B00S04', 'logical_total_size': '800G', 'logical_path': '/dev/mapper/QBOP0B00S04', 'space_saving': 75, 'physical_path': '/dev/qdisk/P0B00S04', 'physical_total_size': '372G', 'physical_used_percent': 20, 'qbo_is_start': True}, 'QBOP0B00S05': {'physical_used_size': 45611155456, 'physical_name': 'P0B00S05', 'logical_total_size': '800G', 'logical_path': '/dev/mapper/QBOP0B00S05', 'space_saving': 79, 'physical_path': '/dev/qdisk/P0B00S05', 'physical_total_size': '372G', 'physical_used_percent': 11, 'qbo_is_start': True}}, indent=4)

with open("./config.yml", 'r') as f:
    data = yaml.load(f.read().replace('!', '#'))
pass
