#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/synonyms/__init__.py
# Author: Hai Liang Wang
# Date: 2017-09-27
#
#===============================================================================

"""
Chinese Synonyms for Natural Language Processing and Understanding.
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hu Ying Xi<>, Hai Liang Wang<hailiang.hl.wang@gmail.com>"
__date__      = "2017-09-27"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

PLT = 2

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"
else:
    PLT = 3

import gzip
import thulac # http://thulac.thunlp.org/
import shutil

_vocab = dict()
_size = 0
_thulac = thulac.thulac() #默认模式
_fin_path = os.path.join(curdir, os.path.pardir, 'tmp', 'words.nearby.gz')
_fin_cached_vocab_path = os.path.join(curdir, 'data', 'words.nearby.%d.pklz' % PLT)

if PLT == 2:
    import cPickle as pickle
else:
    import pickle

def dump_pickle_file(file_path, data):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)
    with gzip.open(file_path, "wb") as fout:
        print("dump pickle file, version ", pickle.HIGHEST_PROTOCOL)
        pickle.dump(data, fout, protocol=pickle.HIGHEST_PROTOCOL)
        print("done.")

def load_pickle_file(file_path):
    if os.path.exists(file_path):
        with gzip.open(file_path, "rb") as fin:
            return pickle.load(fin)
    else: 
        return None

def add_word_to_vocab(word, nearby, nearby_score):
    '''
    Add word into vocab by word, nearby lis and nearby_score lis
    '''
    global _size
    if not word is None:
        if PLT == 2:
            word = word.encode("utf-8")
            nearby = [z.encode("utf-8") for z in nearby]
        _vocab[word] = [nearby, nearby_score]
        _size += 1

def _build_vocab():
    '''
    Build vocab
    '''
    _fin = []
    if PLT == 2:
        import io
        _fin=io.TextIOWrapper(io.BufferedReader(gzip.open(_fin_path)), encoding='utf8', errors='ignore')
    else:
        _fin=gzip.open(_fin_path,'rt', encoding='utf-8', errors = "ignore")

    c = None # current word
    w = []   # word nearby 
    s = []   # score of word nearby
    for v in _fin.readlines():
        v = v.strip()
        if v is None or len(v) == 0: continue
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
    add_word_to_vocab(c, w, s) # add the last word
    print(">> Synonyms vocabulary size: %s" % _size)

def _load_vocab():
    '''
    load vocab dict
    '''
    global _vocab
    try:
        o = load_pickle_file(_fin_cached_vocab_path)
        if o is None:
            _build_vocab()
            dump_pickle_file(_fin_cached_vocab_path, _vocab)
        else:
            _vocab = o
    except Exception as e:
        '''
        Just load the data without cached policy
        '''
        _build_vocab()

# build on load
print(">> Synonyms on loading ...")
_load_vocab()

def nearby(word):
    '''
    Nearby word
    '''
    try:
        return _vocab[word]
    except KeyError as e:
        return [[],[]]

def _segment_words(sen):
    '''
    segment words
    '''
    text = _thulac.cut(sen, text=True)  #进行一句话分词
    words, tags = [], []
    data = [x.rsplit('_', 1) for x in text.split()]
    for _ in data:
        assert len(_) == 2, "seg len should be 2"
        words.append(_[0])
        tags.append(_[1])
    return words, tags

def _similarity(w1, t1, w2, t2, explain = False):
    '''
    compute similarity
    '''
    vocab_space = dict()
    
    for (k,v) in enumerate(t2):
        vocab_space[w2[k]] = 1
        for k2,v2 in enumerate(nearby(w2[k])[0]):
            vocab_space[v2] = nearby(w2[k])[1][k2]
        
    if explain: print(vocab_space)
    total = 0
    overlap = 0
    for (k,v) in enumerate(t1):
        if v.startswith("n") or v.startswith("v"): # 去停，去标，去副词、形容词、代词 etc.
            total += 1
            if w1[k] in vocab_space:
                # overlap += word2_weight_vocab[word1[k]]
                overlap += 1 # set 1 to all included word
    if total == 0:
        return 0.0
    return float("{:1.2f}".format(overlap/total))

def compare(s1, s2):
    '''
    compare similarity
    '''
    w1, t1 = _segment_words(s1)
    w2, t2 = _segment_words(s2)
    return max(_similarity(w1, t1, w2, t2), _similarity(w2, t2, w1, t1))

def display(word):
    print("'%s'近义词：" % word)
    o = nearby(word)
    assert len(o) == 2, "should contain 2 list"
    if len(o[0]) == 0: print(" out of vocabulary")
    for k,v in enumerate(o[0]):
        print("  %d. %s:%s" %(k+1, v, o[1][k]))

def main():
    display("人脸")
    display("NOT_EXIST")

if __name__ == '__main__':
    main()