__author__ = 'APD'

import re, string

# file name and directory settings
my_dir = "D:\\classes\\2015Spring\\Comp. Ling\\hw1\\"
filename = "BROWN_A1.txt"
savetext = "2013-22803_hw1.txt"

# Open and read file
f = open(my_dir + filename, 'r')
w = open(my_dir + savetext, 'w')
data = f.read()
word = data.translate(None, string.punctuation).split()

# close read text file
f.close()

# 1. 모음으로 시작하고 자음-모음의 연쇄로 끝나는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지
vowel_dict = {}
for i in range(len(word)):
    if re.search(r'^[aeiou][bcdfghjklmnpqrstvwxz][aeiou]', word[i].lower()):
        vowel_dict[word[i]] = (vowel_dict[word[i]] + 1) if word[i] in vowel_dict.keys() else 1
w.write("1. 모음으로 시작하고 자음-모음의 연쇄로 끝나는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지\n")
for key, value in sorted(vowel_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
     w.write ("%r : %r" % (key, value))
     w.write("\n")
w.write("\n")
# w.write(vowel_dict)
# sorted(vowel_dict.values(), reverse = 1)

# 2. r다음에 바로 e가 나오거나, e 다음에 바로 r가 나오는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지
er_dict = {}
for i in range(len(word)):
    if re.search(r're|er', word[i].lower()):
        er_dict[word[i]] = (er_dict[word[i]] + 1) if word[i] in er_dict.keys() else 1
w.write("2. r다음에 바로 e가 나오거나, e 다음에 바로 r가 나오는 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지\n")
for key, value in sorted(er_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
     w.write ("%r : %r" % (key, value))
     w.write("\n")
w.write("\n")
# w.write(er_dict)
# sorted(er_dict.values())

# 3. 순수하게 숫자로 이루어진 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지와 숫자를 포함하고 있는 단어들이 몇 번씩 나오는지와 각각의 단어의 수를 출력하는 프로그램을 작성 .
digit_dict = {}
for i in range(len(word)):
    if re.search(r'^[\d]{1,}$', word[i]):
        digit_dict[word[i]] = (digit_dict[word[i]] + 1) if word[i] in digit_dict.keys() else 1
w.write("3. 순수하게 숫자로 이루어진 단어의 총 개수와 해당 단어들이 각각 몇 번씩 나오는지와 숫자를 포함하고 있는 단어들이 몇 번씩 나오는지와 각각의 단어의 수를 출력하는 프로그램을 작성\n")
for key, value in sorted(digit_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
     w.write ("%r : %r" % (key, value))
     w.write("\n")
w.write("\n")
# w.write(digit_dict)
# sorted(digit_dict.keys())
w.close()