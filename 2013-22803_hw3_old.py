# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'APD'
__date__ = '2015-04-14'


'''
과제 3: BROWN_A1, BROWN_F1 코퍼스를 이용하여  'he was there  to take complaint about this course" 이라는 문장의 확률을 출력하는 프로그램을 작성하라.
각각의 bigram을 구해서 markov assumption
log scale로 곱해서 구하는게 나음 underflow
comma, exclamation, 등을 어떻게 처리하였는지 아닌지 주석에 달 것
개별 문장의 확률
힌트:

(1) 각 문장 앞에 <s> (문장시작), 문장 뒤에 </s>(문장 끝)이라는 표시를 넣을 수 있으면 넣고 바이그램을 구성하라. 할 수 없다면 전체를 하나의 긴 연쇄로 해서 바이그램 구성
(2) ", ' 등 모든 기호를 다 별도의 토큰으로 간주하라. 따라서 "을 과 같은 어휘에서도 별도의 space를 넣든지 하여 space를 기준으로 tokenize할 때 적절히 처리될 수 있도록 하여야 한다.
(3) 프로그램 출력은 http://word.snu.ac.kr/ngram/ 에 있는 프로그램처럼 Simple Bigram, Add-one Smoothing, Good-Turing의 결과를 위 예시 문장의 BIgram Counts, Bigram Probability 테이블 그리고 위 문장의 확률을 보여라.

(Due 4월 14일 수업시간 전까지 etl에 탑재)
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
import os, string, re
from tabulate import tabulate
from math import log, exp

#### Setiing file names and directory
curr_dir = os.getcwd() + "\\"
my_dir = "hw3\\"
filename = ["BROWN_A1.txt", "BROWN1_F1.txt"]
savetext = "ComPareBiOutput.txt"

#### Making directory for output file.
if not os.path.exists(curr_dir+my_dir):
    os.makedirs(curr_dir+my_dir)

#### Open and read file
num = 1
data_list = []
for file in filename:
    f = open(curr_dir + my_dir + file, 'r')
    exec("data{0} = f.readlines()" .format(num))
    data_list.append("data{0}" .format(num))
    f.close()
    num += 1
del num, file

data = []
for curlist in data_list:
    data += eval(curlist)
del data_list, curlist

word = []
for lines in data:
    lines = re.sub(r"([!\"#$%&\'()*+,-./:;<=>?@\[\]^_`{|}~])", r" \1 ", lines) # wrap around punctuation
    lines = re.sub(r"\s{2,}", r" ", lines) # replacing double space to single space e.g., "  " to " "
    lines = "<s> " + lines + " </s>" # adding <s>, </s> begining and end of sentence
    word.extend(lines.split())
del lines

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

#### Add-one smoothing (or laplace smoothing)
def addone_smooth(raw_dict, corpus, ngram = 1, prob = True): # raw_dict for raw data dictionary, corpus for denominator dictionary e.g., unigram dictionary
    """:type: dict[int, set[int]]"""
    tmp_dict = {}
    tmp_probdict = {}
    for curdict in raw_dict:
        tmp_dict[curdict] = raw_dict[curdict] + 1
    for curdict in tmp_dict:
        tmp_probdict[curdict] = float(tmp_dict[curdict]) / float(corpus[curdict.split()[:ngram]]+len(corpus))
    if prob:
        return tmp_probdict
    else:
        return tmp_dict

#### Good Turing smoothing
def GT_smooth(f_target_dict, raw_dict, threshold = 5, f_freq = False): # f_target_dict for targeting dictonary, threshold for the number of discount range (default is 5), raw_dict for reference corpus or bigram dictionary,  f_freq for returning frequency of frequency
    ## making frequency of frequency table
    freq_list = list(set(raw_dict.values())) # Unique values
    freq_dict = {} # frequency of frequency
    freq_dict[0] = len(raw_dict)**2 - sum(raw_dict.values()) # for the total number of bigram - having seen bigram (e.g., V^2 - all bigram)
    for freq in freq_list:
        freq_dict[freq] = raw_dict.values().count(freq)
    gt_prob = []
    for gt_digit in range(threshold+1):
        gt_prob.append((gt_digit+1) * float(freq_dict[gt_digit+1]) / float(freq_dict[gt_digit]))
    target_count = {}
    for target in f_target_dict:
        for mod_count in range(len(gt_prob)):
            if f_target_dict[target] == mod_count:
                target_count[target] = gt_prob[mod_count]
    for target in f_target_dict:
        if target not in target_count:
            target_count[target] = f_target_dict[target]
    if f_freq:
        return freq_dict
    else:
        return target_count

#making bigram and unigram dictionary and bigram probability
bi_dict = ngram_maker(word, 2)
uni_dict = ngram_maker(word, 1)
bi_mleprob = cond_prob(bi_dict, uni_dict)

# target_sentence = "<s> he was there to be able to take the first step </s>"
target_sentence = "<s> he was there to take complaint about this course </s>"
target_word = target_sentence.split()
target_list = ngram_maker(target_word, 2, False)
target_dict = ngram_maker(target_word, 2)
for target in target_list:
    target_dict[target] = bi_dict[target] if target in bi_dict else 0

target_probdict = cond_prob(target_dict, uni_dict)
try:
    sum([log(x) for x in target_probdict.values()])
except:
    sentence_prob = 0
target_count_ONEs = addone_smooth(target_dict, uni_dict, 1, False)
target_probdict_ONEs = addone_smooth(target_dict, uni_dict, 1, True)
sentence_One_prob = exp(sum([log(x) for x in target_probdict_ONEs.values()]))
target_count_GTs = GT_smooth(target_dict, bi_dict, 5, False)
target_probdict_GTs = cond_prob(GT_smooth(target_dict, bi_dict, 5, False), uni_dict)
sentence_GT_prob = exp(sum([log(x) for x in target_probdict_GTs.values()]))




def dict_assort(sort_dict):
    result_table = []
    for key, value in sorted(sort_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
        result_table.append([key, value])
    return result_table


def dict_assort(sort_dict):
    result_table = []
    for lists in target_list:
        result_table.append([lists, sort_dict[lists]])
    return result_table

w = open(curr_dir + my_dir + savetext, 'w')
w.write("Simple bigram count\n")
header = ["Bigram", "Simple bigram count"]
w.write(tabulate(dict_assort(target_dict), header, floatfmt = ".15f"))
w.write("\n")
w.write("Simple bigram probability\n")
header = ["Bigram", "Simple bigram probability"]
w.write(tabulate(dict_assort(target_probdict), header, floatfmt = ".15f"))
w.write("\n")
w.write("Simple bigram sentence probability = {0}\n" .format(sentence_prob))
w.write("\n")

w.write("Laplace smoothing bigram count\n")
header = ["Bigram", "Laplace bigram count"]
w.write(tabulate(dict_assort(target_count_ONEs), header, floatfmt = ".15f"))
w.write("\n")
w.write("Laplace smoothing bigram probability\n")
header = ["Bigram", "Laplace bigram probability"]
w.write(tabulate(dict_assort(target_probdict_ONEs), header, floatfmt = ".15f"))
w.write("\n")
w.write("Laplace smoothing bigram sentence probability = {0}\n" .format(sentence_One_prob))
w.write("\n")

w.write("Good-Turing smoothing bigram count\n")
header = ["Bigram", "Good-Turing bigram count"]
w.write(tabulate(dict_assort(target_count_GTs), header, floatfmt = ".15f"))
w.write("\n")
w.write("GT bigram probability\n")
header = ["Bigram", "GT bigram probability"]
w.write(tabulate(dict_assort(target_probdict_GTs), header, floatfmt = ".15f"))
w.write("\n")
w.write("GT bigram sentence probability = {0}\n" .format(sentence_GT_prob))
w.close()



