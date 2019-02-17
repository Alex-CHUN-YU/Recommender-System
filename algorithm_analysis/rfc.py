__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn import preprocessing
from sklearn.model_selection import validation_curve
from sklearn.model_selection import GridSearchCV
from sklearn_evaluation.plot import grid_search
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import json

# Random Forest Classifier Alogorithm
class RFC():
    # RFC Initialize
    def __init__(self):
        # RFC Parameter
        self.n_estimators = 10
        self.criterion = 'gini'
        self.max_depth = None
        self.min_samples_split = 2
        self.min_samples_leaf = 1
        self.min_weight_fraction_leaf = 0.0
        self.max_features = 'auto'
        self.max_leaf_nodes = None
        self.min_impurity_decrease = 0.0
        self.min_impurity_split = None
        self.bootstrap = True
        self.oob_score = False
        self.n_jobs = -1
        self.random_state = None
        self.verbose = 0
        self.warm_start = False
        self.class_weight = None
        #(Validation Parameter) GridSearchCV, validation_curve
        self.cv = 10
        self.criterion_range = ['gini', 'entropy'] # 2 * 3
        self.max_features_range = ['sqrt', 'log2', 'auto']
        self.n_estimators_range = [10, 50, 100, 700, 1000]# 5
        # Accuracy(GridSearchCV application)
        self.score = 0
        self.scoring = 'accuracy'# f1、recall、 precision, your target must binary in sklearn(但貼心的 sklearn 還是有提供 f1_micro、f1_macro...)
        # Normalization        
        self.normalization = False 

    # Find Best Parameter(RFC 有沒有 normalization 都沒差? 暫且留著)
    def tuning_parameters(self, X, y):
        # 第一次 tuning (找出 best n_estimators 和 best max_features)
        # n_estimators 叢林中要有幾顆樹（default = 10）
        # criterion 計算資訊量的的方式（劃分樹分支時所需要的）, gini 或 entropy（default = 'gini'）
        # max_features 選擇最適合屬性時劃分的特徵不能超過此值
        clf = RandomForestClassifier(n_estimators = self.n_estimators, criterion = self.criterion, max_depth = self.max_depth,
                                     min_samples_split = self.min_samples_split, min_samples_leaf = self.min_samples_leaf, 
                                     min_weight_fraction_leaf = self.min_weight_fraction_leaf, max_features = self.max_features,
                                     max_leaf_nodes = self.max_leaf_nodes, min_impurity_decrease = self.min_impurity_decrease,
                                     min_impurity_split = self.min_impurity_split, bootstrap = self.bootstrap, oob_score = self.oob_score,
                                     n_jobs = self.n_jobs, random_state = self.random_state, verbose = self.verbose,
                                     warm_start = self.warm_start, class_weight = self.class_weight)
        parameter_candidates = {# Set the parameter candidates
            'n_estimators': self.n_estimators_range,
            'criterion': self.criterion_range,
            'max_features': self.max_features_range}
        clf_gscv = GridSearchCV(estimator = clf, param_grid = parameter_candidates, cv = self.cv, scoring = self.scoring, n_jobs = self.n_jobs)# Create a classifier with the parameter candidates
        clf_gscv.fit(X, y)# No Normalization
        normalization_clf_gscv = clf_gscv
        normalization_clf_gscv.fit(preprocessing.scale(X), y)# Normalization
        if normalization_clf_gscv.best_score_ > clf_gscv.best_score_:
            self.normalization = True
            X = preprocessing.scale(X)
            self.n_estimators = normalization_clf_gscv.best_estimator_.n_estimators
            self.criterion = normalization_clf_gscv.best_estimator_.criterion
            self.max_features = normalization_clf_gscv.best_estimator_.max_features
            self.score = normalization_clf_gscv.best_score_
            clf = normalization_clf_gscv
        else:
            self.n_estimators = clf_gscv.best_estimator_.n_estimators
            self.criterion = clf_gscv.best_estimator_.criterion
            self.max_features = clf_gscv.best_estimator_.max_features
            self.score = clf_gscv.best_score_
            clf = clf_gscv
