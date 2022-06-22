#!/usr/bin/env python
"""mapper.py"""

import sys


def perform_map():
    for line in sys.stdin:
        line = line.strip()
        words = line.split(',')[2][:7] + ' ' + line.split(',')[9]
        tip = line.split(',')[13]
        if words[:4] == '2020':

            # for word in words:
            print('%s\t%s' % (words, tip))


if __name__ == '__main__':
    perform_map()


