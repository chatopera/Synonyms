#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=========================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/Synonyms/benchmark.py
# Author: Hai Liang Wang
# Date: 2017-10-21:11:26:53
#
#=========================================================================

"""

"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2017-10-21:11:26:53"


import os
import sys
import platform
import multiprocessing
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

import timeit

print("\nEnumerating Available System Resources...")

print("\n++++++++++ OS Name and version ++++++++++")

print("Platform:", platform.system())
print("Kernel:", platform.release())
print("Distro:", platform.linux_distribution())
print("Architecture:", platform.architecture())

print("\n++++++++++ CPU Cores ++++++++++")
p = os.popen("ps aux|awk 'NR > 0{s +=$3};END{print s}'").read()
print("Cores:", multiprocessing.cpu_count(), '\nCPU Load:', p)

print("\n++++++++++ System Memory ++++++++++\n")


def meminfo():
    meminfo = dict()

    with os.popen('cat /proc/meminfo') as f:
        for line in f:
            meminfo[line.split(':')[0]] = line.split(':')[1].strip()
    return meminfo


try:
    meminfo = meminfo()
    print('Total Memory: {0}'.format(meminfo['MemTotal']))
    print('Free Memory: {0}'.format(meminfo['MemFree']))
except BaseException:
    print("meminfo unavailable")


def main():
    repeat = 3
    number = 100000
    unit = "usec"  # 微秒
    unittosec = {"usec": 1e6, "msec": 1000, "sec": 1}
    result = timeit.repeat(
        "synonyms.nearby('人脸')",
        "import synonyms",
        number=number,
        repeat=repeat)
    print("%s: %d loops, best of %d epochs: %.3g %s per loop" %
          ("synonyms#nearby", number, repeat,
           min(result) / number * unittosec[unit], unit))


if __name__ == '__main__':
    main()
