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

__copyright__ = "Copyright (c) (2017-2022) Chatopera Inc. All Rights Reserved"
__author__ = "Hu Ying Xi<>, Hai Liang Wang<hai@chatopera.com>"
__date__ = "2020-09-24"
__version__ = "3.18.0"

import os
import sys
import numpy as np
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, curdir)

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

# Get Environment variables
ENVIRON = os.environ.copy()

import json
import gzip
import shutil
from .word2vec import KeyedVectors
from .utils import any2utf8
from .utils import any2unicode
from .utils import sigmoid
from .utils import cosine
from .utils import is_digit
from jieba import posseg, analyse
import wget

'''
globals
'''
_vocab = dict()
_size = 0
_vectors = None
_stopwords = set()
_cache_nearby = dict()
_debug = False

if "SYNONYMS_DEBUG" in ENVIRON:
    if ENVIRON["SYNONYMS_DEBUG"].lower() == "true": _debug = True

'''
lambda fns
'''
# combine similarity scores
_similarity_smooth = lambda x, y, z, u: (x * y) + z - u
_flat_sum_array = lambda x: np.sum(x, axis=0)  # 分子
_logging_debug = lambda x: print(">> Synonyms DEBUG %s" % x) if _debug else None

'''
Sponsorship
'''
print("\n Synonyms: v%s, Project home: %s" % (__version__, "https://github.com/chatopera/Synonyms/"))
print("\n Project Sponsored by Chatopera")
print("\n  deliver your chatbots with Chatopera Cloud Services --> https://bot.chatopera.com\n")

'''
tokenizer settings
'''
tokenizer_dict = os.path.join(curdir, 'data', 'vocab.txt')
if "SYNONYMS_WORDSEG_DICT" in ENVIRON:
    if os.path.exists(ENVIRON["SYNONYMS_WORDSEG_DICT"]):
        print("info: set wordseg dict with %s" % tokenizer_dict)
        tokenizer_dict = ENVIRON["SYNONYMS_WORDSEG_DICT"]
    else: print("warning: can not find dict at [%s]" % tokenizer_dict)

print(">> Synonyms load wordseg dict [%s] ... " % tokenizer_dict)
posseg.initialize(tokenizer_dict)

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

print(">> Synonyms on loading stopwords [%s] ..." % _fin_stopwords_path)
_load_stopwords(_fin_stopwords_path)

def _segment_words(sen, HMM=True):
    '''
    segment words
    '''
    words, tags = [], []
    m = posseg.cut(sen, HMM=HMM)  # HMM更好的识别新词
    for x in m:
        words.append(x.word)
        tags.append(x.flag)
    return words, tags

def keywords(sentence, topK=5, withWeight=False, allowPOS=()):
    '''
    extract keywords with Jieba Tokenizer
    '''
    return analyse.extract_tags(sentence, topK=topK, withWeight=withWeight, allowPOS=allowPOS)

'''
word embedding
'''
# vectors
## Model File on GitHub https://github.com/chatopera/Synonyms/releases/download/3.15.0/words.vector.gz
## Model File on Gitee, Default.
SYNONYMS_WORD2VEC_BIN_URL_ZH_CN = "https://gitee.com/chatopera/cskefu/attach_files/610602/download/words.vector.gz"
_f_url = os.environ.get("SYNONYMS_WORD2VEC_BIN_URL_ZH_CN", SYNONYMS_WORD2VEC_BIN_URL_ZH_CN)
_f_model = os.path.join(curdir, 'data', 'words.vector.gz')
_download_model = not os.path.exists(_f_model)
if "SYNONYMS_WORD2VEC_BIN_MODEL_ZH_CN" in ENVIRON:
    _f_model = ENVIRON["SYNONYMS_WORD2VEC_BIN_MODEL_ZH_CN"]
    _download_model = False

def _load_w2v(model_file=_f_model, binary=True):
    '''
    load word2vec model
    '''
    if not os.path.exists(model_file) and _download_model:
        print("\n>> Synonyms downloading data from %s to %s ... \n this only happens if SYNONYMS_WORD2VEC_BIN_URL_ZH_CN is not present and Synonyms initialization for the first time. \n It would take minutes that depends on network." % (_f_url, model_file))
        wget.download(_f_url, out = model_file)
        print("\n>> Synonyms downloaded.\n")
    elif not os.path.exists(model_file):
        print(">> Synonyms os.path : ", os.path)
        raise Exception("Model file [%s] does not exist." % model_file)

    return KeyedVectors.load_word2vec_format(
        model_file, binary=binary, unicode_errors='ignore')
print(">> Synonyms on loading vectors [%s] ..." % _f_model)
_vectors = _load_w2v(model_file=_f_model)

