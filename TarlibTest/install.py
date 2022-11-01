#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import logging
import subprocess
import tarfile

main_env_path = "/usr/local/sendoh/python_env/3.8.6/main"
main_env_package = "qversion_env_main.tar.gz"

virtual_env_package = "qversion_env_virtual.tar.gz"

system_lib_path = "/usr/local/sendoh/python_env/system_lib"
system_lib_package = "system_lib.tar.gz"

def tar_x(file_path):
    with tarfile.open(file_path) as f:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(f)

def main():
    parser = argparse.ArgumentParser(description="虚拟环境安装脚本",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--install-main",
                        help="是否安装main环境({main_env})，默认情况下会自动判断是否需要安装。"
                             "".format(main_env=main_env_package),
                        required=False,
                        default=False,
                        action="store_true",
                        dest="install_main")

    parser.add_argument("--install-library",
                        help="是否安装环境动态库相关依赖({system_lib})，默认情况下会自动判断是否需要安装。"
                             "".format(system_lib=system_lib_package),
                        required=False,
                        default=False,
                        action="store_true",
                        dest="install_lib")

    args = parser.parse_args(args=sys.argv[1:])

    # 安装虚拟环境
    run_local_cmd("tar -xvzf {archive_name} -C /".format(archive_name=virtual_env_package))
    with open("/tmp/env_install", "a+") as f:
        f.write("install virtual_env_package over\n")

    # 安装主环境
    if args.install_main or not os.path.isdir(main_env_path):
        run_local_cmd("tar -xvzf {archive_name} -C /".format(archive_name=main_env_package))
    else:
        run_local_cmd("tar -xvzf {archive_name} --skip-old-files -C / &2>/dev/null".format(archive_name=main_env_package))

    with open("/tmp/env_install", "a+") as f:
        f.write("install main over\n")

    # 安装环境动态库依赖
    if args.install_lib or not os.path.isdir(system_lib_path):
        run_local_cmd("tar -xvzf {archive_name} -C /".format(archive_name=system_lib_package))
    else:
        run_local_cmd("tar -xvzf {archive_name} --skip-old-files -C / &2>/dev/null".format(archive_name=system_lib_package))

    with open("/tmp/env_install", "a+") as f:
        f.write("install system_lib_package over\n")


if __name__ == '__main__':
    main()
