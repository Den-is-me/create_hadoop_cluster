#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.split()
    print(f'{line[0]}\t{line[1]};{line[2]};1')

