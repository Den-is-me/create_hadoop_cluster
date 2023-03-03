#!/usr/bin/python

import sys

last_word, words_in_books = None, set()
for line in sys.stdin:
    word, book = line.split('\t')
    if last_word and word != last_word:
        print(last_word + '\t' +  ';'.join(list(words_in_books)))
        last_word, words_in_books = word, set()
        words_in_books.add(book)
    else:
        last_word = word
        words_in_books.add(book)
if last_word:
     print(last_word + '\t' + ';'.join(list(words_in_books)))
