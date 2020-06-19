#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: git_test.py
# Author: alfons
# LastChange:  2020/6/15 下午7:59
#=============================================================================
"""
import git

# new_repo = git.Repo.clone_from("git@gitlab.woqutech.com:qdata/qdata-mgr.git", to_path="/tmp/qdatamgr")
repo = git.Repo("/tmp/qdatamgr")
repo.index
print list(repo.refs)