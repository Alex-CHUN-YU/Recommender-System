# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from word2vec import Word2Vec as w2v
import MySQLdb
import numpy as np
from cnn import CNN 
from lstm import LSTM
from rcnn import RCNN
from sklearn.model_selection import train_test_split
import json
from sklearn import preprocessing

def main():
	vector_training()
	# save_vector()
	# relationship_model_training()
	# scenario_model_training()

# 訓練向量模型(Using Word2vec)
def vector_training():
	# mysql setting
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	cursor = db.cursor()
	# word2vc traning
	t = w2v()
	t.train_file_setting("segmentation.txt", "result")
	# articles ner
	cursor.execute("SELECT title_ner, content_ner FROM articles_ner Where id >= 1")
	results = cursor.fetchall()
	for result in results:
		t.write_file(result[0], append = True)
		t.write_file(result[1], append = True)
	# movies ner
	cursor.execute("SELECT storyline_ner FROM movies_ner Where id >= 1")
	results = cursor.fetchall()
	for result in results:
		t.write_file(result[0], append = True)
	t.train()
	t.load_model()
	print(t.term_ranking_in_corpus("教師節", 50))
	print(t.term_to_vector("爸爸"))
	print(t.terms_similarity("母親", "母親節"))
	print(1 - t.vectors_similarity(t.term_to_vector("在一起"), t.term_to_vector("過甜蜜")))

