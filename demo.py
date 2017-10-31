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
        r = synonyms.compare(sen1, sen2, seg=True)
        print("旗帜引领方向 vs 道路决定命运:", r)
        # assert r == 0.0, "the similarity should be zero"

        sen1 = "发生历史性变革"
        sen2 = "取得历史性成就"
        r = synonyms.compare(sen1, sen2, seg=True)
        print("发生历史性变革 vs 取得历史性成就:", r)
        # assert r > 0, "the similarity should be bigger then zero"



    def testNearbyWords(self):
        synonyms.display("人脸") # synonyms.display calls synonyms.nearby

def test():
    unittest.main()

if __name__ == '__main__':
    test()
