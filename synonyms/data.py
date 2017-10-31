#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/synonyms/data.py
# Author: Hai Liang Wang
# Date: 2017-10-31:17:13:51
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2017-10-31:17:13:51"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"


def add_word_to_vocab(word, nearby, nearby_score):
    '''
    Add word into vocab by word, nearby lis and nearby_score lis
    '''
    global _size
    if word is not None:
        if PLT == 2:
            word = any2unicode(word)
            nearby = [any2unicode(z) for z in nearby]
        _vocab[word] = [nearby, nearby_score]
        _size += 1

def _build_vocab():
    '''
    Build vocab
    '''
    _fin = []
    if PLT == 2:
        import io
        _fin = io.TextIOWrapper(
            io.BufferedReader(
                gzip.open(_fin_path)),
            encoding='utf8',
            errors='ignore')
    else:
        _fin = gzip.open(_fin_path, 'rt', encoding='utf-8', errors="ignore")

    c = None  # current word
    w = []   # word nearby
    s = []   # score of word nearby
    for v in _fin.readlines():
        v = v.strip()
        if v is None or len(v) == 0:
            continue
        if v.startswith("query:"):
            add_word_to_vocab(c, w, s)
            o = v.split(":")
            c = o[1].strip()
            w, s = [], []
        else:
            o = v.split()
            assert len(o) == 2, "nearby data should have text and score"
            w.append(o[0].strip())
            s.append(float(o[1]))
    add_word_to_vocab(c, w, s)  # add the last word
    print(">> Synonyms vocabulary size: %s" % _size)


import unittest

# run testcase: python /Users/hain/ai/Synonyms/synonyms/data.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExample(self):
        print("foo")

def test():
    unittest.main()

if __name__ == '__main__':
    test()
