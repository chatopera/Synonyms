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

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2017-10-16:14:13:24"

import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

import re
import unicodedata
import os
import random
import shutil
import sys
import subprocess
from contextlib import contextmanager
import numpy as np
import numbers
from six import string_types, u

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"
else:
    unicode = str

import collections
import warnings

try:
    from html.entities import name2codepoint as n2cp
except ImportError:
    from htmlentitydefs import name2codepoint as n2cp
try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle


try:
    from smart_open import smart_open
except ImportError:
    print("smart_open library not found; falling back to local-filesystem-only")

    def make_closing(base, **attrs):
        """
        Add support for `with Base(attrs) as fout:` to the base class if it's missing.
        The base class' `close()` method will be called on context exit, to always close the file properly.

        This is needed for gzip.GzipFile, bz2.BZ2File etc in older Pythons (<=2.6), which otherwise
        raise "AttributeError: GzipFile instance has no attribute '__exit__'".

        """
        if not hasattr(base, '__enter__'):
            attrs['__enter__'] = lambda self: self
        if not hasattr(base, '__exit__'):
            attrs['__exit__'] = lambda self, type, value, traceback: self.close()
        return type('Closing' + base.__name__, (base, object), attrs)

    def smart_open(fname, mode='rb'):
        _, ext = os.path.splitext(fname)
        if ext == '.bz2':
            from bz2 import BZ2File
            return make_closing(BZ2File)(fname, mode)
        if ext == '.gz':
            from gzip import GzipFile
            return make_closing(GzipFile)(fname, mode)
        return open(fname, mode)


PAT_ALPHABETIC = re.compile(r'(((?![\d])\w)+)', re.UNICODE)
RE_HTML_ENTITY = re.compile(r'&(#?)([xX]?)(\w{1,8});', re.UNICODE)


def get_random_state(seed):
    """
    Turn seed into a np.random.RandomState instance.
    Method originally from maciejkula/glove-python, and written by @joshloyal.
    """
    if seed is None or seed is np.random:
        return np.random.mtrand._rand
    if isinstance(seed, (numbers.Integral, np.integer)):
        return np.random.RandomState(seed)
    if isinstance(seed, np.random.RandomState):
        return seed
    raise ValueError(
        '%r cannot be used to seed a np.random.RandomState instance' %
        seed)


