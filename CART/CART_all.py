# -------------Fetching data------------------
from pymongo import MongoClient
import pymongo
import numpy as np

attr_list = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
             'urgent', 'hot', 'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell',
             'su_attempted', 'num_root', 'num_file_creations', 'num_shells', 'num_access_files',
             'num_outbound_cmds',
             'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
             'rerror_rate',
             'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count',
             'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
             'dst_host_same_src_port_rate',
             'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
             'dst_host_rerror_rate',
             'dst_host_srv_rerror_rate', 'type']

client = MongoClient('localhost', 27017)
db = client.test

training_cursor = db.training_data.find({"training_set.src_bytes": {"$gt": 1000000}})
test_cursor = db.test_data.find({"test_set.src_bytes": {"$gt": 1000000}})

cursor = training_cursor.sort('training_set.type', pymongo.ASCENDING)
dataset = []
dataTarget = []
for document in cursor:
    tmp = []
    for attr in attr_list:
        if attr is not 'type':
            try:
                tmp.append(document['training_set'][attr].encode('ascii'))
            except:
                tmp.append(document['training_set'][attr])
    dataset.append(tmp)
    dataTarget.append(int(document['training_set']['type']))

training_len = len(dataset)
for document in test_cursor:
    tmp = []
    for attr in attr_list:
        if attr is not 'type':
            try:
                tmp.append(document['test_set'][attr].encode('ascii'))
            except:
                tmp.append(document['test_set'][attr])
    dataset.append(tmp)
    dataTarget.append(int(document['test_set']['type']))

dataset = np.array(dataset)
datatarget = np.array(dataTarget)
T_len = training_len

# -------------Categorical variable encoding------------------
from sklearn import preprocessing

le_1 = preprocessing.LabelEncoder()
le_2 = preprocessing.LabelEncoder()
le_3 = preprocessing.LabelEncoder()

le_1.fit(np.unique(dataset[:, 1]))
le_2.fit(np.unique(dataset[:, 2]))
le_3.fit(np.unique(dataset[:, 3]))

dataset[:, 1] = le_1.transform(dataset[:, 1])
dataset[:, 2] = le_2.transform(dataset[:, 2])
dataset[:, 3] = le_3.transform(dataset[:, 3])

# -------------feature selection------------------
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel

data_set = dataset[0:(T_len - 1)]
data_target = datatarget[0:(T_len - 1)]

clf = ExtraTreesClassifier()
clf = clf.fit(data_set, data_target)
print clf.feature_importances_

model = SelectFromModel(clf, prefit=True)
feature_set = model.transform(data_set)

fea_index = []
for A_col in np.arange(data_set.shape[1]):
    for B_col in np.arange(feature_set.shape[1]):
        if (data_set[:, A_col] == feature_set[:, B_col]).all():
            fea_index.append(A_col)

# -------------Cross Validation Split------------------
from sklearn import tree
import random
import pydotplus
from sklearn.externals import joblib

test_index = random.sample(range(0, len(feature_set) - 1), int(len(data_target) * 0.1))
training_index = list(set(range(0, len(feature_set) - 1)) - set(test_index))

training_set = feature_set[training_index]
training_target = data_target[training_index]

test_set = feature_set[test_index]
test_target = data_target[test_index]

# -------------Training Tree------------------
clf = tree.DecisionTreeClassifier(criterion="gini", max_depth=7, min_samples_leaf=50)
clf = clf.fit(training_set, training_target)

class_names = np.unique([str(i) for i in training_target])
feature_names = [attr_list[i] for i in fea_index]

dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=feature_names,
                                class_names=class_names,
                                filled=True, rounded=True,
                                special_characters=True)

graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("output/tree-vis.pdf")
joblib.dump(clf, 'output/CART.pkl')

# -------------Prediction of cross validation------------------
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

clf = joblib.load('output/CART.pkl')
trained_target = clf.predict(test_set)

print confusion_matrix(test_target, trained_target, labels=[0, 1, 2, 3, 4])
print classification_report(test_target, trained_target)

# -------------Prediction of test dataset------------------
test_data_set = dataset[T_len:len(dataset)]
test_data_target = datatarget[T_len:len(dataset)]
test_feature_set = test_data_set[:, fea_index]

clf = joblib.load('output/CART.pkl')
test_trained_target = clf.predict(test_feature_set)

print confusion_matrix(test_data_target, test_trained_target, labels=[0, 1, 2, 3, 4])
print classification_report(test_data_target, test_trained_target)
