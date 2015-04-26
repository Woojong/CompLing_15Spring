# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'APD'
__date__ = '2015-05-05'

'''
과제 4:교차엔트로피(cross entropy)를 통한 언어 모델(Language model) 비교:
(3명까지의 그룹 가능, 5월 6일까지 ETL에 탑재)
sejong.nov.train은 세종코퍼스에서 추출한 소설코퍼스이다. 이 코퍼스에서 자소별, 음절별로 유니그램, 바이그램 언어 모델을 설정하여,
역시 세종코퍼스의 소설 코퍼스인 sejong.nov.test와 한겨레 신문 기사인 hani.test의 교차엔트로피를 계산하여 어느 모델이 더 좋은 모델인지를 살펴보자. (training의 확률을 곱해서, p(x)logm(x))
이를 다음의 테이블을 출력하여 그 결과를 보여라.
(test에서 나타나고 training에서 나타나지 않으면 unknown으로 할 것)
* 모든 파일은 utf8으로 인코딩 되어 있다.
* 자소 분리를 위해서는 다음의 파이선 프로그램을 참조.
* 받침이 없는 글자의 받침을 적절한 문자로 대치하여 처리할 필요
* 각각의 코퍼스는 하나의 긴 문장으로 생각
# 한글 character인지 확인하는 코드, 즉 한글 자모 외엔 모두 무시
'''

#### Setiing file names and directory
curr_dir = os.getcwd() + "\\"
my_dir = "hw4\\"
filename = ["haniTest.txt", "sejong.nov.test.txt", "sejong.nov.train.txt"]
savetext = "Output.txt"


import codecs, os, sys
sys.path.append(curr_dir+my_dir) # for loading hangulDecoder in my_dir
from hangulDecoder import isHangulSyllable, decodeSyllable


#### Making directory for output file.
if not os.path.exists(curr_dir+my_dir):
    os.makedirs(curr_dir+my_dir)

#### Open and read file
f = codecs.open(curr_dir + my_dir + filename[0], "r", "utf-8")
test1 = f.read()
f = codecs.open(curr_dir + my_dir + filename[1], "r", "utf-8")
test2 = f.read()
f = codecs.open(curr_dir + my_dir + filename[2], "r", "utf-8")
train = f.read()
f.close()

#### Filtering only hangul syllable
def onlyHangul(data):
    tmp_list = []
    for syllable in data:
        if isHangulSyllable(syllable):
            tmp_list.append(syllable)
    return tmp_list

#### Hangul syllable to Hangul jamo (e.g., 한글 > ㅎ ㅏ ㄴ ㄱ ㅡ ㄹ)
def sylTojamo(syllable_list): # syllable to jamo
    tmp_list = []
    for tmp_syl in syllable_list:
        if not isHangulSyllable(tmp_syl):
            tmp_list.append(tmp_syl) # if it is not a hangul syllable, it will be assigned original unicode
        else:
            for decoded in decodeSyllable(tmp_syl): # decoding hangul syllable
                tmp_list.append(decoded)
    return tmp_list

def UNK_process(traindata, testdata):
    keylist = testdata.keys()
    for keys in keylist:
        try:
            traindata[keys]
        except:
            testdata[u"<UNK>"] = testdata[u"<UNK>"]+1 if u"<UNK>" in testdata.keys() else 1
            print keys
    return testdata

def entropy_compute(data, crossdata): # if you using cross entropy, data for training data, crossdata for test data, if you want to just entropy calculating, then data and crossdata for same data set (e.g., data = test, crossdata = test)
    from math import log
    def log2(x): # for using log base 2 as function
        return log(x, 2)
    entropy_dict = {}
    data_keylist = data.keys()
    for keylist in data_keylist:
        entropy_dict[keylist] = data[keylist]*log2(crossdata[keylist])
    return entropy_dict

test1_syllable = onlyHangul(test1)
test2_syllable = onlyHangul(test2)
train_syllable = onlyHangul(train)

test1_jamo = sylTojamo(test1_syllable)
test2_jamo = sylTojamo(test2_syllable)
train_jamo = sylTojamo(train_syllable)

from compling_NLP import ngram_maker, cond_prob
test1_unijamo_dict = ngram_maker(test1_jamo, 1)
test1_bijamo_dict = ngram_maker(test1_jamo, 2)
test1_unisyl_dict = ngram_maker(test1_syllable, 1)
test1_bisyl_dict = ngram_maker(test1_syllable, 2)
test2_unijamo_dict = ngram_maker(test2_jamo, 1)
test2_bijamo_dict = ngram_maker(test2_jamo, 2)
test2_unisyl_dict = ngram_maker(test2_syllable, 1)
test2_bisyl_dict = ngram_maker(test2_syllable, 2)
train_unijamo_dict = ngram_maker(train_jamo, 1)
train_bijamo_dict = ngram_maker(train_jamo, 2)
train_unisyl_dict = ngram_maker(train_syllable, 1)
train_bisyl_dict = ngram_maker(train_syllable, 2)

uniprob = cond_prob(train_unisyl_dict, [], True)
biprob = cond_prob(train_bisyl_dict, train_unisyl_dict)