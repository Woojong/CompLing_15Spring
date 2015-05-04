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
savetext = "Output.htm"
if not os.path.exists(curr_dir+my_dir):
    os.makedirs(curr_dir+my_dir)
sys.path.append(curr_dir+my_dir) # for loading hangulDecoder in my_dir
from hangulDecoder import isHangulSyllable, decodeSyllable

#### Open and read file
f = codecs.open(curr_dir + my_dir + filename[0], "r", "utf-8")
train = f.read()
train = "<s>" + train + "</s>"
f = codecs.open(curr_dir + my_dir + filename[1], "r", "utf-8")
test1 = f.read()
test1 = "<s>" + test1 + "</s>"
f = codecs.open(curr_dir + my_dir + filename[2], "r", "utf-8")
test2 = f.read()
test2 = "<s>" + test2 + "</s>"
f.close()

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
    if ngramprob == False:
        for key in numer_dict.keys():
            cur_ngram = key.split() # load ngram dict by dict
            conditional_prob = float(numer_dict[key])/float(denom_dict[" ".join(cur_ngram[:len(cur_ngram)-1])]) # calculating ngram dict probability using c(n-gram)/c((n-1)-gram)
            conditional[key] = conditional_prob # assigning conditional probability
        return conditional # returing conditiaonl probability
    else:
        for key in numer_dict.keys():
            ngram_prob = float(numer_dict[key])/float(total_numer) # n-gram probability e.g., c(w1 w2)/sum(c(w1 w2))
            ngram[key] = ngram_prob # assigning n-gram probability
        return ngram # returning n-gram probability

#### Filtering only hangul syllable
def onlyHangul(data):
    tmp_list = []
    for syllable in data:
        if isHangulSyllable(syllable): #only hangul syllable append to list
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
def UNK_process(traindata, testdata, testngram): # traindata for training probability data, testdata for test probability data, trainngram for training n-gram dictionary, testgram for test n-gram dictionary
    total_unk = 0 # setting UNK probability as 0
    test_nvocab = sum(testngram.values()) # total trainngram token
    for keys in testdata.keys():# extracting test data probability dictionary keys
        try:
            traindata[keys]
        except: # if exist only in test data, then save unk and calculate unk probability
            total_unk = total_unk + testngram[keys]
    unk_prob = float(total_unk)/float(test_nvocab)
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

# including only hangule
test1_syllable = onlyHangul(test1)
test2_syllable = onlyHangul(test2)
train_syllable = onlyHangul(train)

# convert syllable (eumjeol) to jamo
test1_jamo = sylTojamo(test1_syllable)
test2_jamo = sylTojamo(test2_syllable)
train_jamo = sylTojamo(train_syllable)

# making unigram and bigram with test, training data
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

# calculating MLE probability
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

# entropy calculating
unisyl_entropy = entropy_compute(train_unisylprob, train_unisylprob, dict = False)
bisyl_entropy = entropy_compute(train_bisylprob, train_bisylprob, dict = False)
test1_unisyl_entropy = entropy_compute(test1_unisylprob, test1_unisylprob, dict = False)
test2_unisyl_entropy = entropy_compute(test2_unisylprob, test2_unisylprob, dict = False)
test1_bisyl_entropy = entropy_compute(test1_bisylprob, test1_bisylprob, dict = False)
test2_bisyl_entropy = entropy_compute(test2_bisylprob, test2_bisylprob, dict = False)

# calculating <UNK> probability
train1_unisyl_unkprob = UNK_process(train_unisylprob, test1_unisylprob, test1_unisyl_dict)
train2_unisyl_unkprob = UNK_process(train_unisylprob, test2_unisylprob, test2_unisyl_dict)
train1_bisyl_unkprob = UNK_process(train_bisylprob, test1_bisylprob, test1_bisyl_dict)
train2_bisyl_unkprob = UNK_process(train_bisylprob, test2_bisylprob, test2_bisyl_dict)

