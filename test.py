__author__ = 'APD'
__date__ = '2015-03-10'
# -*- coding: utf-8 -*-
import re, codecs

# alpha_re = re.compile('([a-z]+). ([0-9]+)')
alpha_re = re.compile('([a-z]+)')
line = 'There are 5 apples, 14 fish, 1 orange.'
# print(line)
line = line.lower()
result = alpha_re.search(line) #string에서 pattern을 찾아서 matchOBJ 반환
result.group()
result_all = alpha_re.findall(line)
if alpha_re:
    print result.group(0)

for i in range(len(result_all)):
    if i <= len(result_all):
        print result_all[i], result_all[i+1]

D = {'food': 'Spam', 'quantity': 4, 'color': 'pink'}

f = codecs.open('C:\Users\APD\Desktop\\test.txt', 'r', 'utf-8')
f_readline = f.readlines()
for i in f_readline:
    print i