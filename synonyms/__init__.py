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
import numpy as np
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

PLT = 2

if sys.version_info[0] < 3:
    default_stdout = sys.stdout
    default_stderr = sys.stderr
    reload(sys)
    sys.stdout = default_stdout
    sys.stderr = default_stderr
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"
else:
    PLT = 3

import gzip
import shutil
import jieba.posseg as _tokenizer
import jieba

_vocab = dict()
_size = 0
_fin_path = os.path.join(curdir, os.path.pardir, 'tmp', 'words.nearby.gz')
_fin_cached_vocab_path = os.path.join(curdir, 'data', 'words.nearby.%d.pklz' % PLT)
_fin_wv_path = os.path.join(curdir, 'data', 'words.vector')
_fin_stopwords_path = os.path.join(curdir, 'data', 'stopwords.txt')


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
    words, tags = [], []
    m = _tokenizer.cut(sen, HMM=True) # HMM更好的识别新词
    for x in m:
        words.append(x.word)
        tags.append(x.flag)
    return words, tags



def similarity_distance(s1,s2):
    '''
    compute similarity
    '''
    sim_molecule = lambda x: np.sum(x, axis=0) # 分子

    def load_wv(model_file, binary):
        if not os.path.exists(model_file):
            print("os.path : ",os.path)
            raise Exception("Model file does not exist.")
        from gensim.models.keyedvectors import KeyedVectors
        return KeyedVectors.load_word2vec_format(model_file, binary=binary, unicode_errors='ignore')

    V = load_wv(model_file=_fin_wv_path, binary=True)
    print('loaded.')

    def set_stopwords():
        global words_set
        words = open(_fin_stopwords_path,'r')
        stopwords = words.readlines()
        words_set = set()
        for w in stopwords:
            words_set.add(w.strip())

    def _vector(sentence):
        vectors = []
        for x,y in enumerate(sentence.split()):
            if y.strip() not in words_set:
                y_ = y.decode('utf-8', errors='ignore').strip()
                syns = nearby(y.strip())[0]
                current = []
                try:
                    current.append(V.word_vec(y_))
                except KeyError,error:
                    current.append(np.zeros((100,),dtype=float))
                for y in syns:
                    if y: # discard word if empty
                        try:
                            v = V.word_vec(y)
                        except KeyError,error:
                            v = np.zeros((100,),dtype=float)
                        current.append(v)
                cur = np.average(current,axis=0)
                vectors.append(cur)
        return vectors

    def unigram_overlap(sentence1, sentence2):
        sen1_set = set(sentence1.split())
        sen2_set = set(sentence2.split())

        sen_intersection = sen1_set & sen2_set
        sen_union = sen1_set | sen2_set

        return ((float)(len(sen_intersection))/(float)(len(sen_union)))

    set_stopwords()
    a = sim_molecule(_vector(s1))
    b = sim_molecule(_vector(s2))
    similarity_nearby = 1/(np.linalg.norm(a - b)+1)
    similarity_unigram =unigram_overlap(s1,s2)
    similarity = similarity_nearby*0.8+similarity_unigram*0.2

    return float("%.3f" % similarity)

def compare(s1, s2, seg = True):
    '''
    compare similarity
    s1 : sentence1
    s2 : sentence2
    seg : True : The original sentences need jieba.cut
          Flase : The original sentences have been cut.
    '''
    assert len(s1) > 0 and len(s2) > 0, "The length of s1 and s2 should > 0."
    if seg:
        s1_ = ' '.join(jieba.cut(s1))
        s2_ = ' '.join(jieba.cut(s2))
        return similarity_distance(s1_,s2_)
    else:
        return similarity_distance(s1,s2)


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
