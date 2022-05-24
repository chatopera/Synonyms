#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Radim Rehurek <me@radimrehurek.com>
# Modifications (C) 2017 Hai Liang Wang <hailiang.hl.wang@gmail.com>
# Licensed under the GNU LGPL v3.0 - http://www.gnu.org/licenses/lgpl.html
# Author: Hai Liang Wang
# Date: 2017-10-16:14:13:24
#
#=========================================================================

from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) (2017-2022) Chatopera Inc. All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2017-10-16:14:13:24"

import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"
else:
    xrange = range

from .utils import smart_open, to_unicode, cosine
from numpy import dot, zeros, dtype, float32 as REAL,\
    double, array, vstack, fromstring, sqrt, newaxis,\
    ndarray, sum as np_sum, prod, ascontiguousarray,\
    argmax
from sklearn.neighbors import KDTree

class Vocab(object):
    """
    A single vocabulary item, used internally for collecting per-word frequency/sampling info,
    and for constructing binary trees (incl. both word leaves and inner nodes).
    """

    def __init__(self, **kwargs):
        self.count = 0
        self.__dict__.update(kwargs)

    def __lt__(self, other):  # used for sorting in a priority queue
        return self.count < other.count

    def __str__(self):
        vals = [
            '%s:%r' %
            (key,
             self.__dict__[key]) for key in sorted(
                self.__dict__) if not key.startswith('_')]
        return "%s(%s)" % (self.__class__.__name__, ', '.join(vals))