def _get_wv(sentence, ignore=False):
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
            _logging_debug("sentence %s word: %s" %(sentence, y_))
            _logging_debug("sentence %s word nearby: %s" %(sentence, " ".join(syns)))
            c = []
            try:
                c.append(_vectors.word_vec(y_))
            except KeyError as error:
                if ignore:
                    continue
                else:
                    _logging_debug("not exist in w2v model: %s" % y_)
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

'''
Distance
'''
# Levenshtein Distance
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

def sv(sentence, ignore=False):
    '''
    获得一个分词后句子的向量，向量以BoW方式组成
    sentence: 句子是分词后通过空格联合起来
    ignore: 是否忽略OOV，False时，随机生成一个向量
    '''
    return _get_wv(sentence, ignore = ignore)


def v(word):
    '''
    获得一个词语的向量，OOV时抛出 KeyError 异常
    '''
    y_ = any2unicode(word).strip()
    return _vectors.word_vec(y_)

def _nearby_levenshtein_distance(s1, s2):
    '''
    使用空间距离近的词汇优化编辑距离计算
    '''
    s1_len, s2_len = len(s1), len(s2)
    maxlen = s1_len
    if s1_len == s2_len:
        first, second = sorted([s1, s2])
    elif s1_len < s2_len:
        first = s1
        second = s2
        maxlen = s2_len
    else:
        first = s2
        second = s1

    ft = set() # all related words with first sentence 
    for x in first:
        ft.add(x)
        n, _ = nearby(x)
        for o in n[:10]:
            ft.add(o)
    
    scores = []
    for x in second:
        choices = [_levenshtein_distance(x, y) for y in ft]
        if len(choices) > 0: scores.append(max(choices))

    s = np.sum(scores) / maxlen if len(scores) > 0 else 0
    return s

def _similarity_distance(s1, s2, ignore):
    '''
    compute similarity with distance measurement
    '''
    g = 0.0
    try:
        g_ = cosine(_flat_sum_array(_get_wv(s1, ignore)), _flat_sum_array(_get_wv(s2, ignore)))
        if is_digit(g_): g = g_
    except: pass

    u = _nearby_levenshtein_distance(s1, s2)
    if u >= 0.99:
        r = 1.0
    elif u > 0.9:
        r = _similarity_smooth(g, 0.05, u, 0.05)
    elif u > 0.8:
        r = _similarity_smooth(g, 0.1, u, 0.2)
    elif u > 0.4:
        r = _similarity_smooth(g, 0.2, u, 0.15)
    elif u > 0.2:
        r = _similarity_smooth(g, 0.3, u, 0.1)
    else:
        r = _similarity_smooth(g, 0.4, u, 0)

    if r < 0: r = abs(r)
    r = min(r, 1.0)
    return float("%.3f" % r)

'''
Public Methods
'''
seg = _segment_words # word segmenter

def nearby(word, size = 10):
    '''
    Nearby word
    '''
    w = any2unicode(word)
    wk = w + '-' + str(size)
    # read from cache
    if wk in _cache_nearby: return _cache_nearby[wk]

    words, scores = [], []
    try:
        for x in _vectors.neighbours(w, size):
            words.append(x[0])
            scores.append(x[1])
    except: pass # ignore key error, OOV
    # put into cache
    _cache_nearby[wk] = (words, scores)
    return words, scores

def compare(s1, s2, seg=True, ignore=False, stopwords=False):
    '''
    compare similarity
    s1 : sentence1
    s2 : sentence2
    seg : True : The original sentences need be cut
          False : The original sentences have been cut
    ignore: True: ignore OOV words
            False: get vector randomly for OOV words
    '''
    if s1 == s2: return 1.0
    
    s1_words = []
    s2_words = []

    if seg:
        s1, _ = _segment_words(s1)
        s2, _ = _segment_words(s2)
    else:
        s1 = s1.split()
        s2 = s2.split()

    # check stopwords
    if not stopwords:
        global _stopwords
        for x in s1: 
            if not x in _stopwords:
                s1_words.append(x)
        for x in s2:
            if not x in _stopwords:
                s2_words.append(x)
    else:
        s1_words = s1 
        s2_words = s2

    assert len(s1) > 0 and len(s2) > 0, "The length of s1 and s2 should > 0."
    return _similarity_distance(s1_words, s2_words, ignore)

def describe():
    '''
    summary info of vectors
    '''
    vocab_size = len(_vectors.vocab.keys())
    print("Vocab size in vector model: %d" % vocab_size)
    print("model_path: %s" % _f_model)
    print("version: %s" % __version__)
    return dict({
        "vocab_size": vocab_size,
        "version": __version__,
        "model_path": _f_model
    })

def display(word, size = 10):
    print("'%s'近义词：" % word)
    o = nearby(word, size)
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
