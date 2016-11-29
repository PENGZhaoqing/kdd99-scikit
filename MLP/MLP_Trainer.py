from sklearn.externals import joblib
import random
from sklearn.feature_extraction import DictVectorizer
import collections
import numpy as np
from Mongo_Con import DB_manager
from sklearn.feature_selection import VarianceThreshold
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from Variable import attr_list


class Trainer:
    db = DB_manager.client

    def train(self, training_set, training_target):
        clf = MLPClassifier(solver='adam', alpha=1e-5,
                            hidden_layer_sizes=(10, 6), random_state=1)
        clf.fit(training_set, training_target)
        joblib.dump(clf, 'output/MLP.pkl')

    def feature_selection(self, data_set):
        """

        :param data_set:
        :return:
        """

        sel = VarianceThreshold(threshold=(.5 * (1 - .5)))
        feature_set = sel.fit_transform(data_set)

        fea_index = []
        for A_col in np.arange(data_set.shape[1]):
            for B_col in np.arange(feature_set.shape[1]):
                if (data_set[:, A_col] == feature_set[:, B_col]).all():
                    fea_index.append(A_col)

        check = {}
        for i in fea_index:
            check[attr_list[i]] = data_set[0][i]
        print check

        return data_set

    def one_hot_encoding(self, dataset, datatarget, T_len):
        """

        :param data_set:
        :param data_target:
        :return: data_set, data_target
        """

        vec = DictVectorizer()
        dataset = vec.fit_transform(dataset).toarray()

        print dataset.shape

        data_set = dataset[0:(T_len - 1)]
        data_target = datatarget[0:(T_len - 1)]

        test_set = dataset[T_len:len(dataset)]
        test_target = datatarget[T_len:len(dataset)]

        pca = PCA(n_components=20)
        pca.fit(data_set)

        data_set = pca.transform(data_set)
        test_set = pca.transform(test_set)

        print data_set.shape

        scaler = StandardScaler()
        scaler.fit(data_set)

        print(pca.explained_variance_ratio_)

        data_set = scaler.transform(data_set)
        test_set = scaler.transform(test_set)

        print collections.Counter(test_target)

        return data_set, data_target, test_set, test_target

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

        print "training_set: " + str(training_set.shape)
        print "training_target: " + str(training_target.shape)

        print "test_set: " + str(test_set.shape)
        print "test_target: " + str(test_target.shape)

        counter = collections.Counter(training_target)
        print counter

        return training_set, training_target, test_set, test_target
