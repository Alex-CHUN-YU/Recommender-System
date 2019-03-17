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
	# vector_training()
	save_vector()
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
	print(t.term_ranking_in_corpus("幸福", 20))
	print(t.term_to_vector("爸爸"))
	print(t.terms_similarity("爸爸", "媽媽"))
	print(1 - t.vectors_similarity(t.term_to_vector("在一起"), t.term_to_vector("過甜蜜")))

# 將向量存入資料庫(For Articles Vector and Movies Vector) 
def save_vector():
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	db.ping(True)
	cursor = db.cursor()
	# Load Word2Vec Model
	t = w2v()
	t.train_file_setting("segmentation.txt", "result")
	t.load_model()
	dimension = t.size
	# Access Articles NER 221269
	cursor.execute("SELECT id, relation_content_ner, emotion, event, person_object, time, location , scenario_ner FROM articles_ner Where id >= 1 and id <= 221269")
	sql = "INSERT INTO articles_vector (id, relationship_add_vec, relationship_hadamard_vec, relationship_entity_add_concatenate_vec, relationship_entity_hadamard_concatenate_vec, scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	results = cursor.fetchall()
	for result in results:
		article_id = result[0]
		relation_content_ner = result[1]
		emotion =  result[2]
		event =  result[3]
		person_object =  result[4]
		time =  result[5]
		location =  result[6]
		scenario_ner = result[7]
		print(article_id)
		# For relationship all entity add, hadamard, concatenate(Relationship model)
		add_sum = np.zeros(dimension) 
		hadamard_sum = np.ones(dimension)
		# 此部分暫且不插入
		# concatenate = []
		for relation in relation_content_ner.split(" "):
			if relation != "":
				# print(relation)
				# print(t.term_to_vector(relation))
				add_sum += t.term_to_vector(relation)
				hadamard_sum *= t.term_to_vector(relation)
				# concatenate = np.append(concatenate, t.term_to_vector(relation))
				# if len(concatenate) == 900:
				# 	break;
		# if len(concatenate) < 900:
		# 	concatenate = np.pad(concatenate, (0, 900 - len(concatenate)), 'constant', constant_values = (0)) 
		# For scenario entity add, hadamard(Scenario model)
		scenario_add_sum = np.zeros(dimension) 
		scenario_hadamard_sum = np.ones(dimension)
		scenario_add_concatenate = []
		scenario_hadamard_concatenate = []
		for scenario in scenario_ner.split(" "):
			if scenario != "":
				scenario_add_sum += t.term_to_vector(scenario)
				scenario_hadamard_sum *= t.term_to_vector(scenario)
		# For entity add-concatenate, hadamard-concatenate(every entity for relationship, emotion and event for scenario)
		add_concatenate = []
		hadamard_concatenate = []
		emotion_add = np.zeros(dimension)
		emotion_hadamard = np.ones(dimension)
		for e in emotion.split(" "):
			if e != "":
				emotion_add += t.term_to_vector(e)
				emotion_hadamard *= t.term_to_vector(e)
		print(emotion_add)
		print(emotion_hadamard)
		add_concatenate = np.append(add_concatenate, emotion_add)
		hadamard_concatenate = np.append(hadamard_concatenate, emotion_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, emotion_add)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, emotion_hadamard)
		event_add = np.zeros(dimension)
		event_hadamard = np.ones(dimension)
		for e in event.split(" "):
			if e != "":
				event_add += t.term_to_vector(e)
				event_hadamard *= t.term_to_vector(e)
		print(event_add)
		print(event_hadamard)
		add_concatenate = np.append(add_concatenate, event_add)
		hadamard_concatenate = np.append(hadamard_concatenate, event_hadamard)
		scenario_add_concatenate = np.append(scenario_add_concatenate, event_add)
		scenario_hadamard_concatenate = np.append(scenario_hadamard_concatenate, event_hadamard)
		person_object_add = np.zeros(dimension)
		person_object_hadamard = np.ones(dimension)
		for po in person_object.split(" "):
			if po != "":
				person_object_add += t.term_to_vector(po)
				person_object_hadamard *= t.term_to_vector(po)
		print(person_object_add)
		print(person_object_hadamard)
		add_concatenate = np.append(add_concatenate, person_object_add)
		hadamard_concatenate = np.append(hadamard_concatenate, person_object_hadamard)
		time_add = np.zeros(dimension)
		time_hadamard = np.ones(dimension)
		for ti in time.split(" "):
			if ti != "":
				time_add += t.term_to_vector(ti)
				time_hadamard *= t.term_to_vector(ti)
		print(time_add)
		print(time_hadamard)
		add_concatenate = np.append(add_concatenate, time_add)
		hadamard_concatenate = np.append(hadamard_concatenate, time_hadamard)
		location_add = np.zeros(dimension)
		location_hadamard = np.ones(dimension)
		for l in location.split(" "):
			if l != "":
				location_add += t.term_to_vector(l)
				location_hadamard *= t.term_to_vector(l)
		print(location_add)
		print(location_hadamard)
		add_concatenate = np.append(add_concatenate, location_add)
		hadamard_concatenate = np.append(hadamard_concatenate, location_hadamard)
		# Insert Data Vector
		val = (article_id, add_sum, hadamard_sum, str(list(add_concatenate)), str(list(hadamard_concatenate)), scenario_add_sum, scenario_hadamard_sum, str(list(scenario_add_concatenate)), str(list(scenario_hadamard_concatenate)))
		cursor.execute(sql, val)
		db.commit()

	# Access Movies NER 3722
	cursor.execute("SELECT id, scenario_ner, emotion, event FROM movies_ner Where id >= 1 and id <= 3722")
	sql = "INSERT INTO movies_vector (id, scenario_add_vec, scenario_hadamard_vec, scenario_entity_add_concatenate_vec, scenario_entity_hadamard_concatenate_vec) VALUES (%s, %s, %s, %s, %s)"
	results = cursor.fetchall()
	for result in results:
		movie_id = result[0]
		scenario_ner = result[1]
		emotion = result[2]
		event = result[3]
		print(movie_id)
		# For all entity add, hadamard
		add_sum = np.zeros(dimension) 
		hadamard_sum = np.ones(dimension)
		for scenario in scenario_ner.split(" "):
			if scenario != "":
				add_sum += t.term_to_vector(scenario)
				hadamard_sum *= t.term_to_vector(scenario)
		# For entity add-concatenate, hadamard-concatenate
		add_concatenate = []
		hadamard_concatenate = []
		emotion_add = np.zeros(dimension) 
		emotion_hadamard = np.ones(dimension)
		for e in emotion.split(" "):
			if e != "":
				emotion_add += t.term_to_vector(e)
				emotion_hadamard *= t.term_to_vector(e)
		print(emotion_add)
		print(emotion_hadamard)
		add_concatenate = np.append(add_concatenate, emotion_add)
		hadamard_concatenate = np.append(hadamard_concatenate, emotion_hadamard)
		event_add = np.zeros(dimension) 
		event_hadamard = np.ones(dimension)
		for e in event.split(" "):
			if e != "":
				event_add += t.term_to_vector(e)
				event_hadamard *= t.term_to_vector(e)
		print(event_add)
		print(event_hadamard)
		add_concatenate = np.append(add_concatenate, event_add)
		hadamard_concatenate = np.append(hadamard_concatenate, event_hadamard)
		val = (movie_id, add_sum, hadamard_sum, add_concatenate, hadamard_concatenate)
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
		cursor.execute("SELECT id, relationship_add_vec, relationship_hadamard_vec, relationship_concatenate_vec, relationship_entity_add_concatenate_vec, relationship_entity_hadamard_concatenate_vec FROM articles_vector Where id =" + str(article[0]))
		vectors = cursor.fetchall()
		exist = False
		for vector in vectors:
			add_vec = []
			hadamard_vec = []
			concatenate_vec = []
			add_concatenate_vec = []
			hadamard_concatenate_vec = []
			article_id = vector[0]
			relationship_add_vec = vector[1]
			relationship_hadamard_vec = vector[2]
			# relationship_concatenate_vec = vector[3]
			relationship_entity_add_concatenate_vec = vector[4]
			relationship_entity_hadamard_concatenate_vec = vector[5]
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
			relationship_entity_hadamard_concatenate_vec = np.array(hadamard_concatenate_vec).astype(np.float32)
			# print(relationship_add_vec)
			# print(relationship_hadamard_vec)
			# print(relationship_concatenate_vec)
			# print(1 - t.vectors_similarity(relationship_add_vec, relationship_hadamard_vec))
			data.append(relationship_entity_add_concatenate_vec)
			exist = True
		if exist:
			# Label
			if article[1] == '1':
				target.append([1, 0, 0, 0, 0, 0, 0])
			elif article[1] == '2':
				target.append([0, 1, 0, 0, 0, 0, 0])
			elif article[1] == '3':
				target.append([0, 0, 1, 0, 0, 0, 0])
			elif article[1] == '4':
				target.append([0, 0, 0, 1, 0, 0, 0])
			elif article[1] == '5':
				target.append([0, 0, 0, 0, 1, 0, 0])
			elif article[1] == '6':
				target.append([0, 0, 0, 0, 0, 1, 0])
			elif article[1] == '7':
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
	print(data[:3])
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
