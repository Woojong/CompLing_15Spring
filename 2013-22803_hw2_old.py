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
data = data.lower()
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
        ngram_dict.setdefault(tmp_words,0) # making default dictionary value for current words
        ngram_dict[tmp_words] += 1 # plus 1 if exist current words
    if dict == True:
        return ngram_dict # returning dictionary
    else:
        return ngram_list # returning list

#### calculating conditional probability defining function
def cond_prob(numer_dict, denom_dict, ngramprob = False): # numer_dict for numerator dictionary, denom_dict for denominator dictionary
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
## aking probability dictionary
mle_dict = cond_prob(bi_dict, uni_dict, False)
biprob_dict = cond_prob(bi_dict, uni_dict, True)


result_table = []
header = ["Bigram", "MLE Prob.", "Bi Prob"]
for key, value in sorted(mle_dict.items(), lambda a, b: cmp(a[1], b[1]), reverse=True):
    result_table.append([key, value, biprob_dict[key]])

w = open(curr_dir + my_dir + savetext, 'w')
w.write(tabulate(result_table, header, floatfmt = ".15f"))
w.close()


def ngrams_maker(data, ngram):
    data = data.split()
    tmp_ngram = {}
    for i in range(len(input)-ngram+1):
        g = ' '.join(input[i:i+ngram])
        tmp_ngram.setdefault(g, 0)
        tmp_ngram[g] += 1
    return output
#readlines()는 파일에 들어있는 한 라인의 string을 하나의 element로 리스트에 넣어서 반환한다. 그 반환한 리스트를 lines 변수에 저장
#lines에 저장된 형식 ['나는 학교에 다닌다.\n', '컴언은 정말 재미있다.\n', '컴언을 또 듣고 싶다.\n', ......]
lines = f.readlines()

#sentences에 저장하고 싶은 문장 형식 [['나는', '학교에', '다닌다.'], ['컴언은', '정말', '재미있다.'], ['컴언을', '또', '듣고', '싶다.'], ......]
#sentences를 빈 리스트로 초기화
sentences = []

for sent in lines:
    # print sent
	#lines에 들어있는 각 문장을 sent 변수에 순서대로 할당, lines에 들어있는 문장이 없을 때까지 loop 반복
	sent = sent.strip()	#문장 앞뒤에 포함된 ' '나 '\n'를 제거하여 반환한 값을 다시 sent에 저장
    # print sent
	words = sent.split(' ') #string type의 함수인 split을 이용하여 문장을 space 단위로 쪼개서 리스트로 반환한 결과를 words 변수에 저장
    # print words
	sentences.append(words) #words에 저장된 형태 ['나는', '학교에', '다닌다.']를 sentences 리스트에 append 함수를 이용하여 저장
    # print words
    # tmp = raw_input()
    # if tmp == "q":
    #     break

'''
for sent in sentences:
	for word in sent:
		print word,
	print '\n',
'''

#unigram count를 구하여 uni_dict 딕셔너리 변수에 저장
uni_dict = {}

for sent in sentences:
	#sentences안에 각 문장을 리스트로 하나씩 sent에 할당
	for word in sent:
		#각 문장에 단어 string을 word에 할당
		if uni_dict.has_key(word): #uni_dict안에 key로 word가 존재하는지 검사
			#uni_dict[word]에 들어있는 count value를 1 증가 시켜 덮어 씌어 저장
			uni_dict[word] = uni_dict[word] + 1
		else: #uni_dict안에 key로 word가 존재하지 않을 때
			#word값을 key로 1로 value를 초기화
			uni_dict[word] = 1

'''
for key in uni_dict.keys():
	print 'word: %s	frequency: %d' % (key, uni_dict[key])
'''

#bigram count를 구하여 bi_dict 딕셔너리 변수에 저장
#bigram: 두 단어의 연쇄

