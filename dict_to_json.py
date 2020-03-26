#!/usr/bin/env python
# encoding: utf-8
"""
@file: dict_to_json.py
@time: 2020/3/25
@author: alfons
"""
set_a = {(1, 2), (1, 2), ("@", "B"), ("@", "B"), {"b": "a"}, {"b": "a"}}
print set_a


import json

dict_a = [
    {"Slot": "P0B00S03p1", "SpaceSavingSize": "0.0B", "PhysicalSizeByte": 379459731456, "Ratio": "2.1x", "Name": "QP0B00S03", "LogicalUsedSizeByte": 0, "PhysicalUsedSize": "5.6GB",
     "Compress": "N/A", "PhysicalUsedSizeByte": 6003548160, "SpaceSavingSizeByte": 0, "Status": "Started", "PhysicalUsedPercent": 1, "LogicalSize": "744.0GB",
     "PhysicalSize": "353.4GB", "Path": "/dev/qdisk/QP0B00S03", "SpaceSavingPercent": 0, "LogicalUsedSize": "0.0B", "LogicalSizeByte": 798863917056},
    {"Slot": "P0B00S04p1", "SpaceSavingSize": "0.0B", "PhysicalSizeByte": 379459731456, "Ratio": "3.0x", "Name": "QP0B00S04", "LogicalUsedSizeByte": 0, "PhysicalUsedSize": "5.6GB",
     "Compress": "N/A", "PhysicalUsedSizeByte": 6003548160, "SpaceSavingSizeByte": 0, "Status": "Started", "PhysicalUsedPercent": 1, "LogicalSize": "1.0TB",
     "PhysicalSize": "353.4GB", "Path": "/dev/qdisk/QP0B00S04", "SpaceSavingPercent": 0, "LogicalUsedSize": "0.0B", "LogicalSizeByte": 1138379194368},
    {"Slot": "P0B00S05p1", "SpaceSavingSize": "0.0B", "PhysicalSizeByte": 379459731456, "Ratio": "2.1x", "Name": "QP0B00S05", "LogicalUsedSizeByte": 0, "PhysicalUsedSize": "5.6GB",
     "Compress": "N/A", "PhysicalUsedSizeByte": 6003548160, "SpaceSavingSizeByte": 0, "Status": "Started", "PhysicalUsedPercent": 1, "LogicalSize": "744.0GB",
     "PhysicalSize": "353.4GB", "Path": "/dev/qdisk/QP0B00S05", "SpaceSavingPercent": 0, "LogicalUsedSize": "0.0B", "LogicalSizeByte": 798863917056}]

with open("dict_a.json", "w") as f:
    f.write(json.dumps(dict_a, indent=4))
