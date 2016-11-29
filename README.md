# kdd99-scikit
Solutions to kdd99 dataset with Decision Tree (CART) and Multilayer Perceptron by scikit-learn

## Intro to Kdd99 Dataset

The [competition task](https://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html) was to build a network intrusion detector, a predictive model capable of distinguishing between "bad" connections, called intrusions or attacks, and "good" normal connections. Note that the test data is not from the same probability distribution as the training data, and it includes specific attack types not in the training data. 

Snapshoot of training data(`raw/kddcup.data_10_percent.txt`):
```
0,tcp,http,SF,181,5450,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,9,9,1.00,0.00,0.11,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,239,486,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,19,19,1.00,0.00,0.05,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,235,1337,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,29,29,1.00,0.00,0.03,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,219,1337,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,6,6,0.00,0.00,0.00,0.00,1.00,0.00,0.00,39,39,1.00,0.00,0.03,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,217,2032,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,6,6,0.00,0.00,0.00,0.00,1.00,0.00,0.00,49,49,1.00,0.00,0.02,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,217,2032,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,6,6,0.00,0.00,0.00,0.00,1.00,0.00,0.00,59,59,1.00,0.00,0.02,0.00,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,212,1940,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,2,0.00,0.00,0.00,0.00,1.00,0.00,1.00,1,69,1.00,0.00,1.00,0.04,0.00,0.00,0.00,0.00,normal.
0,tcp,http,SF,159,4087,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,5,5,0.00,0.00,0.00,0.00,1.00,0.00,0.00,11,79,1.00,0.00,0.09,0.04,0.00,0.00,0.00,0.00,normal.
```

## Prerequisite

* Python 2.7.x
* [Scikit-learn tool](http://scikit-learn.org/stable/)
* Mongodb

## Usage

Fork first and then execute `Preprocessing.py` file to do:

1. 将raw目录下的训练集和测试集的target类别用数字标识，生成新的文件储存在data目录下
2. 将data目录下的训练机和测试集导入MongoDB数据库，方便后面快速读取

```
git clone https://github.com/your-github-account/kdd99-scikit
cd kdd99-scikit
python Preprocessing.py
```

### For Decision Tree

```
cd CART
python CART_Runner.py
```

Output:

Confusion matrix:

```
[[ 6335     7    24     0     2]
 [  184   606    19     0     0]
 [  233     1 41486     0     0]
 [    3     0     0     0     0]
 [ 1098     0     1     0     1]]
```

Performance report:

```
             precision    recall  f1-score   support

          0       0.81      0.99      0.89      6368
          1       0.99      0.75      0.85       809
          2       1.00      0.99      1.00     41720
          3       0.00      0.00      0.00         3
          4       0.33      0.00      0.00      1100

avg / total       0.96      0.97      0.96     50000
```

训练完成的决策树导出到`CART/output/tree-vis.pdf`供可视化



决策树模型被持久化在 `CART/output/CART.pkl`文件下，方便以后做离线预测

### For MLP

```
cd MLP
python MLP_Runner.py
```

Output:

confusion matrix:
```
[[ 6320    41     6     0     1]
 [    5   801     3     0     0]
 [  212     0 41508     0     0]
 [    2     1     0     0     0]
 [ 1095     1     2     0     2]]
```

Performance report:
```
             precision    recall  f1-score   support

          0       0.83      0.99      0.90      6368
          1       0.95      0.99      0.97       809
          2       1.00      0.99      1.00     41720
          3       0.00      0.00      0.00         3
          4       0.67      0.00      0.00      1100

avg / total       0.97      0.97      0.96     50000
```

MLP模型被持久化在 `MLP/output/MLP.pkl`文件下，方便以后做离线预测

## Structure

```
.
├── CART
│   ├── CART_Predictor.py
│   ├── CART_Predictor.pyc
│   ├── CART_Runner.py
│   ├── CART_Trainer.py
│   ├── CART_Trainer.pyc
│   ├── __init__.py
│   └── output
│       ├── CART.pkl
│       └── tree-vis.pdf
├── MLP
│   ├── MLP_Predictor.py
│   ├── MLP_Predictor.pyc
│   ├── MLP_Runner.py
│   ├── MLP_Trainer.py
│   ├── MLP_Trainer.pyc
│   ├── __init__.py
│   └── output
│       ├── MLP.pkl
│       └── decision-tree.pkl
├── Mongo_Con.py
├── Mongo_Con.pyc
├── Preprocessing.py
├── Preprocessing.pyc
├── Variable.py
├── Variable.pyc
├── __init__.py
├── __init__.pyc
├── data
│   ├── corrected.txt
│   └── kddcup.data_10_percent.txt
└── raw
    ├── corrected.txt
    ├── kddcup.data_10_percent.txt
    ├── testdata_unlabeled_50000.txt
    └── training_attack_types.txt
    
```
