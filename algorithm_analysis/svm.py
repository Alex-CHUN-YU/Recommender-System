__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sklearn.datasets import load_digits
from sklearn.svm import SVC
from sklearn import preprocessing
from sklearn.model_selection import validation_curve
from sklearn.model_selection import GridSearchCV
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import json

# Support Vector Machine Alogorithm
class SVM():
    # SVM Initialize
    def __init__(self, name):
        self.model_name = 'model/' + name + '_svm'
        self.image_name = 'image/' + name + '_svm'
        # SVM Parameter
        self.C = 1.0
        self.kernel = 'linear'
        self.gamma = 'auto'
        self.degree = 3
        self.coef0 = 0.0
        self.shrinking = True
        self.probability = False
        self.tol = 0.001
        self.cache_size = 200
        self.class_weight = None
        self.verbose = False
        self.max_iter = -1 
        self.decision_function_shape = 'ovr'
        self.random_state = None
        #(Validation Parameter) GridSearchCV
        self.n_jobs = -1
        self.cv = 10
        self.Crange = [1, 10, 100, 1000]# 4
        self.gamma_range = np.logspace(-6, -2.4, 5)# 5
        # Accuracy(GridSearchCV application)
        self.score = 0
        self.scoring = 'accuracy'# f1、recall、 precision, your target must binary in sklearn(但貼心的 sklearn 還是有提供 f1_micro、f1_macro...)
        # Normalization        
        self.normalization = False 

    def tuning_parameters(self, X, y):
        # 第一次 tuning (找出 best C 和 best kernel 和 best gamma)
        # C 懲罰系數，即是對誤差的寬容度(c越高，越不能容忍出現誤差,容易 overfitting 。C越小，容易 underfitting)
        # gamma 是 RBF Kernel 所使用的參數，隱含著決定數據映射到新的特徵空間分佈，gamma越大，支持向量越少，gamma 值越小支持向量越多。支持向量的個數影響訓練與預測的速度。
        clf = SVC(C = self.C, kernel = self.kernel, degree = self.degree, gamma = self.gamma, coef0 = self.coef0,
                  shrinking = self.shrinking, probability = self.probability, tol = self.tol, cache_size = self.cache_size,
                  class_weight = self.class_weight, verbose = self.verbose, max_iter = self.max_iter, 
                  decision_function_shape = self.decision_function_shape, random_state = self.random_state)
        parameter_candidates = [# Set the parameter candidates
            {'C': self.Crange, 'kernel': ['rbf'], 'gamma': self.gamma_range},# 4 * 5
            {'C': self.Crange, 'kernel': ['linear']},# 1 * 4
            {'C': self.Crange, 'kernel': ['poly']},# 1 * 4
            {'C': self.Crange, 'kernel': ['sigmoid']}]# 1 * 4
        clf_gscv = GridSearchCV(estimator = clf, param_grid = parameter_candidates, cv = self.cv, scoring = self.scoring, n_jobs = self.n_jobs)# Create a classifier with the parameter candidates
        clf_gscv.fit(X, y)# No Normalization
        normalization_clf_gscv = clf_gscv
        normalization_clf_gscv.fit(preprocessing.scale(X), y)# Normalization
        if normalization_clf_gscv.best_score_ > clf_gscv.best_score_:
            self.normalization = True
            X = preprocessing.scale(X)
            self.C = normalization_clf_gscv.best_estimator_.C
            self.gamma = normalization_clf_gscv.best_estimator_.gamma
            self.kernel = normalization_clf_gscv.best_estimator_.kernel
            self.score = normalization_clf_gscv.best_score_
            clf = normalization_clf_gscv
        else:
            self.C = clf_gscv.best_estimator_.C
            self.gamma = clf_gscv.best_estimator_.gamma
            self.kernel = clf_gscv.best_estimator_.kernel
            self.score = clf_gscv.best_score_
            clf = clf_gscv
            # Print out the results 
