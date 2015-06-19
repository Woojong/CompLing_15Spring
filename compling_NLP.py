# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'APD'
__copyright__ = "Copyrights by Woojong, Yi for Computational Lingustics class (2015 spring)"
__version__ = "1.0.1"

"""
2015-06-19 added Viterbi algorithm and emission, transition probability
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

#### Filtering only hangul syllable
def onlyHangul(data):
    tmp_list = []
    for syllable in data:
        if isHangulSyllable(syllable):
            tmp_list.append(syllable)
    return tmp_list

#### Hangul syllable to Hangul jamo (e.g., 한글 > ㅎ ㅏ ㄴ ㄱ ㅡ ㄹ)
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

def emission_dict_word(data, tag_list, sep = '/'): # data for tagged corpus set, i.e., training data, and tag_list for all the tag list
    emis_dict = dict((i,{}) for i in tag_list if i != "<START>") # excepting start of sentenece symbols
    for elem in data:
        try: # add dictionary values
            if elem != "<START>" and elem != "<END>":
                tmp_word = elem.split(sep)[0] # word (c.f., "the/dt" -> ["the", "at"][0]
                tmp_tag = elem.split(sep)[1]  # tag (c.f., "the/dt" -> ["the", "at"][1]
                emis_dict[tmp_word][tmp_tag] += 1
        except: # dictionary initialization
            tmp_word = elem.split(sep)[0]
            tmp_tag = elem.split(sep)[1]
            emis_dict[tmp_word].setdefault(tmp_tag,1)
    return emis_dict

def emission_prob_word(data, tag_ngram): # data for tagged corpus set, i.e., training data, and tag_ngram for tag trasition ngram
    emis_prob = dict((i,{}) for i in data.keys()) # excepting start of sentenece symbols
    for word in data.keys():
        for tag in data[word]:
            emis_prob[word][tag] = float(data[word][tag])/float(tag_ngram[tag]) # C(word|tag)/C(tag)
    return emis_prob

def transition_dict(data): # data for tagged corpus set
    ntrial=0
    trans_dict = dict((i,{}) for i in data)
    for elem in data:
        try:
            tag = data[ntrial+1]
            trans_dict[elem][tag] += 1
        except:
            tag = data[ntrial+1]
            trans_dict[elem].setdefault(tag,1)
        ntrial+=1
        if ntrial >= len(data)-1:
            break
    return trans_dict

def transition_prob(data, denom):
    trans_prob = dict((i,{}) for i in data)
    for elem in data.keys():
        for tag in data[elem].keys():
            trans_prob[elem][tag] = float(data[elem][tag])/float(denom[elem])
    return trans_prob


def viterbi(observation, transition_p, emission_p): # viterbi algorithms
    prev_prob = 0
    tagged_result = []
    ## initial pos of start sentence##
    for lines in observation: # firstly, processing viterbi decoder line by line
        lines = lines.split() # splitting line to word  list
        initial_phase = transition_p['<START>'] # start of sentence processing
        tagged_sentence = [] # result sentence (tagged sentence after algorithm) initialization
        for word in range(len(lines)):
            try:
                pairs = {} # possible probability and tag dictionary initialization
                if lines[word] != "<START>":
                    for emiss in emission_p[lines[word]]:
                        try:
                            pairs[emiss] = emission_p[lines[word]][emiss]*initial_phase[emiss] # possible probability pairs (e.g., [tag, prob]
                        except: continue
                    tag = pairs.keys()[pairs.values().index(max(pairs.values()))] # find maximum probability
                    prev_prob = pairs[tag] # save as previous viterbi probability
                    tagged_sentence.append(lines[word] + "/" + tag) # tagging sentence
                    cur_phase = transition_p[tag] # transition probability phase
                    trans_tag = cur_phase.keys()[cur_phase.values().index(max(cur_phase.values()))] #find maximum prob
                    trans_tag_prob = cur_phase[trans_tag] # assign maximum prob for the current transition condition/
                    prev_prob  = prev_prob * trans_tag_prob # save as previous viterbi probability
            except: tagged_sentence.append(lines[word] + "/" + "dunno") # Unknown pos tagger
        tagged_result.append(" ".join(tagged_sentence)) # stack tagged sentence to result lists
    return tagged_result