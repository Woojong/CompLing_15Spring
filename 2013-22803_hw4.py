# -*- coding: utf-8 -*-
#!/usr/bin/python
__author__ = 'APD'
__date__ = '2015-05-05'

'''
과제 4:교차엔트로피(cross entropy)를 통한 언어 모델(Language model) 비교:
(3명까지의 그룹 가능, 5월 6일까지 ETL에 탑재)
sejong.nov.train은 세종코퍼스에서 추출한 소설코퍼스이다. 이 코퍼스에서 자소별, 음절별로 유니그램, 바이그램 언어 모델을 설정하여,
역시 세종코퍼스의 소설 코퍼스인 sejong.nov.test와 한겨레 신문 기사인 hani.test의 교차엔트로피를 계산하여 어느 모델이 더 좋은 모델인지를 살펴보자.
(training의 확률을 곱해서, p(x)logm(x))
이를 다음의 테이블을 출력하여 그 결과를 보여라.
(test에서 나타나고 training에서 나타나지 않으면 unknown으로 할 것)
* 모든 파일은 utf8으로 인코딩 되어 있다.
* 자소 분리를 위해서는 다음의 파이선 프로그램을 참조.
* 받침이 없는 글자의 받침을 적절한 문자로 대치하여 처리할 필요
* 각각의 코퍼스는 하나의 긴 문장으로 생각
# 한글 character인지 확인하는 코드, 즉 한글 자모 외엔 모두 무시
'''

#### Setiing file names and directory
import codecs, os, sys
#### Making directory for output file.
curr_dir = os.getcwd() + "\\"
my_dir = "hw4\\"
filename = ["sejong.nov.train.txt", "sejong.nov.test.txt", "haniTest.txt"]
savetext = "Output.txt"
if not os.path.exists(curr_dir+my_dir):
    os.makedirs(curr_dir+my_dir)
sys.path.append(curr_dir+my_dir) # for loading hangulDecoder in my_dir
from hangulDecoder import isHangulSyllable, decodeSyllable

#### Open and read file
f = codecs.open(curr_dir + my_dir + filename[0], "r", "utf-8")
train = f.read()
f = codecs.open(curr_dir + my_dir + filename[1], "r", "utf-8")
test1 = f.read()
f = codecs.open(curr_dir + my_dir + filename[2], "r", "utf-8")
test2 = f.read()
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

#### Converting unseen words in trainig data to <UNK>
def UNK_process(traindata, testdata, trainngram, testngram): # traindata for training probability data, testdata for test probability data, trainngram for training n-gram dictionary, testgram for test n-gram dictionary
    keylist = testdata.keys() # extracting test data probability dictionary keys
    total_unk = 0 # setting UNK probability as 0
    train_nvocab = sum(trainngram.values())
    for keys in keylist:
        try:
            traindata[keys]
        except:
            total_unk = total_unk + testngram[keys] if u"<UNK>" in trainngram.keys() else testngram[keys]
    unk_prob = float(total_unk)/float(train_nvocab)
    return unk_prob

#### Computing entropy (and cross entropy, if you want entroypy: "data == crossdata", cross entropy: "data != crossdata")
def entropy_compute(data, crossdata, unkprob = None, dict = True): # if you using cross entropy, data for training data, crossdata for test data, if you want to just entropy calculating, then data and crossdata for same data set (e.g., data = test, crossdata = test)
    from math import log # for using log base 2 as function
    def log2(x):
        return log(x, 2)
    entropy_dict = {} # empty entropy dictionary
    data_keylist = data.keys() # extract data dictionary keys
    for keylist in data_keylist:
        try:
            entropy_dict[keylist] = data[keylist]*log2(crossdata[keylist]) # p*log_2(p)
        except:
            entropy_dict[keylist] = data[keylist]*log2(unkprob) # if don't exist intraining data, then UNK probability which was computed already
    entropy_values = sum(entropy_dict.values()) # summation of entropy of data
    if dict:
        return entropy_dict
    elif dict == False:
        return entropy_values

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


train_unisylprob = cond_prob(train_unisyl_dict, [], True)
train_bisylprob = cond_prob(train_bisyl_dict, train_unisyl_dict)
train_unijamoprob = cond_prob(train_unijamo_dict, [], True)
train_bijamoprob = cond_prob(train_bijamo_dict, train_unijamo_dict)
test1_unisylprob = cond_prob(test1_unisyl_dict, [], True)
test1_bisylprob = cond_prob(test1_bisyl_dict, test1_unisyl_dict)
test1_unijamoprob = cond_prob(test1_unijamo_dict, [], True)
test1_bijamoprob = cond_prob(test1_bijamo_dict, test1_unijamo_dict)
test2_unisylprob = cond_prob(test2_unisyl_dict, [], True)
test2_bisylprob = cond_prob(test2_bisyl_dict, test2_unisyl_dict)
test2_unijamoprob = cond_prob(test2_unijamo_dict, [], True)
test2_bijamoprob = cond_prob(test2_bijamo_dict, test2_unijamo_dict)

