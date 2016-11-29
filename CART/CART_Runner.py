from Mongo_Con import DB_manager
from CART_Trainer import Trainer
from CART_Predictor import Predictor
from Variable import attr_list


class Runner:
    trainer = Trainer()
    predictor = Predictor()

    def train_and_validate(self, dataset, datatarget, T_len):
        dataset = self.trainer.label_encoding(dataset)
        # feature_set, fea_index = self.trainer.feature_selection(data_set, self.db.attr_list)
        data_set = dataset[0:(T_len - 1)]
        data_target = datatarget[0:(T_len - 1)]
        feature_set, fea_index = self.trainer.tree_based_selection(data_set, data_target, attr_list)
        training_set, training_target, test_set, test_target = self.trainer.corss_validation_filter(feature_set,
                                                                                                    data_target)
        self.trainer.train(training_set, training_target, fea_index)
        self.predictor.predict(test_set, test_target, mode="validation")
        return dataset, datatarget, fea_index

    def predict(self, data_set, data_target, fea_index, T_len):
        test_data_set = data_set[T_len:len(dataset)]
        test_data_target = data_target[T_len:len(dataset)]
        feature_set = test_data_set[:, fea_index]
        self.predictor.predict(feature_set, test_data_target, mode="test")


runner = Runner()
dataset, datatarget, T_len = DB_manager().CART_fetch_data()
dataset, datatarget, fea_index = runner.train_and_validate(dataset, datatarget, T_len)
runner.predict(dataset, datatarget, fea_index, T_len)
