# kdd99-scikit
Solutions to kdd99 dataset with Decision Tree (CART) and Multilayer Perceptron by scikit-learn

## Prerequisite

* Python 2.7.x
* [Scikit-learn tool](http://scikit-learn.org/stable/)
* Mongodb

## Usage

```
git clone https://github.com/PENGZhaoqing/kdd99-scikit
cd kdd99-scikit
python Preprocessing.py
```

### For Decision Tree

```
cd CART
python CART_Runner.py
```

Output:

confusion matrix:


Performance report:


Besides, you can visualize the trained tree in `CART/output/tree-vis.pdf`


And the trained model is persisted in `CART/output/CART.pkl`, you can perform off-line perdiction 

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

And the trained model is persisted in `MLP/output/MLP.pkl`, you can perform off-line perdiction 

## structure

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
