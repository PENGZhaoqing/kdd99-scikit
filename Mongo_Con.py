from io import open
from pymongo import MongoClient
import pymongo
import numpy as np
from Variable import *

class DB_manager:
    client = MongoClient('localhost', 27017)
    db = client.test

    def import_training_data(self, training_file):

        self.db.training_data.delete_many({})
        self.db.training_data.create_index("training_set.type")

        with open(training_file) as f:
            lines = f.readlines()
            for line in lines:
                columns = line.split(',')
                dic = {}
                for attr in attr_list:
                    element = columns[attr_list.index(attr)]
                    if element.isdigit():
                        element = int(element)
                    elif self.isfloat(element):
                        element = float(element)
                    dic[attr] = element
                self.db.training_data.insert_one({"training_set": dic})

    def import_test_data(self, test_file):
        self.db.test_data.delete_many({})
        with open(test_file) as f:
            lines = f.readlines()
            for line in lines:
                columns = line.split(',')
                dic = {}
                for attr in attr_list:
                    element = columns[attr_list.index(attr)]
                    if element.isdigit():
                        element = int(element)
                    elif self.isfloat(element):
                        element = float(element)
                    dic[attr] = element
                self.db.test_data.insert_one({"test_set": dic})

    def CART_fetch_data(self):
        # training_cursor = self.db.training_data.find({"training_set.src_bytes": {"$gt": 1000}})
        # test_cursor = self.db.test_data.find({"test_set.src_bytes": {"$gt": 1000}})

        training_cursor = self.db.training_data.find()
        test_cursor = self.db.test_data.find()

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

        return np.array(dataset), np.array(dataTarget), training_len

    def MLP_fetch_data(self):
        # training_cursor = self.db.training_data.find({"training_set.src_bytes": {"$gt": 10000}})
        # test_cursor = self.db.test_data.find({"test_set.src_bytes": {"$gt": 100000}})

        training_cursor = self.db.training_data.find()
        test_cursor = self.db.test_data.find()

        cursor = training_cursor.sort('training_set.type', pymongo.ASCENDING)

        dataset = []
        dataTarget = []

        for document in cursor:
            tmp_dic = {}
            for attr in attr_list:
                if attr is not 'type':
                    try:
                        tmp_dic[attr] = document['training_set'][attr].encode('ascii')
                    except:
                        tmp_dic[attr] = document['training_set'][attr]
            dataset.append(tmp_dic)
            dataTarget.append(int(document['training_set']['type']))

        training_len = len(dataset)

        for document in test_cursor:
            tmp_dic = {}
            for attr in attr_list:
                if attr is not 'type':
                    try:
                        tmp_dic[attr] = document['test_set'][attr].encode('ascii')
                    except:
                        tmp_dic[attr] = document['test_set'][attr]
            dataset.append(tmp_dic)
            dataTarget.append(int(document['test_set']['type']))

        return np.array(dataset), np.array(dataTarget), training_len

    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
