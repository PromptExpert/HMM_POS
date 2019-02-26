## A Simple Python Implementation of Part-of-Speech Tagging with HMM

See [隐马尔可夫模型词性标注及其Python实现](https://zhuanlan.zhihu.com/p/48260272) for detail.

#### Data
Click [here](https://pan.baidu.com/s/1gk28n6or4NHZfOuaiJg1Ag) to download the data.

#### Train
```
python learn_hmm.py pos_train.json
```

#### Decode
```
python viterbi.py
```

#### Forward Algorithm
```
python forward.py
```

#### Evaluate
```
python measure.py
```