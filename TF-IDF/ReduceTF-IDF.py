#!/usr/bin/python
import sys
from math import log

d = []
last_key = None
total_words = 0
num_books = 4
for line in sys.stdin:
    key, value = line.split()
    word, count, w_in_b = value.split(';')
    if last_key and key != last_key:
        for i in d:
            TF = int(i[1]) / total_words
            TF_IDF = TF * log(num_books / int(i[2]))
            print(i[0] + '#' + last_key + '\t' + str(TF_IDF))
        d, last_key, total_words = [], key, int(count)
    else:
        d.append([word, count, w_in_b])
        last_key = key
        total_words += int(count)

if last_key:
    for i in d:
        TF = int(i[1]) / total_words
        TF_IDF = TF * log(num_books / int(i[2]))
        print(i[0] + '#' + last_key + '\t' + str(TF_IDF))
