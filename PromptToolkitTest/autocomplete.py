#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: autocomplete.py
# Desc:
# Author: chenhui.shang
# Email: chenhui.shang@woqutech.com
# HomePage: www.woqutech.com
# Version: 0.0.1
# LastChange:  2020/5/6 下午5:05
# History:
#=============================================================================
"""
import pprint
import requests
import argparse
import argcomplete
from argcomplete.completers import EnvironCompleter


def github_org_members(prefix, parsed_args, **kwargs):
    resource = "https://api.github.com/orgs/{org}/members".format(org=parsed_args.organization)
    return (member['login'] for member in requests.get(resource).json() if member['login'].startswith(prefix))


parser = argparse.ArgumentParser()
parser.add_argument("--organization", help="GitHub organization")
parser.add_argument("--member", help="GitHub member").completer = github_org_members

argcomplete.autocomplete(parser)
args = parser.parse_args()

pprint.pprint(requests.get("https://api.github.com/users/{m}".format(m=args.member)).json())
