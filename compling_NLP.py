# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'APD'
__copyright__ = "Copyrights by Woojong, Yi for Computational Lingustics class (2015 spring)"
__version__ = "1.0.1"

"""
2015-04-24 added hangul syllable to jamo
2015-04-14 added good-turing smoothing
2015-04-11 added add-one smoothing
2015-04-07 added n-gram maker and conditioanl probability
"""

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
    if ngramprob:
        for key in numer_dict.keys():
            ngram_prob = float(numer_dict[key])/float(total_numer) # n-gram probability e.g., c(w1 w2)/sum(c(w1 w2))
            ngram[key] = ngram_prob # assigning n-gram probability
        return ngram # returning n-gram probability
    elif not ngramprob:
        for key in numer_dict.keys():
            cur_ngram = key.split() # load ngram dict by dict
            conditional_prob = float(numer_dict[key])/float(denom_dict[" ".join(cur_ngram[:len(cur_ngram)-1])]) # calculating ngram dict probability using c(n-gram)/c((n-1)-gram)
            conditional[key] = conditional_prob # assigning conditional probability
        return conditional # returing conditiaonl probability

#### Add-one smoothing (or laplace smoothing)
def addone_smooth(raw_dict, corpus, ngram = 1, prob = True): # raw_dict for raw data dictionary, corpus for denominator dictionary e.g., unigram dictionary
    tmp_dict = {} # for count dictionary
    tmp_probdict = {} # for probability dictionary
    for curdict in raw_dict:
        tmp_dict[curdict] = raw_dict[curdict] + 1 # add 1 dictonary count
    for curdict in tmp_dict:
        tmp_probdict[curdict] = float(tmp_dict[curdict]) / float(corpus[curdict.split()[ngram-1]]+len(corpus)) # smoothed dictionary probability
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
    gt_prob = [] # frequency of frequency probability
    for gt_digit in range(threshold+1):
        gt_prob.append((gt_digit+1) * float(freq_dict[gt_digit+1]) / float(freq_dict[gt_digit])) # c* = (c+1)*n_c+1/n+c
    ## for counting dictionary
    target_count = {}
    for target in f_target_dict: # replacing target dictionary count
        for mod_count in range(len(gt_prob)): # modified count
            if f_target_dict[target] == mod_count:
                target_count[target] = gt_prob[mod_count]
    for target in f_target_dict: # replacing target dictionary count into
        if target not in target_count: # out of threshold range dictionary count, assign original count
            target_count[target] = f_target_dict[target]
    if f_freq:
        return freq_dict # returning frequency of frequency dictionary
    else:
        return target_count # returning target dictionary replace good turing discount

#### Sorting dictionary to target sentence order
def dict_assort(sort_dict): # for sorting result as target sentence order
    result_table = []
    for lists in sort_dict:
        result_table.append([lists, sort_dict[lists]])
    return result_table

#### Hnagul syllable to Hangul jamo (e.g., 한글 > ㅎ ㅏ ㄴ ㄱ ㅡ ㄹ)
from hangulDecoder import isHangulSyllable, decodeSyllable # requiring for checking hangul and decoding syllable
def sylTojamo(syllable_list): # syllable to jamo
    tmp_list = []
    for tmp_syl in syllable_list:
        if not isHangulSyllable(tmp_syl):
            tmp_list.append(tmp_syl) # if it is not a hangul syllable, it will be assigned original unicode
        else:
            for decoded in decodeSyllable(tmp_syl): # decoding hangul syllable
                tmp_list.append(decoded)
    return tmp_list

#### UNK processor
def UNK_process(traindata, testdata):
    keylist = testdata.keys()
    for keys in keylist:
        try:
            traindata[keys]
        except:
            testdata[u"<UNK>"] = testdata[u"<UNK>"]+1 if u"<UNK>" in testdata.keys() else 1
            print keys
    return testdata

#### Entropy calculation
def entropy_compute(data, crossdata): # if you using cross entropy, data for training data, crossdata for test data, if you want to just entropy calculating, then data and crossdata for same data set (e.g., data = test, crossdata = test)
    from math import log
    def log2(x): # for using log base 2 as function
        return log(x, 2)
    entropy_dict = {}
    data_keylist = data.keys()
    for keylist in data_keylist:
        entropy_dict[keylist] = data[keylist]*log2(crossdata[keylist])
    return entropy_dict