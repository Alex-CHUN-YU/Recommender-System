__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from sklearn.datasets import load_iris
from sklearn.naive_bayes import GaussianNB # Naive Bayes Classifier
from sklearn.model_selection import cross_val_score # cross validation
from sklearn.externals import joblib
import json

# Naive Bayes Alogorithm(Probability model, continuous data)
class NB():
    # NB Initialize
    def __init__(self, name):
        self.model_name = 'model/' + name + '_nb'
        #(Validation Parameter) cross_val_score
        self.cv = 10
        # Accuracy（validation_curve application）
        self.score = 0
        self.scoring = 'accuracy'# f1、recall、 precision, your target must binary in sklearn(但貼心的 sklearn 還是有提供 f1_micro、f1_macro...)

    # Find Best Parameter(由於沒有需要 tuning 的參數， 故此部份只有進行計算 score, NB 有沒有 normalization 都沒差)
    def tuning_parameters(self, X, y):
        clf = GaussianNB()
        scores = cross_val_score(clf, X, y, cv = self.cv, scoring = self.scoring)
        self.score = scores.mean()
        print("NB Cross Validation Finished")
    
    # Produce Model
    def train(self, X, y):
        # Train
        clf = GaussianNB()
        clf.fit(X, y)
        # 透過 joblib 存 model
        joblib.dump(clf, self.model_name + '.pkl')
        print("NB Save Model Finished")
        # 儲存參數、準確性
        parameters = {}
        parameters['scoring'] = []
        parameters['scoring'].append({  
        'valid_score': self.score
        })
        with open(self.model_name + '_parameters', 'w', encoding = "utf-8") as nbf:
            json.dump(parameters, nbf)
        print("NB Save Parameters Finished")
            
if __name__ == '__main__':
    X, y = load_iris().data, load_iris().target
    name = 'iris'
    nb = NB(name)
    nb.tuning_parameters(X, y)
    nb.train(X, y)
    # 載入參數並顯示出來
    with open(nb.model_name + '_parameters') as json_file:  
        data = json.load(json_file)
        # 不同的評分標準 key 要做更改
        for s in data['scoring']:
            print('valid_score: ' + str(s['valid_score']))
    # 載入 model 並去預測
    nb = joblib.load(nb.model_name + '.pkl')
    print(nb.score(X, y))
    
