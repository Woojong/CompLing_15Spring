#!/usr/bin/python
__author__ = 'APD'

import re, string, os

#### Setiing file names and directory
curr_dir = os.getcwd() + "\\"
my_dir = "hw1\\"
filename = "BROWN_A1.txt"
savetext = "2013-22803_hw1.txt"

if not os.path.exists(curr_dir + my_dir):
    os.makedirs(curr_dir + my_dir)

#### Open and read file
f = open(curr_dir + my_dir + filename, 'r')
w = open(curr_dir + my_dir + savetext, 'w')
data = f.read()
# word = data.split()
# clearing punctuation from BROWNA1
word = data.translate(None, string.punctuation).split()


#### Close read text file
f.close()

#### Defining general regular expression function for homework
def find_regex(data, regex,
               file=None):  # data for word corpus as python list type, regex for regular expression for searching specific rule, file for saving result
    tmpdict = {}  # making empty dictionary
    for i in range(len(data)):
        if re.search(r"%s" % regex, data[i].lower()):  # search specific regular expression
            tmpdict[data[i]] = (tmpdict[data[i]] + 1) if data[
                                                             i] in tmpdict.keys() else 1  # if exist exp., then add one count in dictionary
    if file:
        for key, value in sorted(tmpdict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):  # for sorting dictionary
            file.write("%r : %r" % (key, value))  # writing  dictionary
            file.write("\n")
        file.write("\n")
    else:
        for key, value in sorted(tmpdict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
            print "%r : %r" % (key, value)  # for checking processed dictionary

#### Homework questions
w.write("1. 모음으로 시작하고 자음-모음의 연쇄로 끝나는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지\n")
find_regex(word, '^([aeiou]|y[aeiou]).*?([bcdfghjklmnpqrstvwxz][aeiou])$', w)
w.write("2. r다음에 바로 e가 나오거나, e 다음에 바로 r가 나오는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지\n")
find_regex(word, 're|er', w)
w.write("3-1. 순수하게 숫자로 이루어진 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지\n")
find_regex(word, '^[\d]{1,}$', w)
w.write("3-2. 숫자를 포함하고 있는 단어들이 몇 번씩 나오는지\n")
find_regex(word, '[\d][\D]|[\D][\d]', w)
w.close()