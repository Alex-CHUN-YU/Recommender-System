__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from classification import Classification
from sklearn.model_selection import train_test_split
import sklearn.datasets as ds
import MySQLdb
import numpy as np

class Scenario():
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.kinship_name = "kinship"
		self.kinship_data = []
		self.kinship_target = []
		self.romantic_relationship_name = "romantic_relationship"
		self.romantic_relationship_data = []
		self.romantic_relationship_target = []
		self.friendship_name = "friendship"
		self.friendship_data = []
		self.friendship_target = []
		self.teacher_student_relationship_name = "teacher_student_relationship"
		self.teacher_student_relationship_data = []
		self.teacher_student_relationship_target = []
		self.business_relationship_name = "business_relationship"
		self.business_relationship_data = []
		self.business_relationship_target = []
		self.others_name = "others"
		self.others_data = []
		self.others_target = []
		self.scenario_e2v_bert_name = 'scenario_e2v_bert'
		self.scenario_e2v_w2v_sg_name = 'scenario_e2v_w2v_sg'
		self.sum_w2v_w2v_sg_name = 'sum_w2v_w2v_sg'
	def scenario(self):
		# self.scenario_model_training(self.scenario_e2v_bert_name)
		self.scenario_model_training(self.scenario_e2v_w2v_sg_name)
		# self.scenario_model_training(self.sum_w2v_w2v_sg_name)
	# 主要將資料進行分析，選擇出適合的演算法，以及儲存每個演算法 model 和使用到的參數(Parameter)與它的精確性
	def scenario_model_training(self, feature_type):
		# 1~7 可指定(目前只針對1~6) 另外此部分主要對應過去就是 label 代號
		self.cursor.execute("SELECT id, relationship_type, scenario_type FROM movies Where id >= 1 and id <= 1171 and relationship_type !='' and scenario_type !=''")
		movies = self.cursor.fetchall()	
		for movie in movies:
			movies_id = movie[0]
			print("id:" + str(movies_id))
			relationship_type = movie[1]
			relationship_type_list = relationship_type.split(',')
			print("relationship_type:" + relationship_type)
			scenario_type = movie[2]
			scenario_type_list = scenario_type.split(',')
			print("scenario_type:" + scenario_type)
			for idx, rt in enumerate(relationship_type_list):
				if rt == '1':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.kinship_data.append(np.array(training_data).astype(np.float32))
					self.kinship_target.append(scenario_type_list[idx])
				elif rt == '2':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.romantic_relationship_data.append(np.array(training_data).astype(np.float32))
					self.romantic_relationship_target.append(scenario_type_list[idx])
				elif rt == '3':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.friendship_data.append(np.array(training_data).astype(np.float32))
					self.friendship_target.append(scenario_type_list[idx])
				elif rt == '4':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.teacher_student_relationship_data.append(np.array(training_data).astype(np.float32))
					self.teacher_student_relationship_target.append(scenario_type_list[idx])
				elif rt == '5':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.business_relationship_data.append(np.array(training_data).astype(np.float32))
					self.business_relationship_target.append(scenario_type_list[idx])
				elif rt == '6':
					training_data = self.produce_training_data(movies_id, feature_type)
					if training_data == []:
						continue
					self.others_data.append(np.array(training_data).astype(np.float32))
					self.others_target.append(scenario_type_list[idx])
		self.kinship_data = np.array(self.kinship_data)
		self.kinship_target = np.array(self.kinship_target).astype(np.float32)
		self.romantic_relationship_data = np.array(self.romantic_relationship_data)
		self.romantic_relationship_target = np.array(self.romantic_relationship_target).astype(np.float32)
		self.friendship_data = np.array(self.friendship_data)
		self.friendship_target = np.array(self.friendship_target).astype(np.float32)
		self.teacher_student_relationship_data = np.array(self.teacher_student_relationship_data)
		self.teacher_student_relationship_target = np.array(self.teacher_student_relationship_target).astype(np.float32)
		self.business_relationship_data = np.array(self.business_relationship_data)
		self.business_relationship_target = np.array(self.business_relationship_target).astype(np.float32)
		self.others_data = np.array(self.others_data)
		self.others_target = np.array(self.others_target).astype(np.float32)
		# print("kinship:")
		# print(self.kinship_data[0][:3])
		# print(self.kinship_target[:3])
		# print(self.kinship_data.shape)
		# print(self.kinship_target.shape)
		# print("romantic_relationship:")
		# print(self.romantic_relationship_data[0][:3])
		# print(self.romantic_relationship_target[:3])
		# print(self.romantic_relationship_data.shape)
		# print(self.romantic_relationship_target.shape)
		# print("friendship:")
		# print(self.friendship_data[0][:3])
		# print(self.friendship_target[:3])
		# print(self.friendship_data.shape)
		# print(self.friendship_target.shape)
		# print("teacher_student_relationship:")
		# print(self.teacher_student_relationship_data[0][:3])
		# print(self.teacher_student_relationship_target[:3])
		# print(self.teacher_student_relationship_data.shape)
		# print(self.teacher_student_relationship_target.shape)
		# print("business_relationship:")
		# print(self.business_relationship_data[0][:3])
		# print(self.business_relationship_target[:3])
		# print(self.business_relationship_data.shape)
		# print(self.business_relationship_target.shape)
		# print("others:")
		# print(self.others_data[0][:3])
		# print(self.others_target[:3])
		# print(self.others_data.shape)
		# print(self.others_target.shape)
		print("="*10)
		print(self.kinship_data.shape)
		print(self.kinship_target.shape)
		self.training(self.kinship_name, self.kinship_data, self.kinship_target)
		print(self.romantic_relationship_data.shape)
		print(self.romantic_relationship_target.shape)
		self.training(self.romantic_relationship_name, self.romantic_relationship_data, self.romantic_relationship_target)
		print(self.friendship_data.shape)
		print(self.friendship_target.shape)
		self.training(self.friendship_name, self.friendship_data, self.friendship_target)
		# print(teacher_student_relationship_data.shape)
		# print(teacher_student_relationship_target.shape)
		# self.training(self.teacher_student_relationship_name, teacher_student_relationship_data, teacher_student_relationship_target)
		print(self.business_relationship_data.shape)
		print(self.business_relationship_target.shape)
		self.training(self.business_relationship_name, self.business_relationship_data, self.business_relationship_target)
		print(self.others_data.shape)
		print(self.others_target.shape)
		self.training(self.others_name, self.others_data, self.others_target)
	# 訓練資料集
	def produce_training_data(self, movies_id, feature_type):
		vector = []
		sql = "SELECT " + feature_type + " FROM movies_vector Where id =" + str(movies_id) + " and " + feature_type + " != ''"
		self.cursor.execute(sql)
		movies_vector = self.cursor.fetchone()
		for s in movies_vector[0][1:-1].split(', '):
			try:
				if s != "":
					vector.append(float(s))
			except:
				pass
		if np.max(vector) == 0.0 and np.min(vector) == 0.0:
			vector = []
		return vector	
	# 使用演算法訓練
	def training(self, name, data, target):
		X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.1)
		clf = Classification(X_train, y_train, name)
		# clf.knn_model()
		clf.nb_model()
		# clf.mnb_model()
		clf.rfc_model()
		clf.svm_model()
		clf.find_best_estimator(X_test, y_test)

if __name__ == "__main__":
    scenario = Scenario()
    scenario.scenario()
