from viterbi import viterbi
import json

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
        sent, tags = zip(*t)
        preds = viterbi(transition,emission,pi,sent) 
        total_tags.extend(tags)
        total_preds.extend(preds)

    correct_num = sum([t==p for t,p in zip(total_tags,total_preds)])

    print ('准确率{0:.2f}%'.format(correct_num*100/len(total_preds)))
