from sklearn.externals import joblib
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

class Predictor:
    def predict(self, test_set, test_target):
        clf = joblib.load('output/MLP.pkl')
        trained_target = clf.predict(test_set)

        print confusion_matrix(test_target, trained_target, labels=[0, 1, 2, 3, 4])
        print classification_report(test_target, trained_target)


