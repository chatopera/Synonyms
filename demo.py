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

import thulac # http://thulac.thunlp.org/
import synonyms # https://github.com/huyingxi/Synonyms
import numpy
import unittest


thulac_c = thulac.thulac() #默认模式

def segment_words(sen):
    '''
    segment words
    '''
    text = thulac_c.cut(sen, text=True)  #进行一句话分词
    words, tags = [], []
    data = [x.rsplit('_', 1) for x in text.split()]
    for _ in data:
        assert len(_) == 2, "seg len should be 2"
        words.append(_[0])
        tags.append(_[1])
    return words, tags

def similarity(s1, s2):
    '''
    '''
    word1, tag1 = segment_words(s1)
    word2, tag2 = segment_words(s2)
    word2_weight_vocab = dict()
    
    for (k,v) in enumerate(tag2):
        word2_weight_vocab[word2[k]] = 1
        for k2,v2 in enumerate(synonyms.nearby(word2[k])[0]):
            word2_weight_vocab[v2] = synonyms.nearby(word2[k])[1][k2]
        
    print(word2_weight_vocab)
    ct = 0
    score = 0
    for (k,v) in enumerate(tag1):
        if v.startswith("n") or v.startswith("v"): # 去停，去标，去副词、形容词、代词 etc.
            ct += 1
            if word1[k] in word2_weight_vocab:
                score += word2_weight_vocab[word1[k]]
    return float("{:1.2f}".format(score/ct))

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
        sen1 = "未来智能互联网不仅仅是搜索"
        sen2 = "未来的互联网是基于人工智能的智能互联"
        print(max(similarity(sen1, sen2), similarity(sen2, sen1)))

    def testWordseg(self):
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
                print("%s: %s" % (words[k], synonyms.nearby(words[k])))

def test():
    unittest.main()

if __name__ == '__main__':
    test()