bi_dict = {}
for sent in sentences: #각 문장 마다 bigram을 만들기 위해 sent에 각 문장 할당
	if len(sent) > 1: #sent안에 들어있는 element갯수, 즉 문장의 길이가 한 단어 이상일 때만 bigram 만듬
		for i in range(len(sent)): #len(sent)는 문장에 포함된 단어의 갯수, range()에 넣어 0부터 단어갯수-1까지의 리스트 만듬
			if (i == 0): #i값을 이용하여 sent안에 단어 값 접근함, 그때 i값이 0이라서 문장 시작 표시와 bigram을 만들 필요가 있을 경우
				bi_pair = "<s>" + " " + sent[i]
            #string을 붙여서 bigram을 만들고 그 바이그램 스트링을 딕셔너리에 있는지 없는지 검사후 있을 때는 카운트 증가 없을 때는 1로 초기화함
				if bi_dict.has_key(bi_pair):
					bi_dict[bi_pair] = bi_dict[bi_pair] + 1
				else:
					bi_dict[bi_pair] = 1
            #i가 증가하고나면 sent[0], sent[1]의 연쇄 bigram을 만들 수 없기 때문에 여기서 bigram 생성
				bi_pair = sent[i] + " " + sent[i+1]
				if bi_dict.has_key(bi_pair):
					bi_dict[bi_pair] = bi_dict[bi_pair] + 1
				else:
					bi_dict[bi_pair] = 1

			elif (i == len(sent)-1): #i값이 문장의 마지막 인덱스일 때는 문장의 끝 표시 </>와 함께 bigram 만듬
				bi_pair = sent[i] + " " + "</s>"
				if bi_dict.has_key(bi_pair):
					bi_dict[bi_pair] = bi_dict[bi_pair] + 1
				else:
					bi_dict[bi_pair] = 1

			else: #i의 값이 문장 두번째 단어부터 마지막 전 단어일때의 bigram생성을 위한 부분
				bi_pair = sent[i] + " " + sent[i+1]
				if bi_dict.has_key(bi_pair):
					bi_dict[bi_pair] = bi_dict[bi_pair] + 1
				else:
					bi_dict[bi_pair] = 1

'''
#bigram dictionary 출력
for key in bi_dict.keys():
	print 'bigram: %s	frequency: %d' % (key, bi_dict[key])
'''
#conditional probability P(b|a) = count(a b) / count (a)

#conditional probability 저장을 위한 딕셔너리 con_prob 초기화
con_prob = {}
for key in bi_dict.keys():
	#bigram 딕셔너리에서 bigram의 key값을 split하여 리스트로 저장
	bigram = key.split()
	#bigram[0]인 첫단어의  unigram이 존재하지 않을 경우, 즉 bigram[0]이 <s>일 경우, <s>의 유니그램은 문장 전체수로 생각할 수 있다.
	if not uni_dict.has_key(bigram[0]):
		#존재하는 bigram[1]의 unigram count를 문장 전체의 갯수로 나눔
		prob = float(uni_dict[bigram[1]])/float(len(sentences))
		con_prob[key] = prob
	#또는 bigram[1]인 두번째 단어의 unigram이 존재하지 않을 경우, 즉 bigram[1]이 </s>일 경우, </s>의 유니그램은 문장 전체수로 생각할 수 있다.
	elif not uni_dict.has_key(bigram[1]):
		prob = float(uni_dict[bigram[0]])/float(len(sentences))
		con_prob[key] = prob
	else:
		#모든 bigram count를 첫 단어의 unigram 카운트로 나누어 P(b|a) 값 저장
		prob = float(bi_dict[key]) / float(uni_dict[bigram[0]])
		con_prob[key] = prob
#conditional probability dictionary 출력
for key in con_prob.keys():
    bigram = key.split()
    print 'P(%s|%s) prob: %f' % (bigram[1], bigram[0], con_prob[key])

def cond_prob(nom_dict, denom_dict):
    conditional = {}
    for key in nom_dict.keys():
        cur_ngram = key.split()
        if not denom_dict.has_key(cur_ngram[0]):
            prob = float(denom_dict[cur_ngram[1]])/float(len())
        elif not denom_dict.has_key(cur_ngram[1]):
            prob = float(denom_dict[cur_ngram[0]])/float(len())
        else:
            prob = float(nom_dict[key])/float(denom_dict[cur_ngram[0]])
            conditional[key] = prob
    return conditional

def cond_prob(numer_dict, denom_dict):
    conditional = {}
    for key in numer_dict.keys():
        cur_ngram = key.split()
        prob = float(numer_dict[key])/float(denom_dict[" ".join(cur_ngram[:len(cur_ngram)-1])])
        conditional[key] = prob
    return conditional
