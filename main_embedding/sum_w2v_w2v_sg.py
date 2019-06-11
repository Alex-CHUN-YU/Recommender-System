# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from word2vec import Word2Vec as w2v
import MySQLdb
import numpy as np
import jieba
import re
# Baseline Vector
class Sum_W2V_W2V_SG():
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.stopwordset = set()
		self.articles = []
		self.movies = []
	# main function
	def sum_w2v_w2v_sg(self):
		self.load_data()
		# self.vector_training()
		self.save_vector()
	# load data and stop word filter
	def load_data(self):
		self.set_stopword()
		# 221269
		self.cursor.execute("SELECT id, content FROM articles Where id >= 1 and id <= 221269")
		self.articles = self.cursor.fetchall()
		# 3722
		self.cursor.execute("SELECT id, storyline FROM movies Where id >= 1 and id <= 3722")
		self.movies = self.cursor.fetchall()
	# 讀取 stopword 辭典，並存到 stopwordset
	def set_stopword(self):
		with open("stopwords.txt", "r", encoding = "utf-8") as stopwords:
			for stopword in stopwords:
				self.stopwordset.add(stopword.strip('\n'))
		#print(self.stopwordset)
		print("StopWord Set 已儲存!")
	# 訓練向量模型(Using Word2vec)
	def vector_training(self):
		# w2v setting
		t = w2v()
		t.train_file_setting("segmentation.txt", "sum_w2v_w2v_sg")
		# articles
		for article in self.articles:
			article_id = article[0]
			content = article[1]
			print("article_id:", end = '')
			print(article_id)
			# print(content)
			sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', content)
			sentence_list = sentences.split("\n")
			# print(sentence_list)
			for sentence in sentence_list:
				if sentence != '':
					# print(sentence)
					seg_list = jieba.cut(sentence, cut_all = False)
					for seg in seg_list:
						if seg not in self.stopwordset and seg != ' ':
							print(seg, end = ' ')
							t.write_file(seg + " ", append = True)
				print('')
		# movies
		for movie in self.movies:
			movie_id = movie[0]
			storyline = movie[1]
			print("movie_id:", end = '')
			print(movie_id)
			# print(content)
			sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', storyline)
			sentence_list = sentences.split("\n")
			# print(sentence_list)
			for sentence in sentence_list:
				if sentence != '':
					# print(sentence)
					seg_list = jieba.cut(sentence, cut_all = False)
					for seg in seg_list:
						if seg not in self.stopwordset and seg != ' ':
							print(seg, end = ' ')
							t.write_file(seg + " ", append = True)
				print('')
		t.train()
		t.load_model()
		print(t.term_ranking_in_corpus("教師節", 50))
		print(t.term_to_vector("爸爸"))
		print(t.terms_similarity("母親", "母親節"))
		print(1 - t.vectors_similarity(t.term_to_vector("母親"), t.term_to_vector("母親節")))
	# Save Vector(此部分是用插入資料模式)
	def save_vector(self):
		# w2v setting
		t = w2v()
		t.train_file_setting("segmentation.txt", "sum_w2v_w2v_sg")
		t.load_model()
		dimension = t.size
		# articles
		sql = "INSERT INTO articles_vector (id, sum_w2v_w2v_sg) VALUES (%s, %s)"
		for article in self.articles:
			article_sum_w2v_w2v_sg = np.zeros(dimension)
			article_id = article[0]
			content = article[1]
			print("article_id:", end = '')
			print(article_id)
			# print(content)
			sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', content)
			sentence_list = sentences.split("\n")
			# print(sentence_list)
			for sentence in sentence_list:
				if sentence != '':
					# print(sentence)
					seg_list = jieba.cut(sentence, cut_all = False)
					for seg in seg_list:
						if seg not in self.stopwordset and seg != ' ':
							try:
								seg_vector = t.term_to_vector(seg)
								print(seg)
								print(seg_vector[:5], end = '\n\n')
								article_sum_w2v_w2v_sg += seg_vector
							except:
								continue
				print('')
			val = (article_id, article_sum_w2v_w2v_sg)
			print("sum")
			print(article_sum_w2v_w2v_sg[:5], end = "\n\n")
			self.cursor.execute(sql, val)
			self.db.commit()
		# movies
		sql = "INSERT INTO movies_vector (id, sum_w2v_w2v_sg) VALUES (%s, %s)"
		for movie in self.movies:
			movie_sum_w2v_w2v_sg = np.zeros(dimension)
			movie_id = movie[0]
			storyline = movie[1]
			print("movie_id:", end = '')
			print(movie_id)
			# print(content)
			sentences = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', storyline)
			sentence_list = sentences.split("\n")
			# print(sentence_list)
			for sentence in sentence_list:
				if sentence != '':
					# print(sentence)
					seg_list = jieba.cut(sentence, cut_all = False)
					for seg in seg_list:
						if seg not in self.stopwordset and seg != ' ':
							try:
								seg_vector = t.term_to_vector(seg)
								print(seg)
								print(seg_vector[:5], end = '\n\n')
								movie_sum_w2v_w2v_sg += seg_vector
							except:
								continue
				print('')
			val = (movie_id, movie_sum_w2v_w2v_sg)
			print("sum")
			print(movie_sum_w2v_w2v_sg[:5], end = "\n\n")
			self.cursor.execute(sql, val)
			self.db.commit()

if __name__ == "__main__":
	sum_w2v_w2v_sg = Sum_W2V_W2V_SG()
	sum_w2v_w2v_sg.sum_w2v_w2v_sg()
