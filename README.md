# Hadoop MapReduce jobs
*This repository is designed to store simple MapReduce jobs.*

For testing, I use single machine with Oracle VM Virtual Box, Ubuntu, RAM 4096 mb, 3 CPUs and [the text file of the novel "War and Peace"](/War_and_Peace.txt). Hadoop version 3.3.4
___
## Jobs
- [Word Count](#word-count)
- [TF-IDF](#tf-idf)
## Word Count
This standard job counts how many times each word appears in a text.
First of all, I have created a python for mapper and reducer in hadoop-streaming:

**MapCount.py**
```python
#!/usr/bin/python

import sys
import re

for line in sys.stdin:
    for i in line.split():
        i = re.search(r'[a-zA-Z]+', i)
        if i:
            print(i[0].lower() + '\t1')
            
```
**ReduceCount.py**
```python
#!/usr/bin/python

import sys

last_key, sum = None, 0

for line in sys.stdin:
    key, value = line.split()
    if last_key and key != last_key:
        print(last_key + '\t' + str(sum))
        last_key, sum = key, 1
    else:
        last_key, sum = key, sum + int(value)
if last_key:
    print(last_key + '\t' + str(sum))
```
checked workers with test file
```shell
$ cat ./test.txt | ./MapCount.py | sort | ./ReduceCount.py
```
Then I started hadoop
```shell
$ start-dfs.sh
$ start-yarn.sh
...
$ jps
14833 Jps
13875 DateNode
14052 SecondaryNameNode
14326 ResourceManager
14446 NodeManager
13759 NameNode
```
and put the file in hdfs.
```shell
$ hdfs dfs -put War_and_Peace.txt /tmp
```
**After that I started the job with hadoop-streaming:**
```shell
$ yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar\
-files MapCount.py,ReduceCount.py\
-input /tmp/War_and_Peace.txt\
-output /tmp/WordCount\
-mapper MapCount.py\
-reducer ReduceCount.py
```
With succsess, the file is in hdfs
```shell
$ hdfs dfs -cat /tmp/WordCount/part-00000 | head -n 3
a 10442
aah 1
ab 1
```

As a result we had have [the file](/Word_Count/WordCount) in hdfs, which include each word with a count of repetitions.
*Fun fact: the word "peace" is repeated 110 times, while the word "war" is repeated 297 times.*
___
## TF-IDF
### Term Frequency - Inverse Document Frequency is a statistical measure that evaluates how relevant a word is to a document in a collection of documents.

This is done by multiplying two metrics: how many times a word appears in a document, and the inverse document frequency of the word across a set of documents.
As set of documents, I used 4 different books in txt format: ['War and Peace'](/War_and_Peace.txt), ['Gone with the wind'](/TF-IDF/Gone_with_the_Wind.txt), ['Harry Potter and philosopher's stone'](/TF-IDF/Harry_Potter_and_PS.txt) and ['Bible'](/TF-IDF/Bible.txt).
The main job consists of 3 phases:
- 'TF' the term frequency of a word in a document. There are several ways of calculating this frequency, with the simplest being a raw count of instances a word appears in a document. Then, there are ways to adjust the frequency, by length of a document, or by the raw frequency of the most frequent word in a document.
- 'IDF' this means, how common or rare a word is in the entire document set. The closer it is to 0, the more common a word is. This metric can be calculated by taking the total number of documents, dividing it by the number of documents that contain a word, and calculating the logarithm.
- Combine the two previous results in the evaluation of TF-IDF words in the document. The higher the score, the more relevant that word is in that particular document.

### Firts phase
I have taken previous Word Count Mapper and Reducer to change them for this task. Because now stdout should be with document's id.

**MapCount.py**

```python
#!/usr/bin/python

import sys
import re
import os

for line in sys.stdin:
    file = os.environ['map_input_file']
    file = re.search(r'\w+[^.txt]', os.path.split(file)[-1])[0]
    for i in line.split():
        i = re.search(r'[a-zA-Z]+', i)
        if i:
            print(i[0].lower() + '#' + file + '\t1')
            
```
**ReduceCount.py**
```python
#!/usr/bin/python

import sys

last_key, sum = None, 0

for line in sys.stdin:
    key, value = line.split()
    if last_key and key != last_key:
        last_key = last_key.split('#')
        print(f'{last_key[0]}\t{last_key[1]}\t{str(sum)}')
        last_key, sum = key, 1
    else:
        last_key, sum = key, sum + 1
if last_key:
    last_key = last_key.split('#')
    print(f'{last_key[0]}\t{last_key[1]}\t{str(sum)}')
    
```
Then I started yarn jar with books that were prepared in hdfs 
```shell
$ yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar\
-files MapCount.py,ReduceCount.py\
-input /tmp/War_and_Peace.txt /tmp/Gone_with_the_Wind.txt /tmp/Harry_Potter_and_PS.txt /tmp/Bible.txt\
-output /tmp/WordCount\
-mapper MapCount.py\
-reducer ReduceCount.py
```
As the result I have had [the WordCount file](/TF-IDF/WordCount) for next phase.

### Second phase
The second step is to give information about how many books a word contains.

[**MapIDF.py**](/TF-IDF/MapIDF.py)
```python
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
```
[**ReduceIDF.py**](/TF-IDF/ReduceIDF.py)
```python
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
        
```

Run hadoop-streaming

```shell
$ yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar\
-files MapIDF.py,ReduceIDF.py\
-input /tmp/WordCount/part-00000\
-output /tmp/IDF/\
-mapper MapIDF.py\
-reducer ReduceIDF.py
```

### Third phase
Finally I took the TF for each word in every book and got TF-IDF with format:
```
word#Book_name  TF-IDF
```
[**MapTF-IDF.py**](/TF-IDF/MapTF-IDF.py)
```python
#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.split()
    word, book = line[0].split('#')
    print(book + '\t' + word + ';' + line[1] + ';' + line[2])
```

[**ReduceTF-IDF.py**](/TF-IDF/ReduceTF-IDF.py)
```python
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
```

Run hadoop-streaming

```shell
$ yarn jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.4.jar\
-files MapTF-IDF.py,ReduceTF-IDF.py\
-input /tmp/IDF/part-00000\
-output /tmp/TF-IDF/\
-mapper MapTF-IDF.py\
-reducer ReduceTF-IDF.py
```
As the result, I received [the TF-IDF file](/TF-IDF/TF-IDF) with these rows:
```shell
lever#War_and_Peace	4.927776346079288e-06
level#War_and_Peace	6.135635915046557e-06
levee#War_and_Peace	6.15972043259911e-06
letting#War_and_Peace	0.0
```
*Fun fact: the most relevant word in War and Peace is 'Wittgenstein', it's a character, he was the commander of a separate corps in the St. Petersburg direction - during the Patriotic War of 1812 *
