#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/demo.py
# Author: Hai Liang Wang
# Date: 2017-09-28:22:23:34
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2017-09-28:22:23:34"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import synonyms # https://github.com/huyingxi/Synonyms
import numpy
import unittest
import thulac

# run testcase: python /Users/hain/ai/Synonyms/demo.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSenSimilarity(self):
        '''
        Generate sentence similarity
        '''
        sen1 = "旗帜引领方向"
        sen2 = "道路决定命运"
        assert synonyms.compare(sen1, sen2) == 0.0, "the similarity should be zero"

        sen1 = "发生历史性变革"
        sen2 = "取得历史性成就"
        assert synonyms.compare(sen1, sen2) > 0, "the similarity should be bigger then zero"

    def testNearbyWords(self):
        thu1 = thulac.thulac() #默认模式
        text = thu1.cut("人脸识别", text=True)  #进行一句话分词
        words, tags = [], []
        data = [x.rsplit('_', 1) for x in text.split()]
        for _ in data:
            assert len(_) == 2, "seg len should be 2"
            words.append(_[0])
            tags.append(_[1])
        for (k,v) in enumerate(tags):
            if v.startswith("n") or v.startswith("v"): # 去停，去标，去副词、形容词、代词 etc.
                synonyms.display(words[k]) # synonyms.display calls synonyms.nearby

def test():
    unittest.main()

if __name__ == '__main__':
    test()