# 將向量存入資料庫(For Articles Vector and Movies Vector) 
def save_vector():
	'''
	# 不經過辭典
	sum_of_vec = 5 個 entity 向量總和
	# 經過辭典
	relationship_add_sum = 5 個 entity 向量總和
	relationship_hadamard_sum = 5 個 entity 向量 hardmard
	relationship_add_concatenate = 5 個 entity 分別向量總和在進行 concatenate
	relationship_hadamard_concatenate = 5 個 entity 分別向量 hardmard 在進行 concatenate
	scenario_add_sum = 2 個 entity 向量總和
	scenario_hadamard_sum = 2 個 entity 向量 hardmard
	scenario_add_concatenate = 2 個 entity 分別向量總和在進行 concatenate
	scenario_hadamard_concatenate = 2 個 entity 分別向量 hardmard 在進行 concatenate
	'''
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	db.ping(True)
	cursor = db.cursor()
	# Load Word2Vec Model
	t = w2v()
	t.train_file_setting("segmentation.txt", "result")
	t.load_model()
	dimension = t.size
	# Access Articles NER 221269
	cursor.execute("SELECT id, relation_content_ner, scenario_ner, emotion, event, person_object, time, location, content_ner FROM articles_ner Where id >= 1 and id <= 221269")
	results = cursor.fetchall()
	for result in results:
		article_id = result[0]
		relation_content_ner = result[1]
		scenario_ner = result[2]
		emotion =  result[3]
		event =  result[4]
		person_object =  result[5]
		time =  result[6]
		location =  result[7]
		content_ner = result[8]
		print(article_id)
		# For word2vec Baseline Vec
		sum_of_vec = np.zeros(dimension)
		for content in content_ner.split(" "):
			if content != "":
				sum_of_vec += t.term_to_vector(content)
		# For scenario entity add, hadamard(Scenario model)		
		scenario_add_sum = np.zeros(dimension) 
		scenario_hadamard_sum = np.ones(dimension)
		scenario_add_concatenate = []
		scenario_average_concatenate = []
		scenario_hadamard_concatenate = []
		for scenario in scenario_ner.split(" "):
			if scenario != "":
				scenario_add_sum += t.term_to_vector(scenario)
				scenario_hadamard_sum *= t.term_to_vector(scenario)
		# For relationship all entity add, hadamard, concatenate(Relationship model)
		relationship_add_sum = np.zeros(dimension) 
		relationship_hadamard_sum = np.ones(dimension)
		relationship_add_concatenate = []
		relationship_average_concatenate = []
		relationship_hadamard_concatenate = []
		# 此部分暫且不插入(資料庫欄位已刪)
		# concatenate = []
		for relation in relation_content_ner.split(" "):
			if relation != "":
				# print(relation)
				# print(t.term_to_vector(relation))
				relationship_add_sum += t.term_to_vector(relation)
				relationship_hadamard_sum *= t.term_to_vector(relation)
				# concatenate = np.append(concatenate, t.term_to_vector(relation))
				# if len(concatenate) == 900:
				# 	break;
		# if len(concatenate) < 900:
		# 	concatenate = np.pad(concatenate, (0, 900 - len(concatenate)), 'constant', constant_values = (0)) 
		# For entity add-concatenate, hadamard-concatenate(every entity for relationship, emotion and event for scenario)
		emotion_add = np.zeros(dimension)
		emotion_hadamard = np.ones(dimension)
		emotion_count = 0
		for e in emotion.split(" "):
			if e != "":
				emotion_count += 1
				emotion_add += t.term_to_vector(e)
				emotion_hadamard *= t.term_to_vector(e)
		if emotion_count == 0:
			emotion_count = 1
		print(emotion_add)
		print(emotion_hadamard)
		relationship_add_concatenate = np.append(relationship_add_concatenate, emotion_add)
		relationship_average_concatenate = np.append(relationship_average_concatenate, emotion_add/emotion_count)
		relationship_hadamard_concatenate = np.append(relationship_hadamard_concatenate, emotion_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, emotion_add)
		scenario_average_concatenate = np.append(scenario_average_concatenate, emotion_add/emotion_count)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, emotion_hadamard)
		event_add = np.zeros(dimension)
		event_hadamard = np.ones(dimension)
		event_count = 0
		for e in event.split(" "):
			if e != "":
				event_count += 1
				event_add += t.term_to_vector(e)
				event_hadamard *= t.term_to_vector(e)
		if event_count == 0:
			event_count = 1
		print(event_add)
		print(event_hadamard)
		relationship_add_concatenate = np.append(relationship_add_concatenate, event_add)
		relationship_average_concatenate = np.append(relationship_average_concatenate, event_add/event_count)
		relationship_hadamard_concatenate = np.append(relationship_hadamard_concatenate, event_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, event_add)
		scenario_average_concatenate = np.append(scenario_average_concatenate, event_add/event_count)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, event_hadamard)
		person_object_add = np.zeros(dimension)
		person_object_hadamard = np.ones(dimension)
		person_object_count = 0
		for po in person_object.split(" "):
			if po != "":
				person_object_count += 1
				person_object_add += t.term_to_vector(po)
				person_object_hadamard *= t.term_to_vector(po)
		if person_object_count == 0:
			person_object_count = 1		
		print(person_object_add)
		print(person_object_hadamard)
		relationship_add_concatenate = np.append(relationship_add_concatenate, person_object_add)
		relationship_average_concatenate = np.append(relationship_average_concatenate, person_object_add/person_object_count)
		relationship_hadamard_concatenate = np.append(relationship_hadamard_concatenate, person_object_hadamard)
		time_add = np.zeros(dimension)
		time_hadamard = np.ones(dimension)
		time_count = 0
		for ti in time.split(" "):
			if ti != "":
				time_count += 1
				time_add += t.term_to_vector(ti)
				time_hadamard *= t.term_to_vector(ti)
		if time_count == 0:
			time_count = 1
		print(time_add)
		print(time_hadamard)
		relationship_add_concatenate = np.append(relationship_add_concatenate, time_add)
		relationship_average_concatenate = np.append(relationship_average_concatenate, time_add/time_count)
		relationship_hadamard_concatenate = np.append(relationship_hadamard_concatenate, time_hadamard)
		location_add = np.zeros(dimension)
		location_hadamard = np.ones(dimension)
		location_count = 0
		for l in location.split(" "):
			if l != "":
				location_count += 1
				location_add += t.term_to_vector(l)
				location_hadamard *= t.term_to_vector(l)
		if location_count == 0:
			location_count = 1		
		print(location_add)
		print(location_hadamard)
		relationship_add_concatenate = np.append(relationship_add_concatenate, location_add)
		relationship_average_concatenate = np.append(relationship_average_concatenate, location_add/location_count)
		relationship_hadamard_concatenate = np.append(relationship_hadamard_concatenate, location_hadamard)
		# Insert Data Vector
		# sql = "INSERT INTO articles_vector (id, relationship_add_vec, relationship_hadamard_vec, relationship_entity_add_concatenate_vec, relationship_entity_average_concatenate_vec, relationship_entity_hadamard_concatenate_vec, scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_average_concatenate_vec, scenario_entity_hadamard_concatenate_vec, sum_of_vec) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		# val = (article_id, relationship_add_sum, relationship_hadamard_sum, str(list(relationship_add_concatenate)), str(list(relationship_average_concatenate)), str(list(relationship_hadamard_concatenate)), scenario_add_sum, scenario_hadamard_sum, str(list(scenario_add_concatenate)), str(list(scenario_average_concatenate)), str(list(scenario_hadamard_concatenate)), sum_of_vec)
		sql = "INSERT INTO articles_vector (id, relationship_entity_add_concatenate_vec, relationship_entity_average_concatenate_vec, scenario_entity_add_concatenate_vec, scenario_entity_average_concatenate_vec, sum_of_vec) VALUES (%s, %s, %s, %s, %s, %s)"
		val = (article_id, str(list(relationship_add_concatenate)), str(list(relationship_average_concatenate)), str(list(scenario_add_concatenate)), str(list(scenario_average_concatenate)), sum_of_vec)
		# 過濾 relationship 非 7 且 vector element 皆為 0, 也就是不訓練
		'''cursor.execute("SELECT relationship_type FROM articles Where id ==" + str(article_id) + " and relationship_type !=''")
		relationship_type = cursor.fetchone()
		relationship_type = relationship_type[0]
		if relationship_type != '7':
			print(np.reshape(relationship_average_concatenate, (5, dimension)))
			if np.max(relationship_average_concatenate) == 0.0 and np.min(relationship_average_concatenate) == 0.0:
				print(article_id)
				continue'''
		cursor.execute(sql, val)
		db.commit()

	# Access Movies NER 3722
	cursor.execute("SELECT id, scenario_ner, emotion, event, storyline_ner FROM movies_ner Where id >= 0 and id <= 0")
	results = cursor.fetchall()
	for result in results:
		movie_id = result[0]
		scenario_ner = result[1]
		emotion = result[2]
		event = result[3]
		storyline_ner = result[4]
		print(movie_id)
		# 如果 emotion 和 event 皆為空就不儲存了(也就是 vector element 皆為 0, 不訓練)
		if emotion == "" and event == "":
			continue
		# 之後當成 baseline 的向量
		sum_of_vec = np.zeros(dimension)
		for storyline in storyline_ner.split(" "):
			if storyline != "":
				sum_of_vec += t.term_to_vector(storyline)
		# For all entity add, hadamard
		scenario_add_sum = np.zeros(dimension) 
		scenario_hadamard_sum = np.ones(dimension)
		scenario_add_concatenate = []
		scenario_average_concatenate = []
		scenario_hadamard_concatenate = []
		for scenario in scenario_ner.split(" "):
			if scenario != "":
				scenario_add_sum += t.term_to_vector(scenario)
				scenario_hadamard_sum *= t.term_to_vector(scenario)
		# For entity add-concatenate, hadamard-concatenate
		emotion_add = np.zeros(dimension) 
		emotion_hadamard = np.ones(dimension)
		emotion_count = 0
		for e in emotion.split(" "):
			if e != "":
				emotion_count += 1
				emotion_add += t.term_to_vector(e)
				emotion_hadamard *= t.term_to_vector(e)
		if emotion_count == 0:
			emotion_count = 1
		print(emotion_add)
		print(emotion_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, emotion_add)
		scenario_average_concatenate = np.append(scenario_average_concatenate, emotion_add/emotion_count)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, emotion_hadamard)
		event_add = np.zeros(dimension) 
		event_hadamard = np.ones(dimension)
		event_count = 0
		for e in event.split(" "):
			if e != "":
				event_count += 1
				event_add += t.term_to_vector(e)
				event_hadamard *= t.term_to_vector(e)
		if event_count == 0:
			event_count = 1		
		print(event_add)
		print(event_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, event_add)
		scenario_average_concatenate = np.append(scenario_average_concatenate, event_add/event_count)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, event_hadamard)
		# Insert Data Vector
		# sql = "INSERT INTO movies_vector (id, scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_average_concatenate_vec, scenario_entity_hadamard_concatenate_vec, sum_of_vec) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		# val = (movie_id, scenario_add_sum, scenario_hadamard_sum, scenario_add_concatenate, scenario_average_concatenate, scenario_hadamard_concatenate, sum_of_vec)
		sql = "INSERT INTO movies_vector (id, scenario_entity_add_concatenate_vec, scenario_entity_average_concatenate_vec, sum_of_vec) VALUES (%s, %s, %s, %s)"
		val = (movie_id, scenario_add_concatenate, scenario_average_concatenate, sum_of_vec)
		cursor.execute(sql, val)
		db.commit()

