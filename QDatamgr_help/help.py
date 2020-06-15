#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@file: help.py
@time: 2020/6/3
@author: alfons
"""
import os
import yaml
import subprocess

def read_help(main_file, output_file):
    with open("./modules.yml", "r") as f:
        main_command_list = yaml.load(f)
        res_list = list()
        for main_command in main_command_list:
            res_list.append(main_command.center(100, "="))
            print main_command

            # 截取子命令
            p = subprocess.Popen("source /home/sendoh/sendoh-dev-env/bin/activate && python /tmp/pycharm_project_789/src/{main_file} {main_cmd} -h"
                                 "".format(main_file=main_file,
                                           main_cmd=main_command),
                                 shell=True,
                                 stdout=subprocess.PIPE)
            stdout_str = p.stdout.read()
            stdout_str_list = stdout_str.splitlines()

            start_index = 0
            end_index = len(stdout_str_list)
            for index, line in enumerate(stdout_str_list):
                if "<subcommands>" in line.lower():
                    start_index = index + 1
                if "optional arguments" in line.lower():
                    end_index = index - 1

            sub_command_list = [c for c in stdout_str_list[start_index:end_index] if c[:8].count(' ') < 8]

            # 子命令选项
            for sub_command in sub_command_list:
                print sub_command
                sub_command = sub_command.strip().split()[0]
                res_list.append(sub_command.center(20, '-'))

                s = subprocess.Popen("source /home/sendoh/sendoh-dev-env/bin/activate && python /tmp/pycharm_project_789/src/{main_file} {m} {s} -h"
                                     "".format(main_file=main_file,
                                               m=main_command,
                                               s=sub_command),
                                     shell=True,
                                     stdout=subprocess.PIPE)

                # sub_command_args_list = s.stdout.read().splitlines()
                # positional_start_index = -1
                # positional_end_index = -1
                # optional_start_index = -1
                # optional_end_index = len(sub_command_args_list)
                # for index, line in enumerate(sub_command_args_list):
                #     if "positional arguments" in line.lower():
                #         positional_start_index = index + 1
                #
                #     if "optional arguments" in line.lower():
                #         positional_end_index = index - 1
                #         optional_start_index = index + 1
                #
                # positional_args_list = sub_command_args_list[positional_start_index: positional_end_index] \
                #     if positional_start_index > 0 and positional_end_index > 0 else list()
                # optional_args_list = sub_command_args_list[optional_start_index: optional_end_index] \
                #     if optional_start_index > 0 else list()
                # optional_args_list = [optional for optional in optional_args_list if "-h" not in optional]
                #
                # positional_args = ["  - **{}**".format(p.strip()) for p in positional_args_list + optional_args_list]
                # res_list.extend(positional_args)
                res_list.append(s.stdout.read())
                res_list.append("\n")

        with open(output_file, "w") as f:
            f.write("\n".join(res_list))

if __name__ == '__main__':
    read_help("main.py", "./qdatamgr_help.md")
    read_help("api_main.py", "./api_qdatamgr_help.md")