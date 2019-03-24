__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from classification import Classification
from sklearn.model_selection import train_test_split
import sklearn.datasets as ds
import MySQLdb
import numpy as np

class Main():
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
	# 主要將資料進行分析，選擇出適合的演算法，以及儲存每個演算法 model 和使用到的參數(Parameter)與它的精確性
	def main(self):
		# 1~7 可指定(目前只針對1~6) 另外此部分主要對應過去就是 label 代號
		self.cursor.execute("SELECT id, relationship_type, scenario_type FROM movies Where id >= 1 and id < 350 and relationship_type !=''")
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
					training_data = self.produce_training_data(movies_id)
					if training_data == []:
						continue
					self.kinship_data.append(np.array(training_data).astype(np.float32))
					self.kinship_target.append(scenario_type_list[idx])
				elif rt == '2':
					training_data = self.produce_training_data(movies_id)
					if training_data == []:
						continue
					self.romantic_relationship_data.append(np.array(training_data).astype(np.float32))
					self.romantic_relationship_target.append(scenario_type_list[idx])
				elif rt == '3':
					training_data = self.produce_training_data(movies_id)
					if training_data == []:
						continue
					self.friendship_data.append(np.array(training_data).astype(np.float32))
					self.friendship_target.append(scenario_type_list[idx])
				elif rt == '4':
					training_data = self.produce_training_data(movies_id)
					if training_data == []:
						continue
					self.teacher_student_relationship_data.append(np.array(training_data).astype(np.float32))
					self.teacher_student_relationship_target.append(scenario_type_list[idx])
				elif rt == '5':
					training_data = self.produce_training_data(movies_id)
					if training_data == []:
						continue
					self.business_relationship_data.append(np.array(training_data).astype(np.float32))
					self.business_relationship_target.append(scenario_type_list[idx])
				elif rt == '6':
					training_data = self.produce_training_data(movies_id)
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
		# print(kinship_data)
		# print(kinship_target)
		# print(kinship_data.shape)
		# print(kinship_target.shape)
		# print(friendship_data)
		# print(friendship_target)
		# print(teacher_student_relationship_data)
		# print(teacher_student_relationship_target)
		# print(business_relationship_data)
		# print(business_relationship_target)
		# print(others_data)
		# print(others_target)
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
	def produce_training_data(self, movies_id):
		add_vec = []
		self.cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
		movies_vector = self.cursor.fetchone()
		try:
			scenario_add_vec = movies_vector[2]
		except:
			return add_vec
		for s in scenario_add_vec[1:-1].split(' '):
			try:
				if s != "":
					add_vec.append(float(s))
			except:
				pass
		return add_vec	
	# 使用演算法訓練
	def training(self, name, data, target):
		clf = Classification(data, target, name)
		X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.25)
		clf.knn_model()
		clf.nb_model()
		clf.mnb_model()
		clf.rfc_model()
		clf.svm_model()
		clf.find_best_estimator(X_test, y_test)

if __name__ == "__main__":
    main = Main()
    main.main()
