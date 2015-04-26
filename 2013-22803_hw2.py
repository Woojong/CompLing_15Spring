# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'APD'
__date__ = '2015-04-07'

'''
MLE(Maximum Likelihood Estimation)에 의한 bigram확률(즉 P(news|interesting)과 그냥 bigram 확률(즉 P(interesting news)를,
ComPareBiOutput.txt파일에 작성하는 프로그램을 구현하라. 출력은 확률이 높은 순으로 이루어진다.

출력 형식은
Bigram MLE Prob. Bi Prob
interesting news 0.0003245	0.0000234
.....	...	....

MLE에 기반한 바이그램 확률은 배운대로 조건부 확률을 사용하고 e.g.,) c(interesting news)/c(interesting)
그냥 바이그램 확률은 특정 바이그램의 수를 전체 바이그램의 수로 e.g.,) c(interesting news)/c(total bigram)
MLE에 기반한 바이그램 확률을 구하기 위해서는 각 타입의 유니그램 수도 필요
단어에 붙어 있는 . ", 등 가급적 기호를 제거하고 확률을 구하는게 바람직
'''

#### For checking whether pip installed module exists
pkg = "tabulate"
import imp
try:
    imp.find_module(pkg)
except ImportError:
    from subprocess import call
    call("pip2 install " + pkg, shell=True) # installing a package

#### Importing modules
import os, string
from tabulate import tabulate

#### Setiing file names and directory
curr_dir = os.getcwd() + "\\"
my_dir = "hw2\\"
filename = "BROWN_A1.txt"
savetext = "ComPareBiOutput.txt"

#### Making directory for output file.
if not os.path.exists(curr_dir+my_dir):
    os.makedirs(curr_dir+my_dir)

#### Open and read file
f = open(curr_dir + my_dir + filename, 'r')
data = f.read()
f.close()

#### Clearing punctuation from BROWNA1
word = data.translate(None, string.punctuation).split() # punctuation clearing
word.insert(0, "<s>") # first of sentence
word.insert(len(word), "/<s>") # last of sentence

#### Defining function for making n-gram list
def ngram_maker(data, n_digit, dict=True): #data for word corpus (post-processed), n_digit for the number of "n"-gram
    tmp_ngram = [] #Creating empty temporary n-gram list
    for num in range(len(data)-n_digit+1): # make n-gram list using list type e.g., [['The', 'last'], ['last', 'forever']]
        tmp_ngram.append(data[num:num+n_digit]) # from num to num+n_digit e.g., data[0:2], data[1:3]
    ngram_list = [] # creating empty n-gram list and n-gram dict
    ngram_dict = {}
    for unlist in range(len(tmp_ngram)): # Unlisting n-gram list e.g., ['The last'], ['last forever']
        tmp_words = " ".join(tmp_ngram[unlist]) # join each list elements with " "(space)
        ngram_list.append(tmp_words) # appending n-gram list to joined words
        ngram_dict.setdefault(tmp_words,0) # making default dictionary value for current words or zero
        ngram_dict[tmp_words] += 1 # plus 1 if exist current words
    if dict == True:
        return ngram_dict # returning dictionary
    else:
        return ngram_list # returning list

#### calculating conditional probability defining function
def cond_prob(numer_dict, denom_dict, ngramprob = False): # numer_dict for numerator dictionary, denom_dict for denominator dictionary, ngramprob for n-gram probability not conditional probability
    conditional = {} # initializing conditional probability dictionary
    ngram = {} # initializing n-gram probability dictionary
    total_numer = sum(numer_dict.values())
    for key in numer_dict.keys():
        cur_ngram = key.split() # load ngram dict by dict
        conditional_prob = float(numer_dict[key])/float(denom_dict[" ".join(cur_ngram[:len(cur_ngram)-1])]) # calculating ngram dict probability using c(n-gram)/c((n-1)-gram)
        ngram_prob = float(numer_dict[key])/float(total_numer) # n-gram probability e.g., c(w1 w2)/sum(c(w1 w2))
        conditional[key] = conditional_prob # assigning conditional probability
        ngram[key] = ngram_prob # assigning n-gram probability
    if ngramprob == False:
        return conditional # returing conditiaonl probability
    else:
        return ngram # returning n-gram probability

#### Question
## making n-gram dictionary using defined function
uni_dict = ngram_maker(word,1)
bi_dict = ngram_maker(word,2)
## making probability dictionary
mle_dict = cond_prob(bi_dict, uni_dict)
biprob_dict = cond_prob(bi_dict, uni_dict, True)


result_table = []
header = ["Bigram", "MLE Prob.", "Bi Prob"]
for key, value in sorted(mle_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    result_table.append([key, value, biprob_dict[key]])

w = open(curr_dir + my_dir + savetext, 'w')
w.write(tabulate(result_table, header, floatfmt = ".15f"))
w.close()