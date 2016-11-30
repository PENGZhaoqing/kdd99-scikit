from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import collections


class Predictor:
    def predict(self, data_set, data_target, mode):
        clf = joblib.load('output/CART.pkl')
        trained_target = clf.predict(data_set)

        if mode == "validation":
            print "cross validation test_target sum: " + str(collections.Counter(data_target))
        elif mode == "test":
            print "true test_target sum: " + str(collections.Counter(data_target))

        print "\n"
        print confusion_matrix(data_target, trained_target, labels=[0, 1, 2, 3, 4])
        print "\n"
        print classification_report(data_target, trained_target)
        print "\n"

        return trained_target





        # for row in range(0, 4):
        #     if sum(matrix[row, :][0:-1]) > 0:
        #         matrix[row][5] = matrix[row][row] / sum(matrix[row, :][0:-1])

        # for col in range(0, 4):
        #     if sum(matrix[:, col][0:-1]) > 0:
        #         matrix[5][col] = matrix[col][col] / sum(matrix[:, col][0:-1])
        #
        # print np.around(matrix, 3)
