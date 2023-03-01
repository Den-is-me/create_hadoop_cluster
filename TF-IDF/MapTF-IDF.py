#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.split()
    word, book = line[0].split('#')
    print(book + '\t' + word + ';' + line[1] + ';' + line[2])