#             # Print out the results 
#             print('Best score for training data:', clf_gscv.best_score_)
#             print('Best n_estimators:',clf_gscv.best_estimator_.n_estimators)
#             print('Best max_features:',clf_gscv.best_estimator_.max_features)
#         print(normalization_clf_gscv.best_score_)
#         print(clf.cv_results_['params'])
        criterion = [x['criterion'] for x in clf.cv_results_['params']]
#         print(criterion)
        max_features = [x['max_features'] for x in clf.cv_results_['params']]
#         print(max_features)
        plt.title("Validation Curve with RFC")
        plt.xlabel("Value Of n_estimators For RFC")
        plt.ylabel(self.scoring)
        # 6 * 5
        mean_scores = np.array(clf.cv_results_['mean_test_score']).reshape(len(self.criterion_range) * len(self.max_features_range), len(self.n_estimators_range))
        std_scores = np.array(clf.cv_results_['std_test_score']).reshape(len(self.criterion_range) * len(self.max_features_range), len(self.n_estimators_range))
#         print(mean_scores)
#         print(std_scores)
        ind = 0
        for i in range(0, len(criterion), len(self.n_estimators_range)):
            plt.plot(self.n_estimators_range, mean_scores[ind], "-o", label = 'criterion: ' + criterion[i] + ', max_features: ' + max_features[i])
            plt.fill_between(self.n_estimators_range, mean_scores[ind] - std_scores[ind], 
                             mean_scores[ind] + std_scores[ind], alpha = 0.2)
            ind += 1
        plt.legend(loc = "best") # best location
        plt.savefig('image/rfc.png')# save image
        plt.close()
        print("RFC Save Image Finished")
        print("RFC Tuning Parameters Finished")
            
    # Produce Model
    def train(self, X, y):
        # Train
        clf = RandomForestClassifier(n_estimators = self.n_estimators, criterion = self.criterion, max_depth = self.max_depth,
                                     min_samples_split = self.min_samples_split, min_samples_leaf = self.min_samples_leaf, 
                                     min_weight_fraction_leaf = self.min_weight_fraction_leaf, max_features = self.max_features,
                                     max_leaf_nodes = self.max_leaf_nodes, min_impurity_decrease = self.min_impurity_decrease,
                                     min_impurity_split = self.min_impurity_split, bootstrap = self.bootstrap, oob_score = self.oob_score,
                                     n_jobs = self.n_jobs, random_state = self.random_state, verbose = self.verbose,
                                     warm_start = self.warm_start, class_weight = self.class_weight)
        if self.normalization == True:
            X = preprocessing.scale(X)
        clf.fit(X, y)
        # 透過 joblib 存 model
        joblib.dump(clf, "model/rfc.pkl")
        print("RFC Save Model Finished")
        # 儲存參數、準確性
        parameters = {}
        parameters['parameters'] = []
        parameters['parameters'].append({  
        'n_estimators': self.n_estimators,
        'criterion': self.criterion,
        'max_features': self.max_features,    
        })
        parameters['scoring'] = []
        parameters['scoring'].append({  
        self.scoring: self.score
        })
        parameters['preprocessing'] = []
        parameters['preprocessing'].append({  
        'normalization': self.normalization
        })
        with open('model/rfc_parameters', 'w', encoding = "utf-8") as rfcf:
            json.dump(parameters, rfcf)
        print("RFC Save Parameters Finished")
            
if __name__ == '__main__':
    X, y = load_wine().data, load_wine().target
    rfc = RFC()
    rfc.tuning_parameters(X, y)
    rfc.train(X, y)
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
        X = preprocessing.scale(X)
    rfc = joblib.load("model/rfc.pkl")
    print(rfc.score(X, y))
