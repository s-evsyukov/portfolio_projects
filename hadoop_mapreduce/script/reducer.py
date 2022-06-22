#!/usr/bin/env python
"""reducer.py"""

import sys


def perform_reduce():
    current_word = None
    current_tip = 0
    word = None
    arr = {}
    avg = 0.0

    for line in sys.stdin:
        line = line.strip()
        word, tip = line.split('\t', 1)
        try:
            tip = float(tip)
        except ValueError:
            pass

        if word in arr:
            arr[word] = (float(arr[word][0] + tip), arr[word][1] + 1)
        else:
            arr[word] = (tip, 1)

    for key, v in arr.items():
        try:
            avg = round(float(v[0] / v[1]), ndigits=2)
        except:
            pass

        print('%s\t%s' % (key, avg))


if __name__ == '__main__':
    perform_reduce()