class NoCM(object):
    def acquire(self):
        pass

    def release(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass


nocm = NoCM()


@contextmanager
def file_or_filename(input):
    """
    Return a file-like object ready to be read from the beginning. `input` is either
    a filename (gz/bz2 also supported) or a file-like object supporting seek.

    """
    if isinstance(input, string_types):
        # input was a filename: open as file
        yield smart_open(input)
    else:
        # input already a file-like object; just reset to the beginning
        input.seek(0)
        yield input


def deaccent(text):
    """
    Remove accentuation from the given string. Input text is either a unicode string or utf8 encoded bytestring.

    Return input string with accents removed, as unicode.

    >>> deaccent("Šéf chomutovských komunistů dostal poštou bílý prášek")
    u'Sef chomutovskych komunistu dostal postou bily prasek'

    """
    if not isinstance(text, unicode):
        # assume utf8 for byte strings, use default (strict) error handling
        text = text.decode('utf8')
    norm = unicodedata.normalize("NFD", text)
    result = u('').join(ch for ch in norm if unicodedata.category(ch) != 'Mn')
    return unicodedata.normalize("NFC", result)


def copytree_hardlink(source, dest):
    """
    Recursively copy a directory ala shutils.copytree, but hardlink files
    instead of copying. Available on UNIX systems only.
    """
    copy2 = shutil.copy2
    try:
        shutil.copy2 = os.link
        shutil.copytree(source, dest)
    finally:
        shutil.copy2 = copy2


def tokenize(
        text,
        lowercase=False,
        deacc=False,
        encoding='utf8',
        errors="strict",
        to_lower=False,
        lower=False):
    """
    Iteratively yield tokens as unicode strings, removing accent marks
    and optionally lowercasing the unidoce string by assigning True
    to one of the parameters, lowercase, to_lower, or lower.

    Input text may be either unicode or utf8-encoded byte string.

    The tokens on output are maximal contiguous sequences of alphabetic
    characters (no digits!).

    >>> list(tokenize('Nic nemůže letět rychlostí vyšší, než 300 tisíc kilometrů za sekundu!', deacc = True))
    [u'Nic', u'nemuze', u'letet', u'rychlosti', u'vyssi', u'nez', u'tisic', u'kilometru', u'za', u'sekundu']

    """
    lowercase = lowercase or to_lower or lower
    text = to_unicode(text, encoding, errors=errors)
    if lowercase:
        text = text.lower()
    if deacc:
        text = deaccent(text)
    return simple_tokenize(text)


def simple_tokenize(text):
    for match in PAT_ALPHABETIC.finditer(text):
        yield match.group()


def simple_preprocess(doc, deacc=False, min_len=2, max_len=15):
    """
    Convert a document into a list of tokens.

    This lowercases, tokenizes, de-accents (optional). -- the output are final
    tokens = unicode strings, that won't be processed any further.

    """
    tokens = [
        token for token in tokenize(doc, lower=True, deacc=deacc, errors='ignore')
        if min_len <= len(token) <= max_len and not token.startswith('_')
    ]
    return tokens


def any2utf8(text, errors='strict', encoding='utf8'):
    """Convert a string (unicode or bytestring in `encoding`), to bytestring in utf8."""
    if isinstance(text, unicode):
        return text.encode('utf8')
    # do bytestring -> unicode -> utf8 full circle, to ensure valid utf8
    return unicode(text, encoding, errors=errors).encode('utf8')


to_utf8 = any2utf8


def any2unicode(text, encoding='utf8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)


to_unicode = any2unicode

# cosine distance
# https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.linalg.norm.html
from numpy import dot
from numpy.linalg import norm
cosine = lambda a, b: dot(a, b)/(norm(a)*norm(b))

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def call_on_class_only(*args, **kwargs):
    """Raise exception when load methods are called on instance"""
    raise AttributeError('This method should be called on a class object.')

def is_digit(obj):
    '''
    Check if an object is Number
    '''
    return isinstance(obj, (numbers.Integral, numbers.Complex, numbers.Real))

def is_zhs(str):
    '''
    Check if str is Chinese Word
    '''
    for i in str:
        if not is_zh(i):
            return False
    return True

def is_zh(ch):
    """return True if ch is Chinese character.
    full-width puncts/latins are not counted in.
    """
    x = ord(ch)
    # CJK Radicals Supplement and Kangxi radicals
    if 0x2e80 <= x <= 0x2fef:
        return True
    # CJK Unified Ideographs Extension A
    elif 0x3400 <= x <= 0x4dbf:
        return True
    # CJK Unified Ideographs
    elif 0x4e00 <= x <= 0x9fbb:
        return True
    # CJK Compatibility Ideographs
    elif 0xf900 <= x <= 0xfad9:
        return True
    # CJK Unified Ideographs Extension B
    elif 0x20000 <= x <= 0x2a6df:
        return True
    else:
        return False

def is_punct(ch):
    x = ord(ch)
    # in no-formal literals, space is used as punctuation sometimes.
    if x < 127 and ascii.ispunct(x):
        return True
    # General Punctuation
    elif 0x2000 <= x <= 0x206f:
        return True
    # CJK Symbols and Punctuation
    elif 0x3000 <= x <= 0x303f:
        return True
    # Halfwidth and Fullwidth Forms
    elif 0xff00 <= x <= 0xffef:
        return True
    # CJK Compatibility Forms
    elif 0xfe30 <= x <= 0xfe4f:
        return True
    else:
        return False