#             print('Best score for training data:', clf_gscv.best_score_)
#             print('Best `C`:',clf_gscv.best_estimator_.C)
#             print('Best kernel:',clf_gscv.best_estimator_.kernel)
#             print('Best `gamma`:',clf_gscv.best_estimator_.gamma)
#         print(normalization_clf_gscv.best_score_)
        # For RBF Graph
#         print(clf.cv_results_)
        plt.title("Validation Curve with SVM")
        # 4 * 5 
        length = len(self.Crange) * len(self.gamma_range)
        if self.kernel == 'rbf':
            plt.xlabel("Value Of gamma For SVM " + self.kernel)
            plt.ylabel(self.scoring)
            # 4 * 5 
            test_mean_scores = np.array(clf.cv_results_['mean_test_score'][:length]).reshape(len(self.Crange), len(self.gamma_range))
            test_std_scores = np.array(clf.cv_results_['std_test_score'][:length]).reshape(len(self.Crange), len(self.gamma_range))
            # train_mean_scores = np.array(clf.cv_results_['mean_train_score'][:length]).reshape(len(self.Crange), len(self.gamma_range))
            # train_std_scores = np.array(clf.cv_results_['std_train_score'][:length]).reshape(len(self.Crange), len(self.gamma_range))
            for ind, i in enumerate(self.Crange):
                plt.plot(self.gamma_range, test_mean_scores[ind], "-o", label = 'C: ' + str(i))
                plt.fill_between(self.gamma_range, test_mean_scores[ind] - test_std_scores[ind], 
                         test_mean_scores[ind] + test_std_scores[ind], alpha = 0.2)
                # plt.plot(self.gamma_range, train_mean_scores[ind], "-o", label = 'C: ' + str(i))
                # plt.fill_between(self.gamma_range, train_mean_scores[ind] - train_std_scores[ind], 
                #          train_mean_scores[ind] + train_std_scores[ind], alpha = 0.2)
#             print(clf.cv_results_['mean_test_score'][:20])
#             print(clf.cv_results_['std_test_score'][:20])
        # For linear、poly、sigmoid Graph
        else:
            plt.xlabel("Value Of C For SVM " + self.kernel)
            plt.ylabel(self.scoring)
            # 1 * 4
            if self.kernel == 'linear':
                plt.plot(self.Crange, clf.cv_results_['mean_test_score'][length:length + len(self.Crange)], "-o", label = "Validation score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_test_score'][length:length + len(self.Crange)] - clf.cv_results_['std_test_score'][length:length + len(self.Crange)], 
                         clf.cv_results_['mean_test_score'][length:length + len(self.Crange)] + clf.cv_results_['std_test_score'][length:length + len(self.Crange)], alpha = 0.2)
                plt.plot(self.Crange, clf.cv_results_['mean_train_score'][length:length + len(self.Crange)], "-o", label = "Training score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_train_score'][length:length + len(self.Crange)] - clf.cv_results_['std_train_score'][length:length + len(self.Crange)], 
                         clf.cv_results_['mean_train_score'][length:length + len(self.Crange)] + clf.cv_results_['std_train_score'][length:length + len(self.Crange)], alpha = 0.2)
#                 print(clf.cv_results_['mean_test_score'][20:24])
#                 print(clf.cv_results_['std_test_score'][20:24])
            elif self.kernel == 'poly':
                plt.plot(self.Crange, clf.cv_results_['mean_test_score'][length + len(self.Crange):length + len(self.Crange) * 2], "-o", label = "Validation score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_test_score'][length + len(self.Crange):length + len(self.Crange) * 2] - clf.cv_results_['std_test_score'][length + len(self.Crange):length + len(self.Crange) * 2], 
                         clf.cv_results_['mean_test_score'][length + len(self.Crange):length + len(self.Crange) * 2] + clf.cv_results_['std_test_score'][length + len(self.Crange):length + len(self.Crange) * 2], alpha = 0.2)
                plt.plot(self.Crange, clf.cv_results_['mean_train_score'][length + len(self.Crange):length + len(self.Crange) * 2], "-o", label = "Training score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_train_score'][length + len(self.Crange):length + len(self.Crange) * 2] - clf.cv_results_['std_train_score'][length + len(self.Crange):length + len(self.Crange) * 2], 
                         clf.cv_results_['mean_train_score'][length + len(self.Crange):length + len(self.Crange) * 2] + clf.cv_results_['std_train_score'][length + len(self.Crange):length + len(self.Crange) * 2], alpha = 0.2)
