from Mongo_Con import DB_manager
from MLP_Trainer import Trainer
from MLP_Predictor import Predictor


class MLP_Runner:
    trainer = Trainer()
    predictor = Predictor()

    def data_load(self):
        dataset, datatarget, T_len = self.db.MLP_fetch_data()
        return dataset, datatarget, T_len

    def train(self, dataset, datatarget, T_len):
        data_set, data_target, test_set, test_target = self.trainer.one_hot_encoding(dataset, datatarget, T_len)
        self.trainer.train(data_set, data_target)
        self.predictor.predict(test_set, test_target)

runner = MLP_Runner()
dataset, datatarget, T_len = DB_manager().MLP_fetch_data()
runner.train(dataset, datatarget, T_len)
