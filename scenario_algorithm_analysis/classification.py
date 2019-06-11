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
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# Classification Selection
class Classification():
    # Classification Initialize
    def __init__(self, train_X, train_y, name):
        self.name = name
        # Save Evaluate Results
        self.model_name = 'model/' + self.name
        self.train_X = train_X
        self.train_y = train_y
        self.knn = None
        self.svm = None
        self.nb = None
        self.mnb = None
        self.rfc = None

    # KNN Alogorithm
    def knn_model(self):
        # KNN Alogorithm
        self.knn = KNN(self.name)
        self.knn.tuning_parameters(self.train_X, self.train_y)
        self.knn.train(self.train_X, self.train_y)
        
    # SVM Alogorithm
    def svm_model(self):
        # SVM Alogorithm
        self.svm = SVM(self.name)
        self.svm.tuning_parameters(self.train_X, self.train_y)
        self.svm.train(self.train_X, self.train_y)
    
    # NB Alogorithm
    def nb_model(self):
        # NB Alogorithm
        self.nb = NB(self.name)
        self.nb.tuning_parameters(self.train_X, self.train_y)
        self.nb.train(self.train_X, self.train_y)

    # MNB Alogorithm
    def mnb_model(self):
        # MNB Alogorithm
        self.mnb = MNB(self.name)
        self.mnb.tuning_parameters(self.train_X, self.train_y)
        self.mnb.train(self.train_X, self.train_y)

    # RFC Alogorithm
    def rfc_model(self):
        # RFC Alogorithm
        self.rfc = RFC(self.name)
        self.rfc.tuning_parameters(self.train_X, self.train_y)
        self.rfc.train(self.train_X, self.train_y)
    
    # Evaluate Result(accuracy, precision, recall, f1 score)
    def evaluate_result(self, model_name, model, X, y_true):
        # micro precision and recall and f1 score 都一樣, macro 則是每個類別的平均
        accuracy_score_result = model.score(X, y_true)
        precision_score_result = precision_score(y_true, model.predict(X), average = 'macro')
        recall_score_result = recall_score(y_true, model.predict(X), average = 'macro')
        f1_score_result = f1_score(y_true, model.predict(X), average = 'macro')
        print("unknown data accuracy_score: " + str(accuracy_score_result))
        print("unknown data precision_score: " + str(precision_score_result))
        print("unknown data recall_score: " + str(recall_score_result))
        print("unknown data f1_score: " + str(f1_score_result))
        # 儲存評估結果
        evaluate_result = {}
        evaluate_result['result'] = []
        evaluate_result['result'].append({  
        'accuracy': accuracy_score_result,
        'precision_score': precision_score_result,
        'recall_score': recall_score_result,
        'f1_score': f1_score_result
        })
        with open(self.model_name + "_" + model_name + '_evaluate_result', 'w', encoding = "utf-8") as result:
            json.dump(evaluate_result, result)
        print("Evaluate Result is Saved")

    # Find Best Estimator
    def find_best_estimator(self, X_test, y_test):
        print('-'*20, end = '\nK Nearest Neighbor:\n')
        # 載入參數並顯示出來
        with open(self.knn.model_name + '_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('n_neighbors: ' + str(p['n_neighbors']))
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('valid_score: ' + str(s['valid_score']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        knn = joblib.load(self.knn.model_name + '.pkl')
        self.evaluate_result("knn", knn, X, y_test)
        #######################################
        print('-'*20, end = '\nSupport Vector Machine:\n')
        # 載入參數並顯示出來
        with open(self.svm.model_name + '_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('C: ' + str(p['C']))
                print('kernel: ' + p['kernel'])
                print('gamma: ' + str(p['gamma']))
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('valid_score: ' + str(s['valid_score']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        svm = joblib.load(self.svm.model_name + ".pkl")
        self.evaluate_result("svm", svm, X, y_test)
        #######################################
        print('-'*20, end = '\nNaive Bayes:\n')
        # 載入參數並顯示出來
        with open(self.nb.model_name + '_parameters') as json_file:  
            data = json.load(json_file)
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('valid_score: ' + str(s['valid_score']))
        # 載入 model 並去預測
        nb = joblib.load(self.nb.model_name + ".pkl")
        self.evaluate_result("nb", nb, X_test, y_test)
        #######################################
        print('-'*20, end = '\nMultinomial Naive Bayes:\n')
        # 載入參數並顯示出來
        with open(self.mnb.model_name + '_parameters') as json_file:  
            data = json.load(json_file)
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('valid_score: ' + str(s['valid_score']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.MinMaxScaler().fit_transform(X_test)
        else:
            X = X_test
        mnb = joblib.load(self.mnb.model_name + ".pkl")
        self.evaluate_result("mnb", mnb, X, y_test)
        #######################################
        print('-'*20, end = '\nRandom Forest Classifier:\n')
        # 載入參數並顯示出來
        with open(self.rfc.model_name + '_parameters') as json_file:  
            data = json.load(json_file)
            for p in data['parameters']:
                print('n_estimators: ' + str(p['n_estimators']))
                print('criterion: ' + p['criterion'])
                print('max_features: ' + p['max_features'])
            # 不同的評分標準 key 要做更改
            for s in data['scoring']:
                print('valid_score: ' + str(s['valid_score']))
            for p in data['preprocessing']:
                print('normalization: ' + str(p['normalization']))
                normalization = p['normalization']
        # 載入 model 並去預測
        if normalization == True:
            X = preprocessing.scale(X_test)
        else:
            X = X_test
        rfc = joblib.load(self.rfc.model_name + ".pkl")
        self.evaluate_result("rfc", rfc, X, y_test)      

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
    clf.knn_model()
    clf.svm_model()
    clf.nb_model()
    clf.mnb_model()
    clf.rfc_model()
    clf.find_best_estimator(X_test, y_test)

