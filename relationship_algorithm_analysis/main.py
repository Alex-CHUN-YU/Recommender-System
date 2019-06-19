# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import MySQLdb
import numpy as np
from cnn_e2v_bert import CNN_E2V_BERT
from cnn_e2v_w2v_sg import CNN_E2V_W2V_SG 
from cnn_w2v_w2v_sg import CNN_W2V_W2V_SG  
from sklearn.model_selection import train_test_split
import json
from sklearn import preprocessing
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score

# Relationship Classifer
class Relationship:
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.relationship_e2v_bert_name = 'relationship_e2v_bert'
		self.relationship_e2v_w2v_sg_name = 'relationship_e2v_w2v_sg'
		self.sum_w2v_w2v_sg_name = 'sum_w2v_w2v_sg'
	# relationship feature application
	def relationship(self):
		# self.relationship_model_training(self.relationship_e2v_bert_name)
		self.relationship_model_training(self.relationship_e2v_w2v_sg_name)
		# self.relationship_model_training(self.sum_w2v_w2v_sg_name)
	# Relationship Model Training
	def relationship_model_training(self, feature_type):
		data = []
		target = []
		self.cursor.execute("SELECT id, relationship_type FROM articles Where id >= 1 and id <=500 and relationship_type !=''")
		articles = self.cursor.fetchall()
		for article in articles:
			# Access Articles Vector
			article_id = article[0]
			relationships_type = article[1]
			sql = "SELECT " + feature_type + " FROM articles_vector Where id=" + str(article_id) + " and " + feature_type + " is not null"
			# print(sql)
			self.cursor.execute(sql)
			relationship_feature = self.cursor.fetchone()
			for relationship_type in relationships_type.split(","):
				relationship_feature_vector = []
				relationship_feature = relationship_feature[0]
				for s in relationship_feature[1:-1].split(', '):
					try:
						if s != "":
							relationship_feature_vector.append(float(s))
					except:
						pass				
				if relationship_feature_vector == [] :
					continue
				if np.max(relationship_feature_vector) == 0.0 and np.min(relationship_feature_vector) == 0.0:
					continue
				relationship_feature_vector = np.array(relationship_feature_vector).astype(np.float32)
				# print(relationship_feature_vector[:10])
				# print(relationship_feature_vector.shape)
				data.append(relationship_feature_vector)
				target.append(float(relationship_type))
		data = np.array(data)
		print(data.shape)
		print(data.dtype)
		print(data[:3])
		lb = preprocessing.LabelBinarizer()
		lb.fit([1, 2, 3, 4, 5, 6, 7])
		# print(lb.classes_)
		target = lb.transform(target)
		target = np.array(target)
		print(target.shape)
		print(target.dtype)
		print(target[:3])
		'''# Data Normalization(目前效果不佳)
		# data = preprocessing.scale(data)'''
		# CNN Training
		if feature_type == self.relationship_e2v_bert_name:
			model = CNN_E2V_BERT()
		elif feature_type == self.relationship_e2v_w2v_sg_name:
			model = CNN_E2V_W2V_SG()	
		elif feature_type == self.sum_w2v_w2v_sg_name:
			model = CNN_W2V_W2V_SG()
		# 如果是 4 筆資料，1 筆測試，3 筆訓練(test data 如果太大, 可能會導致 GPU 暫存不夠)
		X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.1)
		# cross validation	
		model.cross_validation(X_train, y_train)
		# 載入參數並顯示出來
		filter_n1 = ''
		neural_node = ''
		with open(model.model_hyperparameter_path) as json_file:
			parameters = json.load(json_file)
			for p in parameters['hyperparameter']:
				filter_n1 = str(p['filter_n1'])
				neural_node = str(p['neural_node'])
		# Testing
		model.test(X_test, y_test, filter_n1 + '_' + neural_node)
		print(model.predict(X_test[:1], filter_n1 + '_' + neural_node))
		y_pred = model.predict(X_test, filter_n1 + '_' + neural_node)
		y_true = np.argmax(y_test, 1)
		self.evaluate_result(feature_type, model, y_pred, y_true)
		'''# RNN Training
		model = LSTM()
		model.cross_validation(data, target)
		# # Testing
		# 如果是 4 筆資料，1 筆測試，3 筆訓練(test data 如果太大, 可能會導致 GPU 暫存不夠)
		# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.01)
		model.test(X_test, y_test)
		print(model.predict(X_test[:1]))

		print('='*50)
		# RNN Training
		# model = RCNN()
		# model.cross_validation(data, target)
		# # Testing
		# # 如果是 4 筆資料，1 筆測試，3 筆訓練(test data 如果太大, 可能會導致 GPU 暫存不夠)
		# X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.01)
		# model.test(X_test, y_test)
		# print(model.predict(X_test[:1]))'''
	# Evaluate Result(accuracy, precision, recall, f1 score)
	def evaluate_result(self, model_name, model, y_pred, y_true):
		# micro precision and recall and f1 score 都一樣, macro 則是每個類別的平均
		accuracy_score_result = accuracy_score(y_true, y_pred)
		precision_score_result = precision_score(y_true, y_pred, average = 'macro')
		recall_score_result = recall_score(y_true, y_pred, average = 'macro')
		f1_score_result = f1_score(y_true, y_pred, average = 'macro')
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
		with open('model/' + model_name + '_evaluate_result', 'w', encoding = "utf-8") as result:
			json.dump(evaluate_result, result)
		print("Evaluate Result is Saved")

if __name__ == "__main__":
	relationship = Relationship()
	relationship.relationship()
