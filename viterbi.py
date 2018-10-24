import time
import json
from collections import defaultdict
import sys 
def viterbi(transition,emission,pi,obs):
    #viterbi_matrix[t][i]表示时间t时最后一个状态为i的维特比变量
    #这个维特比变量等于前一个所有维特比变量乘以转移概率再乘以发射概率中的最大值
    viterbi_matrix = defaultdict(dict)
    
    #backpointers_matrix[t][j]表示时间t最后一个状态为i达到最大概率时，
    #它是由哪一个前一个状态转移而来的
    backpointers_matrix = defaultdict(dict)
    N = len(transition) #状态数
    T = len(obs) #观测序列长度
    states = transition.keys()


    #初始化两个矩阵
    for s in states:
        #时刻1，每个cell（维特比变量）等于初始概率乘以相应发射概率
        if obs[0] in emission[s]:
            viterbi_matrix[0][s] = pi[s]*emission[s][obs[0]]
        #如果在训练的时候没有这个状态转移对，记为0。
        else:
            viterbi_matrix[0][s] = 0
        backpointers_matrix[0][s] = '<s>' #句首记号

    def argmax(t,s):
        '''
        计算对于t时刻s状态的维特比变量，顺便记录它是由哪一个状态转移而来
        '''
        max_prob, argmax_pre_state = 0,0
        for i in states:
            p = viterbi_matrix[t-1][i]*transition[i][s]*emission[s][obs[t]]
            if p > max_prob:
                max_prob = p
                argmax_pre_state = i 

        return max_prob,argmax_pre_state
    
    #递推
    for t in range(1,T):
        for s in states: 
            max_prob,argmax_pre_state = argmax(t,s)
            viterbi_matrix[t][s] = max_prob
            backpointers_matrix[t][s] = argmax_pre_state

    #查找最后时刻的最大概率和相应状态
    max_prob_final_state, max_prob = None, 0
    for s in states:
        #可能出现这个条件永不满足的情况，即最后时刻所有状态的最大可能概率都是0
        if viterbi_matrix[T-1][s] > max_prob:
            max_prob_final_state = s
            max_prob =  viterbi_matrix[T-1][s]

    
    #回溯最佳路线
    best_path = [max_prob_final_state]
    for t in range(T-1,0,-1):
        try:
            prev_state = backpointers_matrix[t][best_path[-1]]
            best_path.append(prev_state)
        except:
            best_path.append(None)

    best_path = list(reversed(best_path))


    return best_path


if __name__ == '__main__':
    sent = ['我们', '要', '坚定不移', '地', '贯彻', '执行', '党', '的', '以', '经济', '建设', '为', '中心', '、', \
            '坚持', '四项基本原则', '、', '坚持', '改革开放', '的', '基本路线', '。']
    with open('pi.json') as f:
        pi = json.load(f)
    with open('transition.json') as f:
        transition = json.load(f)
    with open('emission.json') as f:
        emission = json.load(f)

    path = viterbi(transition,emission,pi,sent) 

    #打印观察和状态的配对
    s = ''
    i = 0
    for p in path:
        s += sent[i]+ '/' + '<'+p+'>' + ' '
        i += 1
    print (s)


