__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sklearn.datasets import load_wine
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.model_selection import validation_curve
import numpy as np
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import json
import matplotlib
matplotlib.use('Agg')

# K Nearest Neighbor Alogorithm
class KNN():
    # KNN Initialize
    def __init__(self, name):
        self.model_name = 'model/' + name + '_knn'
        self.image_name = 'image/' + name + '_knn'
        # KNN Parameter
        self.n_neighbors = 5
        self.weights = 'uniform'
        self.algorithm = 'auto'
        self.leaf_size = 30
        self.p = 2
        self.metric = 'minkowski'
        self.metric_params = None
        self.n_jobs = -1
        #(Validation Parameter) validation_curve
        self.cv = 10
        self.k_range = range(1, 20)
        # Accuracy（validation_curve application）
        self.score = 0
        self.scoring = 'accuracy'# f1、recall、 precision, your target must binary in sklearn(但貼心的 sklearn 還是有提供 f1_micro、f1_macro...)
        # Normalization        
        self.normalization = False 

    # Find Best Parameter(Normalization 有時是必要的)
    def tuning_parameters(self, X, y):
        # 第一次 tuning(找出 best n_neighbors 並畫圖)
        # n_neighbors 為 k 的數量。(default = 5)
        # wieght 權重可分為 'uniform'(每個鄰居權重一樣)、'distance'(每個鄰居會因距離而與權重成反比)、'[callable]'(使用者自定義的函式)。(default = 'uniform' )
        # algorithm 演算法可分為 'ball_tree'、'kd_tree'、'brute'、'auto'(透過 fit 根據數值選擇合適的演算法)
        # leaf_size 葉子的節點數量(ball tree or kd tree)。(default = 30)
        # p 為 Minkowski metric 公式所需求之大小(當 p = 1 時，就是曼哈頓距離、當 p = 2 時，就是歐氏距離、當 p→∞ 時，就是切比雪夫距離)。(default = 2)
        # metric 距離公式的選擇(default = 'minkowski')
        # metric_params 主要針對特殊的 metric 所需求而增加的特殊參數。(default = None)
        # n_jobs 線程數量(default = 1, 如為 -1 為 CPU 內核數)
        clf = KNeighborsClassifier(n_neighbors = self.n_neighbors, weights = self.weights, algorithm = self.algorithm,
                                   leaf_size = self.leaf_size,p = self.p, metric = self.metric, metric_params = self.metric_params,
                                   n_jobs = self.n_jobs)
        # n_neighbors Parameter     
        train_scores, valid_scores = validation_curve(clf, X, y, "n_neighbors", self.k_range, cv = self.cv, scoring = self.scoring, n_jobs = self.n_jobs)# No Nomalization  
        train_scores_mean = np.mean(train_scores, axis = 1)
        train_scores_std = np.std(train_scores, axis = 1)# 標準差為資料的離散程度, 一個較大的標準差，代表大部分的數值和其平均值之間差異較大；一個較小的標準差，代表這些數值較接近平均值
        valid_scores_mean = np.mean(valid_scores, axis = 1)
        valid_scores_std = np.std(valid_scores, axis = 1)
        normalization_train_scores, normalization_valid_scores = validation_curve(clf, preprocessing.scale(X), y, "n_neighbors", self.k_range, cv = self.cv, scoring = self.scoring, n_jobs = self.n_jobs)# Normalization
        normalization_train_scores_mean = np.mean(normalization_train_scores, axis = 1)
        normalization_valid_scores_mean = np.mean(normalization_valid_scores, axis = 1)
        # 判斷是否需要 Normalization        
        if normalization_valid_scores_mean.max() > valid_scores_mean.max():
              train_scores_mean = normalization_train_scores_mean                
              valid_scores_mean = normalization_valid_scores_mean
              self.normalization = True
              X = preprocessing.scale(X)
        max_value = 0
        for idx, val in enumerate(valid_scores_mean):
            if val > max_value:
                max_value = val
                max_index = idx
        #print(max_value, end = ' ')
        #print(self.k_range[max_index])
        self.n_neighbors = self.k_range[max_index]
        self.score = max_value
        '''print(train_scores_mean.max())
        print(train_scores_std.max())
        print(valid_scores_mean.max())
        print(valid_scores_std.max())'''
        plt.title("Validation Curve with KNN")
        plt.xlabel("Value Of n For KNN")
        plt.ylabel(self.scoring)       
        #plt.ylim(0.0, 1.1)# 設置y座標軸範圍
        #lw = 1# lw指的是粗细
        plt.plot(self.k_range, train_scores_mean, "-o", color = 'r', label = "Training score")# 畫出平均數值
        plt.fill_between(self.k_range, train_scores_mean - train_scores_std,# 畫出離散程度
                         train_scores_mean + train_scores_std, alpha = 0.2, color = "darkorange")
        plt.plot(self.k_range, valid_scores_mean, "-o", color = 'b', label = "Validation score")
        plt.fill_between(self.k_range, valid_scores_mean - valid_scores_std, 
                         valid_scores_mean + valid_scores_std, alpha = 0.2, color = "navy")      
        plt.legend(loc = "best")
        # save image
        plt.savefig(self.image_name + '.png')
        plt.close()
        print("KNN Save Image Finished")
        print("KNN Tuning Parameters Finished")
    
    # Produce Model
    def train(self, X, y):
        # Train
        clf = KNeighborsClassifier(n_neighbors = self.n_neighbors, weights = self.weights, algorithm = self.algorithm,
                                   leaf_size = self.leaf_size,p = self.p, metric = self.metric, metric_params = self.metric_params,
                                   n_jobs = self.n_jobs)
        #print(self.n_neighbors)
        if self.normalization == True:
            X = preprocessing.scale(X)
        clf.fit(X, y)
        # 透過 joblib 存 model
        joblib.dump(clf, self.model_name + '.pkl')
        print("KNN Save Model Finished")
        # 儲存參數、準確性
        parameters = {}
        parameters['parameters'] = []
        parameters['parameters'].append({  
        'n_neighbors': self.n_neighbors
        })
        parameters['scoring'] = []
        parameters['scoring'].append({  
        'valid_score': self.score
        })
        parameters['preprocessing'] = []
        parameters['preprocessing'].append({  
        'normalization': self.normalization
        })
        with open(self.model_name + '_parameters', 'w', encoding = "utf-8") as knnf:
            json.dump(parameters, knnf)
        print("KNN Save Parameters Finished")
            
if __name__ == '__main__':
    X, y = load_wine().data, load_wine().target
    name = 'wine'
    knn = KNN(name)
    knn.tuning_parameters(X, y)
    knn.train(X, y)
    # 載入參數並顯示出來
    with open(knn.model_name + '_parameters') as json_file:  
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
        X = preprocessing.scale(X)
    knn = joblib.load(knn.model_name + '.pkl')
    print(knn.score(X, y))
    
