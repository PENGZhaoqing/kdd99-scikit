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
And the trained model is persisted in `CART/output/CART.pkl`



### For MLP

cd MLP
python MLP_Runner.py

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



