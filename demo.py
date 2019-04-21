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
    # 

from absl import flags
from absl import logging

FLAGS = flags.FLAGS
import synonyms  # https://github.com/huyingxi/Synonyms
import numpy
import unittest

compare_ = lambda x,y,z: "%s vs %s: %f" % (x, y, synonyms.compare(x, y, seg=z)) + "\n" +"*"* 30 + "\n"

# run testcase: python /Users/hain/ai/Synonyms/demo.py Test.testExample
class Test(unittest.TestCase):
    '''

    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wordseg(self):
        print("test_wordseg")
        print(synonyms.seg("中文近义词工具包"))


    def test_word_vector(self):
        print("test_word_vector")
        word = "三国"
        print(word, "向量", synonyms.v(word))

    def test_diff(self):
        print("test_diff")
        result = []
        # 30个  评测词对中的左侧词
        left = ['轿车', '宝石', '旅游', '男孩子', '海岸', '庇护所', '魔术师', '中午', '火炉', '食物', '鸟', '鸟', '工具', '兄弟', '起重机', '小伙子',
                '旅行', '和尚', '墓地', '食物', '海岸', '森林', '岸边', '和尚', '海岸', '小伙子', '琴弦', '玻璃', '中午', '公鸡']
        # 30个  评测词对中的右侧词
        right = ['汽车', '宝物', '游历', '小伙子', '海滨', '精神病院', '巫师', '正午', '炉灶', '水果', '公鸡', '鹤', '器械', '和尚', '器械', '兄弟',
                 '轿车', '圣贤', '林地', '公鸡', '丘陵', '墓地', '林地', '奴隶', '森林', '巫师', '微笑', '魔术师', '绳子', '航行']
        # 人工评定的相似度列表。
        human = [0.98, 0.96, 0.96, 0.94, 0.925, 0.9025, 0.875, 0.855, 0.7775, 0.77, 0.7625, 0.7425, 0.7375, 0.705, 0.42, 0.415,
                 0.29, 0.275, 0.2375,
                 0.2225, 0.2175, 0.21, 0.1575, 0.1375, 0.105, 0.105, 0.0325, 0.0275, 0.02, 0.02]
        result.append("# synonyms 分数评测 [(v%s)](https://pypi.python.org/pypi/synonyms/%s)" % (synonyms.__version__, synonyms.__version__))
        result.append("| %s |  %s |   %s  |  %s |" % ("词1", "词2", "synonyms", "人工评定"))
        result.append("| --- | --- | --- | --- |")
        for x,y,z in zip(left, right, human):
            result.append("| %s | %s | %s  |  %s |" % (x, y, synonyms.compare(x, y), z))
        for x in result: print(x)
        with open(os.path.join(curdir, "VALUATION.md"), "w") as fout:
            for x in result: fout.write(x + "\n")

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


        sen1 = "你们好呀"
        sen2 = "大家好"
        r = synonyms.compare(sen1, sen2, seg=False)
        print("%s vs %s" % (sen1, sen2), r)


    def test_swap_sent(self):
        print("test_swap_sent")        
        s1 = synonyms.compare("教学", "老师")
        s2 = synonyms.compare("老师", "教学")
        print('"教学", "老师": %s ' % s1)
        print('"老师", "教学": %s ' % s2)
        assert s1 == s2, "Scores should be the same after swap sents"

    def test_nearby(self):
        synonyms.display("奥运")  # synonyms.display calls synonyms.nearby
        synonyms.display("北新桥")  # synonyms.display calls synonyms.nearby


    def test_badcase_1(self):
        synonyms.display("人脸")  # synonyms.display calls synonyms.nearby


    def test_basecase_2(self):
        print("test_basecase_2")
        sen1 = "今天天气"
        sen2 = "今天天气怎么样"
        r = synonyms.compare(sen1, sen2, seg=True)

def test():
    unittest.main()


if __name__ == '__main__':
    FLAGS([__file__, '--verbosity', '1'])
    test()
