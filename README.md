# Hadoop MapReduce jobs
*This repository is designed to store simple MapReduce jobs.*

For testing, I use single machine with Oracle VM Virtual Box, Ubuntu, RAM 4096 mb, 3 CPUs and [the text file of the novel "War and Peace"](/War_and_Peace.txt). Hadoop version 3.3.4
___
## Jobs
- [Word Count](#word-count)
- [TF-IDF](#tf-idf)
## Word Count
This standard job counts how many times each word appears in a text.
First of all, I have created a python API for mapper and reducer:

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
        last_key, sum = key, 0
    else:
        last_key, sum = key, sum + int(value)
if last_key:
    print(last_key + '\t' + str(sum))
```
checked workers with test file
```shell
$ cat ./test.txt | ./MapCount.py | sort | ./ReduceCount.py
```
Then I started hdfs
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
and put the file in dfs.
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
With succsess, the file is in dfs
```shell
$ hdfs dfs -cat /tmp/WordCount/part-00000 | head -n 3
a 10442
aah 1
ab 1
```

As a result we had have [the file](/WordCount) in dfs, which include each word with a count of repetitions.
*Fun fact: the word "peace" is repeated 110 times, while the word "war" is repeated 297 times.*
___
## TF-IDF
### Term Frequency - Inverse Document Frequency is a statistical measure that evaluates how relevant a word is to a document in a collection of documents.

This is done by multiplying two metrics: how many times a word appears in a document, and the inverse document frequency of the word across a set of documents.
