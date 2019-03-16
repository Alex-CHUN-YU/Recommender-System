__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from classification import Classification
from sklearn.model_selection import train_test_split
import sklearn.datasets as ds
import MySQLdb
import numpy as np

# 主要將資料進行分析，選擇出適合的演算法，以及儲存每個演算法 model 和使用到的參數(Parameter)與它的精確性
def main():
	# 1~7 可指定(目前只針對1~6) 另外此部分主要對應過去就是 label 代號
	kinship_data = []
	kinship_target = []
	romantic_relationship_data = []
	romantic_relationship_target = []
	friendship_data = []
	friendship_target = []
	teacher_student_relationship_data = []
	teacher_student_relationship_target = []
	business_relationship_data = []
	business_relationship_target = []
	others_data = []
	others_target = []
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	cursor = db.cursor()
	cursor.execute("SELECT id, relationship_type, scenario_type FROM movies Where id >= 1 and id < 350 and relationship_type !=''")
	movies = cursor.fetchall()	
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
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				kinship_data.append(np.array(add_vec).astype(np.float32))
				kinship_target.append(scenario_type_list[idx])
			if rt == '2':
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				romantic_relationship_data.append(np.array(add_vec).astype(np.float32))
				romantic_relationship_target.append(scenario_type_list[idx])
			if rt == '3':
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				friendship_data.append(np.array(add_vec).astype(np.float32))
				friendship_target.append(scenario_type_list[idx])
			if rt == '4':
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				teacher_student_relationship_data.append(np.array(add_vec).astype(np.float32))
				teacher_student_relationship_target.append(scenario_type_list[idx])
			if rt == '5':
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				business_relationship_data.append(np.array(add_vec).astype(np.float32))
				business_relationship_target.append(scenario_type_list[idx])
			if rt == '6':
				add_vec = []
				cursor.execute("SELECT scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec FROM movies_vector Where id =" + str(movies_id))
				movies_vector = cursor.fetchone()
				try:
					scenario_add_vec = movies_vector[0]
				except:
					continue
				for s in scenario_add_vec[1:-1].split(' '):
					try:
						if s != "":
							add_vec.append(float(s))
					except:
						pass
				others_data.append(np.array(add_vec).astype(np.float32))
				others_target.append(scenario_type_list[idx])
	kinship_data = np.array(kinship_data)
	kinship_target = np.array(kinship_target).astype(np.float32)
	romantic_relationship_data = np.array(romantic_relationship_data)
	romantic_relationship_target = np.array(romantic_relationship_target).astype(np.float32)
	friendship_data = np.array(friendship_data)
	friendship_target = np.array(friendship_target).astype(np.float32)
	teacher_student_relationship_data = np.array(teacher_student_relationship_data)
	teacher_student_relationship_target = np.array(teacher_student_relationship_target).astype(np.float32)
	business_relationship_data = np.array(business_relationship_data)
	business_relationship_target = np.array(business_relationship_target).astype(np.float32)
	others_data = np.array(others_data)
	others_target = np.array(others_target).astype(np.float32)
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

	# name = 'kinship'
	# print(kinship_data.shape)
	# print(kinship_target.shape)
	# training(name, kinship_data, kinship_target)
	name = 'romantic_relationship'
	print(romantic_relationship_data.shape)
	print(romantic_relationship_target.shape)
	training(name, romantic_relationship_data, romantic_relationship_target)
	# name = 'friendship'
	# print(friendship_data.shape)
	# print(friendship_target.shape)
	# training(name, friendship_data, friendship_target)
	# name = 'teacher_student_relationship'
	# print(teacher_student_relationship_data.shape)
	# print(teacher_student_relationship_target.shape)
	# training(name, teacher_student_relationship_data, teacher_student_relationship_target)
	# name = 'business_relationship'
	# print(business_relationship_data.shape)
	# print(business_relationship_target.shape)
	# training(name, business_relationship_data, business_relationship_target)
	# name = 'others'
	# print(others_data.shape)
	# print(others_target.shape)
	# training(name, others_data, others_target)

def training(name, data, target):
	clf = Classification(data, target, name)
	X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.25)
	clf.knn_model()
	clf.nb_model()
	clf.mnb_model()
	clf.rfc_model()
	clf.svm_model()
	clf.find_best_estimator(X_test, y_test)

if __name__ == "__main__":
    main()