class KeyedVectors():
    """
    Class to contain vectors and vocab for the Word2Vec training class and other w2v methods not directly
    involved in training such as most_similar()
    """

    def __init__(self):
        self.syn0 = []
        self.syn0norm = None
        self.vocab = {}
        self.index2word = []
        self.vector_size = None
        self.kdt = None

    @property
    def wv(self):
        return self

    def save(self, *args, **kwargs):
        # don't bother storing the cached normalized vectors
        kwargs['ignore'] = kwargs.get('ignore', ['syn0norm'])
        super(KeyedVectors, self).save(*args, **kwargs)

    @classmethod
    def load_word2vec_format(
            cls,
            fname,
            fvocab=None,
            binary=False,
            encoding='utf8',
            unicode_errors='strict',
            limit=None,
            datatype=REAL):
        """
        Load the input-hidden weight matrix from the original C word2vec-tool format.
        Note that the information stored in the file is incomplete (the binary tree is missing),
        so while you can query for word similarity etc., you cannot continue training
        with a model loaded this way.
        `binary` is a boolean indicating whether the data is in binary word2vec format.
        `norm_only` is a boolean indicating whether to only store normalised word2vec vectors in memory.
        Word counts are read from `fvocab` filename, if set (this is the file generated
        by `-save-vocab` flag of the original C tool).
        If you trained the C model using non-utf8 encoding for words, specify that
        encoding in `encoding`.
        `unicode_errors`, default 'strict', is a string suitable to be passed as the `errors`
        argument to the unicode() (Python 2.x) or str() (Python 3.x) function. If your source
        file may include word tokens truncated in the middle of a multibyte unicode character
        (as is common from the original word2vec.c tool), 'ignore' or 'replace' may help.
        `limit` sets a maximum number of word-vectors to read from the file. The default,
        None, means read all.
        `datatype` (experimental) can coerce dimensions to a non-default float type (such
        as np.float16) to save memory. (Such types may result in much slower bulk operations
        or incompatibility with optimized routines.)
        """
        counts = None
        if fvocab is not None:
            # print("loading word counts from %s" % fvocab)
            counts = {}
            with smart_open(fvocab) as fin:
                for line in fin:
                    word, count = to_unicode(line).strip().split()
                    counts[word] = int(count)

        # print("loading projection weights from %s" % fname)
        with smart_open(fname) as fin:
            header = to_unicode(fin.readline(), encoding=encoding)
            # throws for invalid file format
            vocab_size, vector_size = (int(x) for x in header.split())
            if limit:
                vocab_size = min(vocab_size, limit)
            result = cls()
            result.vector_size = vector_size
            result.syn0 = zeros((vocab_size, vector_size), dtype=datatype)

            def add_word(word, weights):
                word_id = len(result.vocab)
                # print("word id: %d, word: %s, weights: %s" % (word_id, word, weights))
                if word in result.vocab:
                    # print( "duplicate word '%s' in %s, ignoring all but first" % (word, fname))
                    return
                if counts is None:
                    # most common scenario: no vocab file given. just make up
                    # some bogus counts, in descending order
                    result.vocab[word] = Vocab(
                        index=word_id, count=vocab_size - word_id)
                elif word in counts:
                    # use count from the vocab file
                    result.vocab[word] = Vocab(
                        index=word_id, count=counts[word])
                else:
                    # vocab file given, but word is missing -- set count to
                    # None (TODO: or raise?)
                    # print( "vocabulary file is incomplete: '%s' is missing" % word)
                    result.vocab[word] = Vocab(index=word_id, count=None)
                result.syn0[word_id] = weights
                result.index2word.append(word)

            if binary:
                binary_len = dtype(REAL).itemsize * vector_size
                for _ in xrange(vocab_size):
                    # mixed text and binary: read text first, then binary
                    word = []
                    while True:
                        ch = fin.read(1)
                        if ch == b' ':
                            break
                        if ch == b'':
                            raise EOFError(
                                "unexpected end of input; is count incorrect or file otherwise damaged?")
                        # ignore newlines in front of words (some binary files
                        # have)
                        if ch != b'\n':
                            word.append(ch)
                    word = to_unicode(
                        b''.join(word), encoding=encoding, errors=unicode_errors)
                    weights = fromstring(fin.read(binary_len), dtype=REAL)
                    add_word(word, weights)
            else:
                for line_no in xrange(vocab_size):
                    line = fin.readline()
                    if line == b'':
                        raise EOFError(
                            "unexpected end of input; is count incorrect or file otherwise damaged?")
                    parts = to_unicode(
                        line.rstrip(),
                        encoding=encoding,
                        errors=unicode_errors).split(" ")
                    if len(parts) != vector_size + 1:
                        raise ValueError(
                            "invalid vector on line %s (is this really the text format?)" %
                            line_no)
                    word, weights = parts[0], [REAL(x) for x in parts[1:]]
                    add_word(word, weights)
        if result.syn0.shape[0] != len(result.vocab):
            # print( "duplicate words detected, shrinking matrix size from %i to %i" % (result.syn0.shape[0], len(result.vocab)))
            result.syn0 = ascontiguousarray(result.syn0[: len(result.vocab)])
        assert (len(result.vocab), vector_size) == result.syn0.shape
        '''
        KDTree
        Build KDTree with vectors.
        http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html#sklearn.neighbors.KDTree
        '''
        result.kdt = KDTree(result.syn0, leaf_size=10, metric = "euclidean")
        # print("loaded %s matrix from %s" % (result.syn0.shape, fname))
        return result

    def word_vec(self, word, use_norm=False):
        """
        Accept a single word as input.
        Returns the word's representations in vector space, as a 1D numpy array.
        If `use_norm` is True, returns the normalized word vector.
        Example::
          >>> trained_model['office']
          array([ -1.40128313e-02, ...])
        """
        if word in self.vocab:
            if use_norm:
                result = self.syn0norm[self.vocab[word].index]
            else:
                result = self.syn0[self.vocab[word].index]

            result.setflags(write=False)
            return result
        else:
            raise KeyError("word '%s' not in vocabulary" % word)

    def neighbours(self, word, size = 10):
        """
        Get nearest words with KDTree, ranking by cosine distance
        """
        word = word.strip()
        v = self.word_vec(word)
        [distances], [points] = self.kdt.query(array([v]), k = size, return_distance = True)
        assert len(distances) == len(points), "distances and points should be in same shape."
        words, scores = [], {}
        for (x,y) in zip(points, distances):
            w = self.index2word[x]
            if w == word: s = 1.0
            else: s = cosine(v, self.syn0[x])
            if s < 0: s = abs(s)
            words.append(w)
            scores[w] = min(s, 1.0)
        for x in sorted(words, key=scores.get, reverse=True):
            yield x, scores[x]

import unittest

# run testcase: python /Users/hain/tmp/ss Test.testExample


class Test(unittest.TestCase):
    '''

    '''

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_w2v_data(self):
        _fin_wv_path = os.path.join(curdir, 'data', 'words.vector')
        _fin_stopwords_path = os.path.join(curdir, 'data', 'stopwords.txt')
        kv = KeyedVectors()
        binary = True
        kv.load_word2vec_format(
            _fin_wv_path,
            binary=binary,
            unicode_errors='ignore')


def test():
    unittest.main()


if __name__ == '__main__':
    test()