unisyl_entropy = entropy_compute(train_unisylprob, train_unisylprob, dict = False)
bisyl_entropy = entropy_compute(train_bisylprob, train_bisylprob, dict = False)
test1_unisyl_entropy = entropy_compute(test1_unisylprob, test1_unisylprob, dict = False)
test2_unisyl_entropy = entropy_compute(test2_unisylprob, test2_unisylprob, dict = False)
test1_bisyl_entropy = entropy_compute(test1_bisylprob, test1_bisylprob, dict = False)
test2_bisyl_entropy = entropy_compute(test2_bisylprob, test2_bisylprob, dict = False)
train1_unisyl_unkprob = UNK_process(train_unisylprob, test1_unisylprob, train_unisyl_dict, test1_unisyl_dict)
unisyl1_cross_ent = entropy_compute(test1_unisylprob, train_unisylprob, train1_unisyl_unkprob, dict = False)
train2_unisyl_unkprob = UNK_process(train_unisylprob, test2_unisylprob, train_unisyl_dict, test2_unisyl_dict)
unisyl2_cross_ent = entropy_compute(test2_unisylprob, train_unisylprob, train2_unisyl_unkprob, dict = False)
train1_bisyl_unkprob = UNK_process(train_bisylprob, test1_bisylprob, train_bisyl_dict, test1_bisyl_dict)
bisyl1_cross_ent = entropy_compute(test1_bisylprob, train_bisylprob, train1_bisyl_unkprob, dict = False)
train2_bisyl_unkprob = UNK_process(train_bisylprob, test2_bisylprob, train_bisyl_dict, test2_bisyl_dict)
bisyl2_cross_ent = entropy_compute(test2_bisylprob, train_bisylprob, train2_bisyl_unkprob, dict = False)

unijamo_entropy = entropy_compute(train_unijamoprob, train_unijamoprob, dict = False)
bijamo_entropy = entropy_compute(train_bijamoprob, train_bijamoprob, dict = False)
test1_unijamo_entropy = entropy_compute(test1_unijamoprob, test1_unijamoprob, dict = False)
test2_unijamo_entropy = entropy_compute(test2_unijamoprob, test2_unijamoprob, dict = False)
test1_bijamo_entropy = entropy_compute(test1_bijamoprob, test1_bijamoprob, dict = False)
test2_bijamo_entropy = entropy_compute(test2_bijamoprob, test2_bijamoprob, dict = False)
train1_unijamo_unkprob = UNK_process(train_unijamoprob, test1_unijamoprob, train_unijamo_dict, test1_unijamo_dict)
unijamo1_cross_ent = entropy_compute(test1_unijamoprob, train_unijamoprob, train1_unijamo_unkprob, dict = False)
train2_unijamo_unkprob = UNK_process(train_unijamoprob, test2_unijamoprob, train_unijamo_dict, test2_unijamo_dict)
unijamo2_cross_ent = entropy_compute(test2_unijamoprob, train_unijamoprob, train2_unijamo_unkprob, dict = False)
train1_bijamo_unkprob = UNK_process(train_bijamoprob, test1_bijamoprob, train_bijamo_dict, test1_bijamo_dict)
bijamo1_cross_ent = entropy_compute(test1_bijamoprob, train_bijamoprob, train1_bijamo_unkprob, dict = False)
train2_bijamo_unkprob = UNK_process(train_bijamoprob, test2_bijamoprob, train_bijamo_dict, test2_bijamo_dict)
bijamo2_cross_ent = entropy_compute(test2_bijamoprob, train_bijamoprob, train2_bijamo_unkprob, dict = False)

import pandas as pd
df = pd.DataFrame({"Corpus": ["Sejong.nov.Traning", "", "", "", "Sejong.nov.test", "","","","Hani.test","","",""],
                  "Unit": [codecs.decode("자소별", "utf-8"), "", codecs.decode("음절별", "utf-8"), ""]*3,
                 "Model": ["uni-gram", "bi-gram"]*6,
                  "Entropy": [unijamo_entropy, bijamo_entropy, unisyl_entropy, bisyl_entropy, test1_unijamo_entropy, test1_bijamo_entropy, test1_unisyl_entropy, test1_bisyl_entropy, test2_unijamo_entropy, test2_bijamo_entropy, test2_unisyl_entropy, test2_bisyl_entropy],
                 "CrossEntropy": ["", "", "", "", unijamo1_cross_ent, bijamo1_cross_ent, unisyl1_cross_ent, bisyl1_cross_ent, unijamo2_cross_ent, bijamo2_cross_ent, unisyl2_cross_ent, bisyl2_cross_ent],
                  "Difference": ["", "", "", "", test1_unijamo_entropy-unijamo1_cross_ent, test1_bijamo_entropy-bijamo1_cross_ent, test1_unisyl_entropy-unisyl1_cross_ent, test1_bisyl_entropy-bisyl1_cross_ent, test2_unijamo_entropy-unijamo2_cross_ent, test2_bijamo_entropy-bijamo2_cross_ent, test2_unisyl_entropy-unisyl2_cross_ent, test2_bisyl_entropy-bisyl2_cross_ent]
                  })
df = df[["Corpus", "Unit", "Model", "Entropy", "CrossEntropy", "Difference"]]
df.to_csv('C:\\Users\\APD\\Desktop\\Output.csv', sep = ',', encoding = 'utf-8')
print df