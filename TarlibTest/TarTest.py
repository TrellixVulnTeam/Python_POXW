"""
@file: TarTest.py
@time: 2019/9/26
@author: alfons
"""
import os
import tarfile

tar_file = "./qdatamagr_upgrade.tar.gz"

with tarfile.open(tar_file) as f:
    names = f.getnames()
    for n in names:
        if not n.endswith("/qdata_version.conf"):
            continue
        f.extract(n, path='./new')
        print(os.path.join("tmp", n))

try:
    raise KeyError("err")
except Exception as e:
    print(str(e))