#                 print(clf.cv_results_['mean_test_score'][24:28])
#                 print(clf.cv_results_['std_test_score'][24:28])
            elif self.kernel == 'sigmoid':
                plt.plot(self.Crange, clf.cv_results_['mean_test_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], "-o", label = "Validation score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_test_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3] - clf.cv_results_['std_test_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], 
                         clf.cv_results_['mean_test_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3] + clf.cv_results_['std_test_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], alpha = 0.2)
                plt.plot(self.Crange, clf.cv_results_['mean_train_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], "-o", label = "Training score")
                plt.fill_between(self.Crange, clf.cv_results_['mean_train_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3] - clf.cv_results_['std_train_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], 
                         clf.cv_results_['mean_train_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3] + clf.cv_results_['std_train_score'][length + len(self.Crange) * 2 :length + len(self.Crange) * 3], alpha = 0.2)
#                 print(clf.cv_results_['mean_test_score'][28:32])
#                 print(clf.cv_results_['std_test_score'][28:32])
        plt.legend(loc = "best")
        plt.savefig(self.image_name + '.png')
        plt.close()
        print("SVM Save Image Finished")
        print("SVM Tuning Parameters Finished")
            
    # Produce Model
    def train(self, X, y):
        # Train
        clf = SVC(C = self.C, kernel = self.kernel, degree = self.degree, gamma = self.gamma, coef0 = self.coef0,
                  shrinking = self.shrinking, probability = self.probability, tol = self.tol, cache_size = self.cache_size,
                  class_weight = self.class_weight, verbose = self.verbose, max_iter = self.max_iter, 
                  decision_function_shape = self.decision_function_shape, random_state = self.random_state)
        if self.normalization == True:
            X = preprocessing.scale(X)
        clf.fit(X, y)
        # 透過 joblib 存 model
        joblib.dump(clf, self.model_name + '.pkl')
        print("SVM Save Model Finished")
        # 儲存參數、準確性
        parameters = {}
        parameters['parameters'] = []
        parameters['parameters'].append({  
        'C': self.C,
        'kernel': self.kernel,
        'gamma': self.gamma
        })
        parameters['scoring'] = []
        parameters['scoring'].append({  
        self.scoring: self.score
        })
        parameters['preprocessing'] = []
        parameters['preprocessing'].append({  
        'normalization': self.normalization
        })
        with open(self.model_name + '_parameters', 'w', encoding = "utf-8") as svmf:
            json.dump(parameters, svmf)
        print("SVM Save Parameters Finished")
            
if __name__ == '__main__':
    X, y = load_digits().data, load_digits().target
    name = 'digits'
    svm = SVM(name)
    svm.tuning_parameters(X, y)
    svm.train(X, y)
    # 載入參數並顯示出來
    with open(svm.model_name + '_parameters') as json_file:  
        data = json.load(json_file)
        for p in data['parameters']:
            print('C: ' + str(p['C']))
            print('kernel: ' + p['kernel'])
            print('gamma: ' + str(p['gamma']))
        # 不同的評分標準 key 要做更改
        for s in data['scoring']:
            print('accuracy: ' + str(s['accuracy']))
        for p in data['preprocessing']:
            print('normalization: ' + str(p['normalization']))
            normalization = p['normalization']
    # 載入 model 並去預測
    if normalization == True:
        X = preprocessing.scale(X)
    svm = joblib.load(svm.model_name + '.pkl')
    print(svm.score(X, y))
