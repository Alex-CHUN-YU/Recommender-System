__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from knn import KNN
from svm import SVM
from nb import NB
from mnb import MNB
from rfc import RFC
import numpy as np
import sklearn.datasets as ds 
import json
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split

# Classification Selection
class Classification():
    # Classification Initialize
    def __init__(self, train_X, train_y):
        self.train_X = train_X
        self.train_y = train_y

    # KNN Alogorithm
    def knn(self):
        # KNN Alogorithm
        knn = KNN()
        knn.tuning_parameters(self.train_X, self.train_y)
        knn.train(self.train_X, self.train_y)
        
    # SVM Alogorithm
    def svm(self):
        # SVM Alogorithm
        svm = SVM()
        svm.tuning_parameters(self.train_X, self.train_y)
        svm.train(self.train_X, self.train_y)
    
    # NB Alogorithm
    def nb(self):
        # NB Alogorithm
        nb = NB()
        nb.tuning_parameters(self.train_X, self.train_y)
        nb.train(self.train_X, self.train_y)

    # MNB Alogorithm
    def mnb(self):
        # MNB Alogorithm
        mnb = MNB()
        mnb.tuning_parameters(self.train_X, self.train_y)
        mnb.train(self.train_X, self.train_y)

    # RFC Alogorithm
    def rfc(self):
        # RFC Alogorithm
        rfc = RFC()
        rfc.tuning_parameters(self.train_X, self.train_y)
        rfc.train(self.train_X, self.train_y)

    # Find Best Estimator
    def find_best_estimator(self, X_test, y_test):
        print('-'*20, end = '\nK Nearest Neighbor:\n')
        # 載入參數並顯示出來
        with open('model/knn_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('n_neighbors: ' + str(p['n_neighbors']))
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('accuracy: ' + str(s['accuracy']))
                score = s['accuracy']
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        knn = joblib.load("model/knn.pkl")
        print("unknown data predictive score:", end = '')
        print(knn.score(X, y_test))
        #######################################
        print('-'*20, end = '\nSupport Vector Machine:\n')
        # 載入參數並顯示出來
        with open('model/svm_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('C: ' + str(p['C']))
                print('kernel: ' + p['kernel'])
                print('gamma: ' + str(p['gamma']))
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('accuracy: ' + str(s['accuracy']))
                score = s['accuracy']
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        svm = joblib.load("model/svm.pkl")
        print("unknown data predictive score:", end = '')
        print(svm.score(X, y_test))
        #######################################
        print('-'*20, end = '\nNaive Bayes:\n')
        # 載入參數並顯示出來
        with open('model/nb_parameters') as json_file:  
            data = json.load(json_file)
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('accuracy: ' + str(s['accuracy']))
        # 載入 model 並去預測
        nb = joblib.load("model/nb.pkl")
        print("unknown data predictive score:", end = '')
        print(nb.score(X_test, y_test))
        #######################################
        print('-'*20, end = '\nMultinomial Naive Bayes:\n')
        # 載入參數並顯示出來
        with open('model/mnb_parameters') as json_file:  
            data = json.load(json_file)
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('accuracy: ' + str(s['accuracy']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.MinMaxScaler().fit_transform(X_test)
        else:
            X = X_test
        mnb = joblib.load("model/mnb.pkl")
        print("unknown data predictive score:", end = '')
        print(mnb.score(X, y_test))
        #######################################
        print('-'*20, end = '\nRandom Forest Classifier:\n')
        # 載入參數並顯示出來
        with open('model/rfc_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('n_estimators: ' + str(p['n_estimators']))
                print('criterion: ' + p['criterion'])
                print('max_features: ' + p['max_features'])
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('accuracy: ' + str(s['accuracy']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        rfc = joblib.load("model/rfc.pkl")
        print("unknown data predictive score:", end = '')
        print(rfc.score(X, y_test))       

if __name__ == '__main__':
    # data sampling 必須是 cv(default = 10) * class number 以上
    # 如果是使用 knn,data sampling 必須大於設定的 n(default = 40) 值 
    # Build a classification task using 3 informative features
    X, y = ds.make_classification(n_samples = 1000,
                           n_features = 10,
                           n_informative = 3,
                           n_redundant = 0,
                           n_repeated = 0,
                           n_classes = 2,
                           random_state = 0,
                           shuffle = False)
    #X, y = ds.load_iris().data, ds.load_iris().target
    # 如果是 4 筆資料，1 筆測試，3 筆訓練
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)
    clf = Classification(X_train, y_train)
    # 已有 Model 可以註解掉(model test data dimension and train data dimension must same!)
    clf.knn()
    clf.svm()
    clf.nb()
    clf.mnb()
    clf.rfc()
    clf.find_best_estimator(X_test, y_test)

