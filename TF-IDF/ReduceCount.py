#!/usr/bin/python
import sys

lk, sum = None, 0

for line in sys.stdin:
    key, value = line.split()
    if lk and lk != key:
        lk = lk.split('#')
        print(f'{lk[0]}\t{lk[1]}\t{str(sum)}')
        lk, sum = key, 1
    else:
        lk, sum = key, sum + 1
if lk:
    lk = lk.split('#')
    print(f'{lk[0]}\t{lk[1]}\t{str(sum)}')
