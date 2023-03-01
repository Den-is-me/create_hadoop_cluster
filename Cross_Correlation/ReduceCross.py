#!/usr/bin/python
import sys

last_word = '!'
d = {}

for line in sys.stdin:
    word, keys = line.split()
    if last_word and word != last_word:
        for i in d.keys():
            print(last_word + '#' + i + '\t' + str(d[i]))
        last_word = word
        d = {}
    else:
        for pair in keys.split(','):
            pair = pair.split(':')
            d[pair[0]] = d.get(pair[0], 0) + int(pair[1])
        last_word = word
if last_word:
    for i in d.keys():
        print(last_word + '#' + i + '\t' + str(d[i]))
