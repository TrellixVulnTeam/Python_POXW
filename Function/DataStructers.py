#!/usr/bin/env python
# encoding: utf-8
"""
@author: Alfons
@contact: alfons_xh@163.com
@file: DataStructers.py 
@time: 2017/4/25 9:30 
@version: v1.0 
"""


def list_func():
    shoplist = ["banana", "datastruct", "mango", "carrot"]
    print "I have", len(shoplist), "items to purchase"
    print "Thase items are:", shoplist

    print "I alse want to buy rice."
    shoplist.append("rice")
    print "My items now are:", shoplist

    print "Sort my list now."
    shoplist.sort()
    print "After sort,items are:", shoplist

    print "My first item I will but is:", shoplist[0]
    olditem = shoplist[0]
    del shoplist[0]
    print "My buy item is", olditem
    print "My items now are:", shoplist


def tuple_func():
    zoo = ('python', 'elephant', 'penguin')
    print'Number of animals in the zoo is', len(zoo)

    new_zoo = 'monkey', 'camel', zoo
    print'Number of cages in the new zoo is', len(new_zoo)
    print'All animals in new zoo are', new_zoo
    print'Animals brought from old zoo are', new_zoo[2]
    print'Last animal brought from old zoo is', new_zoo[2][2]
    print'Number of animals in the new zoo is', len(new_zoo) - 1 + len(new_zoo[2])


# “ab”是地址（Address）簿（Book）的缩写
def dictionary_func():
    ab = {
        "Alfons": "alfons_xh@163.com",
        "xiaohui100": "xiaohuihui100@gmail.com",
        "shangchenhui": "18602807364"
    }
    print ab
    print "Alfons address is:", ab["Alfons"]

    del ab["shangchenhui"]
    print "\nThere is", len(ab), "items now."

    for name, address in ab.items():
        print name, ":", address

    ab["yagoo"] = "yagoo@gmail.com"
    print ab["yagoo"]


def seq_function():
    store = ["apple", "mango", "carrot", "banana"]
    name = "Alfons"

    print store
    print name
    print 'Item 0 is', store[0]
    print 'Item 1 is', store[1]
    print 'Item -1 is', store[-1]
    print 'Item -2 is', store[-2]
    print 'Char 0 in name is:', name[0]

    # Slicing on a list #
    print '\nstore:',store
    print 'Item 1 to 3 is', store[1:3]
    print 'Item 2 to end is', store[2:]
    print 'Item 1 to -1 is', store[1:-1]
    print 'Item start to end is', store[:]

    # 从某一字符串中切片 #
    print '\nname:',name
    print 'characters 1 to 3 is', name[1:3]
    print 'characters 2 to end is', name[2:]
    print 'characters 1 to -1 is', name[1:-1]
    print 'characters start to end is', name[:]

    print '_*_'.join(store)


if __name__ == "__main__":
    list_func()
    tuple_func()
    dictionary_func()
    seq_function()