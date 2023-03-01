#!/usr/bin/python

my_max = []
with open('TF-IDF', 'r', encoding='UTF-8') as file:
    for i in list(file):
        i = i.strip().split()
        word, book = i[0].split('#')
        if book == 'War_and_Peace':
            my_max.append([word, i[1]])
print(sorted(my_max, key=lambda x: (x[1], x[0]), reverse=True)[:10])

