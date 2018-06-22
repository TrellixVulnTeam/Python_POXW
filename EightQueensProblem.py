#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 @Author  : Alfons
 @Contact: alfons_xh@163.com
 @File    : EightQueensProblem.py
 @Time    : 2018/6/22 10:33
"""
queenTotal = 8
recordList = list()
totalNum = 0


def IsValid(row, col):
    global recordList

    for i, j in enumerate(recordList):
        if i == row or j == col or abs(row - i) == abs(col - j):
            return False
    return True


def Queen(queenNum):
    global recordList
    global totalNum

    if queenNum == queenTotal:
        totalNum += 1
        return True

    for insertCol in range(queenTotal):
        if IsValid(queenNum, insertCol):
            recordList.append(insertCol)
            Queen(queenNum + 1)
            recordList.pop()
    return False


for i in range(13):
    queenTotal = i + 1
    Queen(0)
    print("{n} queens has {total} ways!".format(n=queenTotal, total=totalNum))
    totalNum = 0
pass
