
## A Simple Python Implementation of Part-of-Speech Tagging with HMM

See [隐马尔可夫模型词性标注及其Python实现](https://nlppupil.github.io/%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0/2018/10/23/%E9%9A%90%E9%A9%AC%E5%B0%94%E5%8F%AF%E5%A4%AB%E6%A8%A1%E5%9E%8B%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8%E5%8F%8A%E5%85%B6Python%E5%AE%9E%E7%8E%B0.html) for detail.

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