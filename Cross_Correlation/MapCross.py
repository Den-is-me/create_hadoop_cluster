#!/usr/bin/python

import sys
import re


for line in sys.stdin:
    d = {}
    line = line.strip().split()
    for word in line:
        word = re.search(r'[a-zA-Z]+', word)
        if word:
            word = word[0]
            for pair in line:
                pair = re.search(r'[a-zA-Z]+', pair)
                if pair:
                    pair = pair[0]
                    if pair != word:
                        d[pair] = d.get(pair, 0) + 1
            if d:
                print(word + '\t' + ','.join([f'{k}:{v}' for k, v in d.items()]))
                d = {}
