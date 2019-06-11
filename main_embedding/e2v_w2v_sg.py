# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from word2vec import Word2Vec as w2v
import MySQLdb
import numpy as np
# Entity to Vector
class E2V_W2V_SG():
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.articles = []
		self.movies = []
	# main function
	def e2v_w2v_sg(self):
		self.load_data()
		self.vector_training()
		# self.save_vector()
	# load data
	def load_data(self):
		# articles ner 221269
		self.cursor.execute("SELECT id, title_ner, content_ner FROM articles_ner Where id >= 1 and id <= 5")
		self.articles = cursor.fetchall()
		# movies ner 3722
		self.cursor.execute("SELECT id, storyline_ner FROM movies_ner Where id >= 1 and id <= 5")
		self.movies = cursor.fetchall()
	# 訓練向量模型(Using Word2vec)
	def vector_training(self):
		# w2v setting
		t = w2v()
		t.train_file_setting("segmentation.txt", "e2v_w2v_sg")
		# articles
		for article in self.articles:
			article_id = article[0]
			print("article_id:", end = '')
			print(article_id)
			t.write_file(article[1], append = True)
			t.write_file(article[2], append = True)
		# movies
		for movie in self.movies:
			movie_id = movie[0]
			print("movie_id:", end = '')
			print(movie_id)
			t.write_file(movie[1], append = True)
		t.train()
		t.load_model()
		print(t.term_ranking_in_corpus("教師節", 50))
		print(t.term_to_vector("爸爸"))
		print(t.terms_similarity("母親", "母親節"))
		print(1 - t.vectors_similarity(t.term_to_vector("在一起"), t.term_to_vector("過甜蜜")))
	# Save Vector(此部分是用插入資料模式)
	def save_vector(self):
		# w2v setting
		t = w2v()
		t.train_file_setting("segmentation.txt", "e2v_w2v_sg")
		t.load_model()
		dimension = t.size
		# Access Articles NER 221269
		self.cursor.execute("SELECT id, emotion, event, person_object, time, location FROM articles_ner Where id >= 1 and id <= 5")
		articles_ner = self.cursor.fetchall()
		for article_ner in articles_ner:
			article_id = article_ner[0]
			emotion =  article_ner[1]
			event =  article_ner[2]
			person_object =  article_ner[3]
			time =  article_ner[4]
			location =  article_ner[5]
			print("article_id:", end = '')
			print(article_id)
			relationship_e2v_w2v_sg = []
			scenario_e2v_w2v_sg = []
			emotion_count = 0
			emotion_add = np.zeros(dimension)
			for e in emotion.split(" "):
				if e != "":
					try:
						emotion_add += t.term_to_vector(e)
						emotion_count += 1
					except:
						continue
			if emotion_count == 0:
				emotion_count = 1
			relationship_e2v_w2v_sg = np.append(relationship_e2v_w2v_sg, emotion_add/emotion_count)
			scenario_e2v_w2v_sg = np.append(scenario_e2v_w2v_sg, emotion_add/emotion_count)
			event_count = 0
			event_add = np.zeros(dimension)
			for e in event.split(" "):
				if e != "":
					try:
						event_add += t.term_to_vector(e)
						event_count += 1
					except:
						continue
			if event_count == 0:
				event_count = 1
			relationship_e2v_w2v_sg = np.append(relationship_e2v_w2v_sg, event_add/event_count)
			scenario_e2v_w2v_sg = np.append(scenario_e2v_w2v_sg, event_add/event_count)
			person_object_count = 0
			person_object_add = np.zeros(dimension)
			for po in person_object.split(" "):
				if po != "":
					try:
						person_object_add += t.term_to_vector(po)
						person_object_count += 1
					except:
						continue
			if person_object_count == 0:
				person_object_count = 1
			relationship_e2v_w2v_sg = np.append(relationship_e2v_w2v_sg, person_object_add/person_object_count)
			time_count = 0
			time_add = np.zeros(dimension)
			for ti in time.split(" "):
				if ti != "":
					try:
						time_add += t.term_to_vector(ti)
						time_count += 1
					except:
						continue
			if time_count == 0:
				time_count = 1
			relationship_e2v_w2v_sg = np.append(relationship_e2v_w2v_sg, time_add/time_count)
			location_count = 0
			location_add = np.zeros(dimension)
			for l in location.split(" "):
				if l != "":
					try:
						location_add += t.term_to_vector(l)
						location_count += 1
					except:
						continue
			if location_count == 0:
				location_count = 1
			relationship_e2v_w2v_sg = np.append(relationship_e2v_w2v_sg, location_add/location_count)
			sql = "UPDATE articles_vector SET relationship_e2v_w2v_sg=%s, scenario_e2v_w2v_sg=%s WHERE id=%s" 
			val = (str(list(relationship_e2v_w2v_sg)), str(list(scenario_e2v_w2v_sg)), article_id)
			self.cursor.execute(sql, val)
			self.db.commit()
		# Access Movies NER 3722
		self.cursor.execute("SELECT id, emotion, event FROM movies_ner Where id >= 0 and id <= 5")
		movies_ner = self.cursor.fetchall()
		for movie_ner in movies_ner:
			movie_id = movie_ner[0]
			emotion =  movie_ner[1]
			event =  movie_ner[2]
			print("movie_id:", end = '')
			print(movie_id)
			scenario_e2v_w2v_sg = []
			emotion_count = 0
			emotion_add = np.zeros(dimension)
			for e in emotion.split(" "):
				if e != "":
					try:
						emotion_add += t.term_to_vector(e)
						emotion_count += 1
					except:
						continue
			if emotion_count == 0:
				emotion_count = 1
			scenario_e2v_w2v_sg = np.append(scenario_e2v_w2v_sg, emotion_add/emotion_count)
			event_count = 0
			event_add = np.zeros(dimension)
			for e in event.split(" "):
				if e != "":
					try:
						event_add += t.term_to_vector(e)
						event_count += 1
					except:
						continue
			if event_count == 0:
				event_count = 1
			scenario_e2v_w2v_sg = np.append(scenario_e2v_w2v_sg, event_add/event_count)
			sql = "UPDATE movies_vector SET scenario_e2v_w2v_sg=%s WHERE id=%s" 
			val = (str(list(scenario_e2v_w2v_sg)), movie_id)
			self.cursor.execute(sql, val)
			self.db.commit()

if __name__ == "__main__":
	e2v_w2v_sg = E2V_W2V_SG()
	e2v_w2v_sg.e2v_w2v_sg()
