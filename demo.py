#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=========================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/demo.py
# Author: Hai Liang Wang
# Date: 2017-09-28:22:23:34
#
#=========================================================================

"""

"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2017-09-28:22:23:34"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import synonyms  # https://github.com/huyingxi/Synonyms
import numpy
import unittest

compare_ = lambda x,y,z: "%s vs %s: %f" % (x, y, synonyms.compare(x, y, seg=z))

# run testcase: python /Users/hain/ai/Synonyms/demo.py Test.testExample
class Test(unittest.TestCase):
    '''

    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_pairs(self):
        print("test_pairs")
        print("*"* 30)
        print(compare_("轿车", "汽车", True))
        print("*"* 30)
        print(compare_("宝石", "宝物", True))
        print("*"* 30)
        print(compare_("旅游", "游历", True))
        print("*"* 30)
        print(compare_("男孩子", "小伙子", True))
        print("*"* 30)
        print(compare_("海岸", "海滨", True))
        print("*"* 30)
        print(compare_("庇护所", "精神病院", True))
        print("*"* 30)
        print(compare_("魔术师", "巫师", True))
        print("*"* 30)
        print(compare_("中午", "正午", True))
        print("*"* 30)
        print(compare_("火炉", "炉灶", True))
        print("*"* 30)
        print(compare_("食物", "水果", True))
        print("*"* 30)
        print(compare_("鸡", "公鸡", True))
        print("*"* 30)
        print(compare_("鸟", "鹤", True))
        print("*"* 30)
        print(compare_("工具", "器械", True))
        print("*"* 30)
        print(compare_("兄弟", "和尚", True))
        print("*"* 30)
        print(compare_("起重机", "器械", True))

    def test_similarity(self):
        '''
        Generate sentence similarity
        '''
        sen1 = "旗帜引领方向"
        sen2 = "道路决定命运"
        r = synonyms.compare(sen1, sen2, seg=True)
        print("旗帜引领方向 vs 道路决定命运:", r)
        # assert r == 0.0, "the similarity should be zero"

        sen1 = "旗帜引领方向"
        sen2 = "旗帜指引道路"
        r = synonyms.compare(sen1, sen2, seg=True)
        print("旗帜引领方向 vs 旗帜指引道路:", r)
        # assert r > 0, "the similarity should be bigger then zero"


        sen1 = "发生历史性变革"
        sen2 = "发生历史性变革"
        r = synonyms.compare(sen1, sen2, seg=True)
        print("发生历史性变革 vs 发生历史性变革:", r)
        # assert r > 0, "the similarity should be bigger then zero"

        sen1 = "骨折"
        sen2 = "巴赫"
        r = synonyms.compare(sen1, sen2, seg=True)
        print("%s vs %s" % (sen1, sen2), r)
     

    def test_nearby(self):
        synonyms.display("人脸")  # synonyms.display calls synonyms.nearby


def test():
    unittest.main()


if __name__ == '__main__':
    test()