# Relationship Model 提取向量並運用
def relationship_model_training():
	data = []
	target = []
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	cursor = db.cursor()
	cursor.execute("SELECT id, relationship_type FROM articles Where id >= 1 and relationship_type !=''")
	articles = cursor.fetchall()
	for article in articles:
		# Access Articles Vector
		cursor.execute("SELECT id, relationship_add_vec, relationship_hadamard_vec, relationship_entity_add_concatenate_vec, relationship_entity_average_concatenate_vec, relationship_entity_hadamard_concatenate_vec FROM articles_vector Where id =" + str(article[0]))
		vector = cursor.fetchone()
		target_list = article[1].split(",")
		for t in target_list:
			add_vec = []
			hadamard_vec = []
			concatenate_vec = []
			add_concatenate_vec = []
			average_concatenate_vec = []
			hadamard_concatenate_vec = []
			try:
				article_id = vector[0]
				relationship_add_vec = vector[1]
				relationship_hadamard_vec = vector[2]
				# relationship_concatenate_vec = vector[3]
				relationship_entity_add_concatenate_vec = vector[3]
				relationship_entity_average_concatenate_vec = vector[4]
				relationship_entity_hadamard_concatenate_vec = vector[5]
			except:
				break
			for s in relationship_add_vec[1:-1].split(' '):
				try:
					if s != "":
						add_vec.append(float(s))
				except:
					pass
			for s in relationship_hadamard_vec[1:-1].split(' '):
				try:
					if s != "":
						hadamard_vec.append(float(s))
				except:
					pass	
			# for s in relationship_concatenate_vec[1:-1].split(', '):
			# 	try:
			# 		if s != "":
			# 			concatenate_vec.append(float(s))
			# 	except:
			# 		pass
			for s in relationship_entity_add_concatenate_vec[1:-1].split(', '):
				try:
					if s != "":
						add_concatenate_vec.append(float(s))
				except:
					pass
			for s in relationship_entity_average_concatenate_vec[1:-1].split(', '):
				try:
					if s != "":
						average_concatenate_vec.append(float(s))
				except:
					pass
			for s in relationship_entity_hadamard_concatenate_vec[1:-1].split(', '):
				try:
					if s != "":
						hadamard_concatenate_vec.append(float(s))
				except:
					pass

			relationship_add_vec = np.array(add_vec).astype(np.float32)
			relationship_hadamard_vec = np.array(hadamard_vec).astype(np.float32)
			# relationship_concatenate_vec = np.array(concatenate_vec).astype(np.float32)
			relationship_entity_add_concatenate_vec = np.array(add_concatenate_vec).astype(np.float32)
			relationship_entity_average_concatenate_vec = np.array(average_concatenate_vec).astype(np.float32)
			relationship_entity_hadamard_concatenate_vec = np.array(hadamard_concatenate_vec).astype(np.float32)
			# print(relationship_add_vec)
			# print(relationship_hadamard_vec)
			# print(relationship_concatenate_vec)
			# print(1 - t.vectors_similarity(relationship_add_vec, relationship_hadamard_vec))
			data.append(relationship_entity_average_concatenate_vec)
			# Label
			if t == '1':
				target.append([1, 0, 0, 0, 0, 0, 0])
			elif t == '2':
				target.append([0, 1, 0, 0, 0, 0, 0])
			elif t == '3':
				target.append([0, 0, 1, 0, 0, 0, 0])
			elif t == '4':
				target.append([0, 0, 0, 1, 0, 0, 0])
			elif t == '5':
				target.append([0, 0, 0, 0, 1, 0, 0])
			elif t == '6':
				target.append([0, 0, 0, 0, 0, 1, 0])
			elif t == '7':
				target.append([0, 0, 0, 0, 0, 0, 1])
	data = np.array(data)
	target = np.array(target).astype(np.float32)
	print(data.shape)
	print(data.dtype)
	print(data[:3])
	print(target.shape)
	print(target.dtype)
	print(target[:3])
	# # Access Movies Vector
	# cursor.execute("SELECT id, scenario_add_vec, scenario_hadamard_vec FROM movies_vector Where id >= 0 and id <= 0")
	# results = cursor.fetchall()
	# for result in results:
	# 	add_vec = []
	# 	hadamard_vec = []
	# 	movie_id = result[0]
	# 	scenario_add_vec = result[1]
	# 	scenario_hadamard_vec = result[2]
	# 	for s in scenario_add_vec[1:-1].split(' '):
	# 		try:
	# 			if s != "":
	# 				add_vec.append(float(s))
	# 		except:
	# 			pass
	# 	for s in scenario_hadamard_vec[1:-1].split(' '):
	# 		try:
	# 			if s != "":
	# 				hadamard_vec.append(float(s))
	# 		except:
	# 			pass		
	# 	scenario_add_vec = np.array(add_vec).astype(np.float32)
	# 	scenario_hadamard_vec = np.array(hadamard_vec).astype(np.float32)
	# 	print(scenario_add_vec)
	# 	print(scenario_hadamard_vec)
	# 	print(1 - t.vectors_similarity(scenario_add_vec, scenario_hadamard_vec))

	# Data Normalization(目前效果不佳)
	# data = preprocessing.scale(data)
	# CNN Training
	model = CNN()
	model.cross_validation(data, target)
	# 載入參數並顯示出來
	filter_n1 = ''
	neural_node = ''
	with open('model/cnn_parameters') as json_file:
		parameters = json.load(json_file)
		for p in parameters['hyperparameter']:
			filter_n1 = str(p['filter_n1'])
			neural_node = str(p['neural_node'])
	# Testing
	# 如果是 4 筆資料，1 筆測試，3 筆訓練(test data 如果太大, 可能會導致 GPU 暫存不夠)
	X_train, X_test, y_train, y_test = train_test_split(data, target, test_size = 0.01)
	model.test(X_test, y_test, filter_n1 + '_' + neural_node)
	print(model.predict(X_test[:1], filter_n1 + '_' + neural_node))

	print('='*50)
	# RNN Training
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
	# print(model.predict(X_test[:1]))

# Scenario Model 提取向量並運用
def scenario_model_training():
	pass

if __name__ == "__main__":
    main()
