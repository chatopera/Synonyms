#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=========================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/synonyms/__init__.py
# Author: Hai Liang Wang
# Date: 2017-09-27
#
#=========================================================================

"""
Chinese Synonyms for Natural Language Processing and Understanding.
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__ = "Hu Ying Xi<>, Hai Liang Wang<hailiang.hl.wang@gmail.com>"
__date__ = "2017-09-27"


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

import json
import gzip
import shutil
from synonyms.word2vec import KeyedVectors
from synonyms.utils import any2utf8
from synonyms.utils import any2unicode
from synonyms.utils import sigmoid
import jieba.posseg as _tokenizer
import jieba

'''
globals
'''
_vocab = dict()
_size = 0
_vectors = None
_stopwords = set()

'''
nearby
'''
def _load_vocab(file_path):
    '''
    load vocab dict
    '''
    global _vocab
    if PLT == 2:
        import io
        fin = io.TextIOWrapper(
            io.BufferedReader(
                gzip.open(file_path)),
            encoding='utf8',
            errors='ignore')
    else:
        fin = gzip.open(file_path, 'rt', encoding='utf-8', errors="ignore")

    _vocab = json.loads(fin.read())

# build on load
print(">> Synonyms on loading vocab ...")
_load_vocab(os.path.join(curdir, "data", "words.nearby.json.gz"))

def nearby(word):
    '''
    Nearby word
    '''
    try:
        return _vocab[any2unicode(word)]
    except KeyError as e:
        return [[], []]


'''
similarity
'''

# stopwords
_fin_stopwords_path = os.path.join(curdir, 'data', 'stopwords.txt')
def _load_stopwords(file_path):
    '''
    load stop words
    '''
    global _stopwords
    if sys.version_info[0] < 3:
        words = open(file_path, 'r')
    else:
        words = open(file_path, 'r', encoding='utf-8')
    stopwords = words.readlines()
    for w in stopwords:
        _stopwords.add(any2unicode(w).strip())

print(">> Synonyms on loading stopwords ...")
_load_stopwords(_fin_stopwords_path)

def _segment_words(sen):
    '''
    segment words with jieba
    '''
    words, tags = [], []
    m = _tokenizer.cut(sen, HMM=True)  # HMM更好的识别新词
    for x in m:
        words.append(x.word)
        tags.append(x.flag)
    return words, tags

# vectors
_f_model = os.path.join(curdir, 'data', 'words.vector')
def _load_w2v(model_file=_f_model, binary=True):
    '''
    load word2vec model
    '''
    if not os.path.exists(model_file):
        print("os.path : ", os.path)
        raise Exception("Model file does not exist.")
    return KeyedVectors.load_word2vec_format(
        model_file, binary=binary, unicode_errors='ignore')
print(">> Synonyms on loading vectors ...")
_vectors = _load_w2v(model_file=_f_model)

_sim_molecule = lambda x: np.sum(x, axis=0)  # 分子

def _get_wv(sentence):
    '''
    get word2vec data by sentence
    sentence is segmented string.
    '''
    global _vectors
    vectors = []
    for y in sentence:
        y_ = any2unicode(y).strip()
        if y_ not in _stopwords:
            syns = nearby(y_)[0]
            # print("sentence %s word: %s" %(sentence, y_))
            # print("sentence %s word nearby: %s" %(sentence, " ".join(syns)))
            c = []
            try:
                c.append(_vectors.word_vec(y_))
            except KeyError as error:
                print("not exist in w2v model: %s" % y_)
                # c.append(np.zeros((100,), dtype=float))
                random_state = np.random.RandomState(seed=(hash(y_) % (2**32 - 1)))
                c.append(random_state.uniform(low=-10.0, high=10.0, size=(100,)))
            for n in syns:
                if n is None: continue
                try:
                    v = _vectors.word_vec(any2unicode(n))
                except KeyError as error:
                    # v = np.zeros((100,), dtype=float)
                    random_state = np.random.RandomState(seed=(hash(n) % (2 ** 32 - 1)))
                    v = random_state.uniform(low=10.0, high=10.0, size=(100,))
                c.append(v)
            r = np.average(c, axis=0)
            vectors.append(r)
    return vectors


def _unigram_overlap(sentence1, sentence2):
    '''
    compute unigram overlap
    '''
    x = set(sentence1.split())
    y = set(sentence2.split())

    intersection = x & y
    union = x | y

    return ((float)(len(intersection)) / (float)(len(union)))

def _levenshtein_distance(sentence1, sentence2):
    '''
    Return the Levenshtein distance between two strings.
    Based on:
        http://rosettacode.org/wiki/Levenshtein_distance#Python
    '''
    first = any2utf8(sentence1).decode('utf-8', 'ignore')
    second = any2utf8(sentence2).decode('utf-8', 'ignore')
    sentence1_len, sentence2_len = len(first), len(second)
    maxlen = max(sentence1_len, sentence2_len)
    if sentence1_len > sentence2_len:
        first, second = second, first

    distances = range(len(first) + 1)
    for index2, char2 in enumerate(second):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(first):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1],
                                             distances[index1 + 1],
                                             new_distances[-1])))
        distances = new_distances
    levenshtein = distances[-1]
    d = float((maxlen - levenshtein)/maxlen)
    # smoothing
    s = (sigmoid(d * 6) - 0.5) * 2
    # print("smoothing[%s| %s]: %s -> %s" % (sentence1, sentence2, d, s))
    return s

def _nearby_levenshtein_distance(s1, s2):
    '''
    使用
    '''
    s1_len = len(s1)
    s2_len = len(s2)
    maxlen = max(s1_len, s2_len)
    first, second = (s2, s1) if s1_len == maxlen else (s1, s2)
    ft = set() # all related words with first sentence 
    for x in first:
        ft.add(x)
        n, _ = nearby(x)
        for o in n:
            ft.add(o)
    scores = []
    if len(ft) == 0: return 0.0 # invalid length for first string
    for x in second:
        scores.append(max([_levenshtein_distance(x, y) for y in ft]))
    s = np.sum(scores) / maxlen
    return s

# combine similarity scores
_similarity_smooth = lambda x, y, z: (x * y) + z

def _similarity_distance(s1, s2):
    '''
    compute similarity with distance measurement
    '''
    a = _sim_molecule(_get_wv(s1))
    b = _sim_molecule(_get_wv(s2))
    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.norm.html
    g = 1 / (np.linalg.norm(a - b) + 1)

    u = _nearby_levenshtein_distance(s1, s2)
    # print("g: %s, u: %s" % (g, u))
    if u > 0.8:
        r = _similarity_smooth(g, 1, u)
    elif u > 0.7:
        r = _similarity_smooth(g, 1.5, u)
    elif u > 0.6:
        r = _similarity_smooth(g, 2, u)
    else:
        r = _similarity_smooth(g, 4, u)

    r = min(r, 1.0)
    return float("%.3f" % r)

def compare(s1, s2, seg=True):
    '''
    compare similarity
    s1 : sentence1
    s2 : sentence2
    seg : True : The original sentences need jieba.cut
          Flase : The original sentences have been cut.
    '''
    if seg:
        s1 = [x for x in jieba.cut(s1)]
        s2 = [x for x in jieba.cut(s2)]
    else:
        s1 = s1.split()
        s2 = s2.split()
    assert len(s1) > 0 and len(s2) > 0, "The length of s1 and s2 should > 0."

    return _similarity_distance(s1, s2)

def display(word):
    print("'%s'近义词：" % word)
    o = nearby(word)
    assert len(o) == 2, "should contain 2 list"
    if len(o[0]) == 0:
        print(" out of vocabulary")
    for k, v in enumerate(o[0]):
        print("  %d. %s:%s" % (k + 1, v, o[1][k]))

def main():
    display("人脸")
    display("NOT_EXIST")


if __name__ == '__main__':
    main()
