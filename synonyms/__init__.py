#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/synonyms/__init__.py
# Author: Hai Liang Wang
# Date: 2017-09-27:15:18:36
#
#===============================================================================

"""
Chinese Synonyms for Natural Language Processing and Understanding.
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hu Ying Xi<>, Hai Liang Wang<hailiang.hl.wang@gmail.com>"
__date__      = "2017-09-27:15:18:36"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import gzip
wn_raw_data=gzip.open(os.path.join(curdir, 'data', 'words.nearby.gz'),'rt', encoding='utf-8')

for (k, v) in enumerate(wn_raw_data.readlines()):
    print("index: %s, word: %s" % (k, v))
    if k > 500: break
