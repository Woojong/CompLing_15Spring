# -*- coding: utf-8 -*-
#윗줄을 이 프로그램 파일이 utf-8으로 인코딩된 문자를 포함한다는 의미이다.
#codecs 모듈을 불러와서 사용
import codecs

#codecs를 이용한 코퍼스 오픈, unicode로 인코딩된 입력 텍스트 파일을 열기 위해서 사용하는 오브젝트
# f = codecs.open('BROWN_A1.txt', 'r', 'utf-8')
f = codecs.open('C:\\Users\\APD\\PycharmProjects\\CompLing\\hw2\\BROWN_A1.txt', 'r', 'utf-8')

#readlines()는 파일에 들어있는 한 라인의 string을 하나의 element로 리스트에 넣어서 반환한다. 그 반환한 리스트를 lines 변수에 저장
#lines에 저장된 형식 ['나는 학교에 다닌다.\n', '컴언은 정말 재미있다.\n', '컴언을 또 듣고 싶다.\n', ......]
lines = f.readlines()

#sentences에 저장하고 싶은 문장 형식 [['나는', '학교에', '다닌다.'], ['컴언은', '정말', '재미있다.'], ['컴언을', '또', '듣고', '싶다.'], ......]
#sentences를 빈 리스트로 초기화
sentences = []

for sent in lines:
	#lines에 들어있는 각 문장을 sent 변수에 순서대로 할당, lines에 들어있는 문장이 없을 때까지 loop 반복
	sent = sent.strip()	#문장 앞뒤에 포함된 ' '나 '\n'를 제거하여 반환한 값을 다시 sent에 저장
	words = sent.split(' ') #string type의 함수인 split을 이용하여 문장을 space 단위로 쪼개서 리스트로 반환한 결과를 words 변수에 저장
	sentences.append(words) #words에 저장된 형태 ['나는', '학교에', '다닌다.']를 sentences 리스트에 append 함수를 이용하여 저장

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

