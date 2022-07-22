"""
@file: TarTest.py
@time: 2019/9/26
@author: alfons
"""
import os
import json
import pathlib
import tarfile
import pprint

tar_file = "./Q-qdata8.3.1-001.tar.gz"

with tarfile.open(tar_file) as f:
    for file_path in f.getnames():
        if pathlib.Path(file_path).name != ".version":
            continue

        pprint.pprint(json.loads(f.extractfile(member=file_path).read().decode()), indent=4)
        pass
