#!/usr/bin/python
import sys

d = []
last_key = None

for line in sys.stdin:
    key, value = line.split()
    v1, v2 = value.split(';')[:2]
    if last_key and last_key != key:
        for i in d:
             print(last_key + '#' + "\t".join(i) + '\t' + str(len(d)))
        last_key = key
        d = [[v1, v2]]
    else:
        last_key = key
        d.append([v1, v2])
if last_key:
    for i in d:
        print(last_key + '#' + "\t".join(i) + '\t' + str(len(d)))
