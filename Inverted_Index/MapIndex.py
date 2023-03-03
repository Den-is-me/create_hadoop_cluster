#!/usr/bin/python

import sys
import re
import os

for line in sys.stdin:
    file = os.environ['map_input_file']
    file = os.path.split(file)[-1]
    for j in line.split():
        j = re.search(r'[a-zA-Z]+', j)
        if j:
            print(j[0].lower() + '\t'  + file)

