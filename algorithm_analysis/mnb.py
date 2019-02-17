__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sklearn.datasets import load_iris
from sklearn.naive_bayes import MultinomialNB # Naive Bayes Classifier
from sklearn.model_selection import cross_val_score # cross validation
from sklearn import preprocessing
from sklearn.externals import joblib
import json

# Multinomial Naive Bayes Alogorithm(Probability model, discrete data)
class MNB():
    # MNB Initialize
    def __init__(self):
        #(Validation Parameter) cross_val_score
        self.cv = 10
        # Accuracy（validation_curve application）
        self.score = 0
        self.scoring = 'accuracy'# f1、recall、 precision, your target must binary in sklearn(但貼心的 sklearn 還是有提供 f1_micro、f1_macro...)
        # Normalization        
        self.normalization = False 

    # Find Best Parameter(由於沒有需要 tuning 的參數， 故此部份只有進行計算 score, MNB 視情況來決定是否 normalization)
    def tuning_parameters(self, X, y):
        clf = MultinomialNB()
        #  scale a toy data matrix to the [0, 1] range(MultinomialNB fails when features have negative values)
        if len(X[X < 0]) == 0 :
            scores = cross_val_score(clf, X, y, cv = self.cv, scoring = self.scoring)
            normalizaion_scores = cross_val_score(clf, preprocessing.MinMaxScaler().fit_transform(X), y, cv = self.cv, scoring = self.scoring)
            if normalizaion_scores.mean() > scores.mean():
                self.score = normalizaion_scores.mean()
                self.normalization = True
            else:
                self.score = scores.mean()
        else :
            normalizaion_scores = cross_val_score(clf, preprocessing.MinMaxScaler().fit_transform(X), y, cv = self.cv, scoring = self.scoring)
            self.score = normalizaion_scores.mean()
            self.normalization = True
        print("MNB Cross Validation Finished")
    
    # Produce Model
    def train(self, X, y):
        # Train
        clf = MultinomialNB()
        if self.normalization == True:
            X = preprocessing.MinMaxScaler().fit_transform(X)
        clf.fit(X, y)
        # 透過 joblib 存 model
        joblib.dump(clf, "model/mnb.pkl")
        print("MNB Save Model Finished")
        # 儲存參數、準確性
        parameters = {}
        parameters['scoring'] = []
        parameters['scoring'].append({  
        self.scoring: self.score
        })
        parameters['preprocessing'] = []
        parameters['preprocessing'].append({  
        'normalization': self.normalization
        })
        with open('model/mnb_parameters', 'w', encoding = "utf-8") as mnbf:
            json.dump(parameters, mnbf)
        print("MNB Save Parameters Finished")
            
if __name__ == '__main__':
    X, y = load_iris().data, load_iris().target
    mnb = MNB()
    mnb.tuning_parameters(X, y)
    mnb.train(X, y)
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
        X = preprocessing.MinMaxScaler().fit_transform(X)
    mnb = joblib.load("model/mnb.pkl")
    print(mnb.score(X, y))