# calculating cross entropy with train set
unisyl1_cross_ent = entropy_compute(test1_unisylprob, train_unisylprob, train1_unisyl_unkprob, dict = False)
unisyl2_cross_ent = entropy_compute(test2_unisylprob, train_unisylprob, train2_unisyl_unkprob, dict = False)
bisyl1_cross_ent = entropy_compute(test1_bisylprob, train_bisylprob, train1_bisyl_unkprob, dict = False)
bisyl2_cross_ent = entropy_compute(test2_bisylprob, train_bisylprob, train2_bisyl_unkprob, dict = False)

# jamo entropy
unijamo_entropy = entropy_compute(train_unijamoprob, train_unijamoprob, dict = False)
bijamo_entropy = entropy_compute(train_bijamoprob, train_bijamoprob, dict = False)
test1_unijamo_entropy = entropy_compute(test1_unijamoprob, test1_unijamoprob, dict = False)
test2_unijamo_entropy = entropy_compute(test2_unijamoprob, test2_unijamoprob, dict = False)
test1_bijamo_entropy = entropy_compute(test1_bijamoprob, test1_bijamoprob, dict = False)
test2_bijamo_entropy = entropy_compute(test2_bijamoprob, test2_bijamoprob, dict = False)

# unk probability calculation
train1_unijamo_unkprob = UNK_process(train_unijamoprob, test1_unijamoprob, test1_unijamo_dict)
train2_unijamo_unkprob = UNK_process(train_unijamoprob, test2_unijamoprob, test2_unijamo_dict)
train1_bijamo_unkprob = UNK_process(train_bijamoprob, test1_bijamoprob, test1_bijamo_dict)
train2_bijamo_unkprob = UNK_process(train_bijamoprob, test2_bijamoprob, test2_bijamo_dict)

# jamo cross entropy
unijamo1_cross_ent = entropy_compute(test1_unijamoprob, train_unijamoprob, train1_unijamo_unkprob, dict = False)
unijamo2_cross_ent = entropy_compute(test2_unijamoprob, train_unijamoprob, train2_unijamo_unkprob, dict = False)
bijamo1_cross_ent = entropy_compute(test1_bijamoprob, train_bijamoprob, train1_bijamo_unkprob, dict = False)
bijamo2_cross_ent = entropy_compute(test2_bijamoprob, train_bijamoprob, train2_bijamo_unkprob, dict = False)

#### output entropy and cross-entropy as html files
import pandas as pd # import library pandas
df = pd.DataFrame({"Corpus": ["Sejong.nov.Traning", "", "", "", "Sejong.nov.test", "","","","Hani.test","","",""],
                  "Unit": [codecs.decode("자소별", "utf-8"), "", codecs.decode("음절별", "utf-8"), ""]*3,
                 "Model": ["uni-gram", "bi-gram"]*6,
                  "Entropy": [unijamo_entropy, bijamo_entropy, unisyl_entropy, bisyl_entropy, test1_unijamo_entropy, test1_bijamo_entropy, test1_unisyl_entropy, test1_bisyl_entropy, test2_unijamo_entropy, test2_bijamo_entropy, test2_unisyl_entropy, test2_bisyl_entropy],
                 "CrossEntropy": ["", "", "", "", unijamo1_cross_ent, bijamo1_cross_ent, unisyl1_cross_ent, bisyl1_cross_ent, unijamo2_cross_ent, bijamo2_cross_ent, unisyl2_cross_ent, bisyl2_cross_ent],
                  "Difference": ["", "", "", "", test1_unijamo_entropy-unijamo1_cross_ent, test1_bijamo_entropy-bijamo1_cross_ent, test1_unisyl_entropy-unisyl1_cross_ent, test1_bisyl_entropy-bisyl1_cross_ent, test2_unijamo_entropy-unijamo2_cross_ent, test2_bijamo_entropy-bijamo2_cross_ent, test2_unisyl_entropy-unisyl2_cross_ent, test2_bisyl_entropy-bisyl2_cross_ent]
                  })
df = df[["Corpus", "Unit", "Model", "Entropy", "CrossEntropy", "Difference"]] # reorganization of data frame

w = codecs.open(curr_dir+my_dir+savetext, 'w', 'utf-8') # save as htm files
w.write(df.to_html())
w.close()