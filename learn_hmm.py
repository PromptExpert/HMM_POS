import json
from collections import defaultdict
import sys


filename = sys.argv[1] #训练数据的json文件，存储一个列表的句子，一个句子是一个列表的(词,词性)对，
vocab = defaultdict(int) #词-词频字典
pos   = set() #词性集合
MIN_COUNT = 1 #最小保留词的词频

#加载训练集，统计词频和词性集合
print ('开始加载数据...')
with open(filename) as f:
    train_sents = json.load(f)
    for s in train_sents:
        for w,p in s:
            vocab[w] += 1
            pos.add(p)

#根据最小词频过滤词汇表
vocab = [w[0] for w in vocab.items() if w[1] >= MIN_COUNT]

#声明初始频次计数，转移频次计数，发射频次计数
pi_freq = defaultdict(int) 
transition_freq = {}      
for p in pos:
    transition_freq[p] = defaultdict(int) #对于p这个词性，分配一个字典，存储p后面跟随的每个词性的频次
emission_freq = {}
for p in pos:
    emission_freq[p] = defaultdict(int) #对于p这个词性，分配一个字典，存储其发射的词的概率分布

#开始训练
print ('加载完毕,开始训练...')
for sent in train_sents:
    #学习初始概率，sent[0][1]是句子sent第一个(词，词性)对的词性，也就是本句第一个词性
    pi_freq[sent[0][1]] += 1

    #states_transition是一个列表的状态对，记录了词性的转移过程，例如
    #[('a', 'm'), ('m', 'nt'), ('nt', 'vd'), ('vd', 'p'), ('p', 'ns'), 
    # ('ns', 'v'), ('v', 'u'), ('u', 'p'), ('p', 'ns'), ('ns', 'n'), 
    #('n', 'n'), ('n', 'u'), ('u', 'v'), ('v', 'n'), ('n', 'w'), ('w', 'p'),
    # ('p', 'n'), ('n', 'n'), ('n', 'u'), ('u', 'v'), ('v', 'd'), ('d', 'v'), 
    #('v', 'u'), ('u', 'a'), ('a', 'n'), ('n', 'w')]
    states_transition = [(p1[1],p2[1]) for p1,p2 in zip(sent,sent[1:])]
    #学习转移概率
    for p1,p2 in states_transition:
        transition_freq[p1][p2] += 1
    
    #学习发射概率
    for w,p in sent:
        emission_freq[p][w] += 1

#对于没有出现的状态转移对和发射对，分配0
for p1 in pos:
    for p2 in pos:
        if p2 not in transition_freq[p1]:
            transition_freq[p1][p2] = 0 

for p in pos:
    for v in vocab:
        if v not in emission_freq[p]:
            emission_freq[p][v] = 0


#将频次计数转换成概率分布
def freq2prob(d):
    '''
    输入一个频次字典，输出一个概率字典
    '''
    prob_dist = {} 
    sum_freq = sum(d.values())
    for p,freq in d.items():
        prob_dist[p] = freq/sum_freq
    return prob_dist

pi = freq2prob(pi_freq)

transition = {}
for p, freq_dis in transition_freq.items():
    transition[p] = freq2prob(freq_dis)

emission = {}
for p,freq_dis in emission_freq.items():
    emission[p] = freq2prob(freq_dis)


#存储模型参数
print ('训练完毕,开始存储模型参数...')
with open('pi.json','w') as f:
    json.dump(pi,f,indent=2,ensure_ascii=False)

with open('transition.json','w') as f:
    json.dump(transition,f,indent=2,ensure_ascii=False)

with open('emission.json','w') as f:
    json.dump(emission,f,indent=2,ensure_ascii=False)

print ('存储完毕.')