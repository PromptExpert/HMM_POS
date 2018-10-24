import numpy as np
import json

def forward(transition,emission,pi,observations):
    T = len(observations)
    states = transition.keys()

    #初值
    alphas = []
    for s in states:
        pi_s = pi[s] if s in pi else 0
        alphas.append(pi_s*emission[s][observations[0]])
        

    #递推
    for t in range(1,T):
        previous_alphas = alphas
        alphas = []
        for s in states:
            braket = np.dot(previous_alphas,[dis[s] for dis in transition.values()]) #中括号内的内容，等于previous_alpha列表点乘转移矩阵的第i列
            alphas.append(braket*emission[s][observations[t]])

    #终止
    prob = sum(alphas)

    return prob


if __name__ == '__main__':
    with open('pi.json') as f:
        pi = json.load(f)
    with open('transition.json') as f:
        transition = json.load(f)
    with open('emission.json') as f:
        emission = json.load(f)

    with open('pos_test.json') as f:
        test_data = json.load(f)

    total_tags = []
    total_preds =[]
    for t in test_data:
        sent, _ = zip(*t)
        print (sent)
        print (forward(transition,emission,pi, sent))
        break