from sklearn.externals import joblib
import random
from sklearn import tree
from sklearn import preprocessing
import numpy as np
import pydotplus
from Mongo_Con import DB_manager
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
from Variable import attr_list


class Trainer:
    db = DB_manager.client

    def train(self, training_set, training_target, fea_index):

        clf = tree.DecisionTreeClassifier(criterion="entropy", min_samples_split=30, class_weight="balanced")
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

    def feature_selection(self, data_set, feature_names):
        """

        :param data_set:
        :return:
        """
        sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
        feature_set = sel.fit_transform(data_set)

        fea_index = []
        for A_col in np.arange(data_set.shape[1]):
            for B_col in np.arange(feature_set.shape[1]):
                if (data_set[:, A_col] == feature_set[:, B_col]).all():
                    fea_index.append(A_col)

        check = {}
        for i in fea_index:
            check[feature_names[i]] = data_set[0][i]
        print np.array(check)

        return feature_set, fea_index

    def tree_based_selection(self, data_set, data_target, feature_names):
        """

        :param data_set:
        :return:
        """

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

        check = {}
        for i in fea_index:
            check[feature_names[i]] = data_set[0][i]
        print np.array(check)

        return feature_set, fea_index

    def label_encoding(self, dataset):
        """

        :param data_set:
        :param data_target:
        :return: data_set
        """

        le_1 = preprocessing.LabelEncoder()
        le_2 = preprocessing.LabelEncoder()
        le_3 = preprocessing.LabelEncoder()

        le_1.fit(np.unique(dataset[:, 1]))
        le_2.fit(np.unique(dataset[:, 2]))
        le_3.fit(np.unique(dataset[:, 3]))

        dataset[:, 1] = le_1.transform(dataset[:, 1])
        dataset[:, 2] = le_2.transform(dataset[:, 2])
        dataset[:, 3] = le_3.transform(dataset[:, 3])

        return dataset

    def corss_validation_filter(self, data_set, data_target, factor=0.1):
        """

        :param data_set:
        :param data_target:
        :return: training_set, training_target, test_set, test_target
        """
        test_index = random.sample(range(0, len(data_target) - 1), int(len(data_target) * factor))
        training_index = list(set(range(0, len(data_target) - 1)) - set(test_index))

        training_set = data_set[training_index]
        training_target = data_target[training_index]

        test_set = data_set[test_index]
        test_target = data_target[test_index]

        print "\n"
        print "training_set: " + str(training_set.shape)
        print "training_target: " + str(training_target.shape)

        print "test_set: " + str(test_set.shape)
        print "test_target: " + str(test_target.shape)
        print "\n"

        return training_set, training_target, test_set, test_target
