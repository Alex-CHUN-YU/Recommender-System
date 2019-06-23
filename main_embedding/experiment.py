# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import MySQLdb
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from word2vec import Word2Vec as w2v
from evaluation import Evaluation
import matplotlib.pyplot as plt
from os import path, getcwd
from PIL import Image
import numpy as np
import codecs
from scipy.spatial import distance
# 主要針對頻繁的 50 名 emotion 和 event entity, 並將每個 entity 找出前 10 名做評分, 並用 precision 和 ndcg 來衡量
class Main_Embedding_Experiment:
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.emotion_dic = {}
		self.event_dic = {}
	# frequent entity and entity most similarity top 10
	def frequent_entity_ranking(self):
		# 計算 extrovert event 和 hidden event 品質
		# self.calculate_event_quality()
		# 計算數量並產生文字雲並將排序進行插入
		self.frequent_entity_cloud()
		# self.insert_ranking(embedding_model = 'e2v_w2v_sg', frequent = 50, rank = 10)
		self.insert_ranking(embedding_model = 'e2v_bert', frequent = 50, rank = 10)
		# 將分數提取出來並計算 ndcg 和 precision 以及畫出圖
		# w2v_150_scores = self.extract_score(start = 1, end = 50)
		# w2v_300_scores = self.extract_score(start = 51, end = 100)
		# bert_768_scores = self.extract_score(start = 101, end = 150)
		# self.calculate_score_and_show_result(w2v_150_scores, w2v_300_scores, bert_768_scores)
	# calculate extroverted event and hidden event accuracy
	def calculate_event_quality(self):
		with codecs.open("event.txt", "r", encoding = "utf-8") as events_label:
			extroverted_event_score = 0
			extroverted_event_sum = 0
			hidden_event_score = 0
			hidden_event_sum = 0
			for event_label in events_label:
				event_label = event_label.split(":")
				if event_label[1] == '1':
					extroverted_event_sum += 1
					extroverted_event_score += int(event_label[2])
				elif event_label[1] == '2':
					hidden_event_sum += 1
					hidden_event_score += int(event_label[2])
			print("extroverted_event_score:", end = "")
			print(extroverted_event_score/extroverted_event_sum)
			print("hidden_event_score:", end = "")
			print(hidden_event_score/hidden_event_sum)
	# create emotion and event entity dictionary and frequent term cloud
	def frequent_entity_cloud(self):
		# Article 221269
		self.cursor.execute("SELECT emotion, event FROM articles_ner Where id >= 1 and id <= 221269")
		articles = self.cursor.fetchall()
		for article in articles:
			emotions = article[0]
			events = article[1]
			for emotion in emotions.split(" "):
				# print(emotion)
				if emotion is not "":
					if emotion not in self.emotion_dic.keys():
						self.emotion_dic[emotion] = 1
					else:
						self.emotion_dic[emotion] = self.emotion_dic[emotion] + 1
			for event in events.split(" "):
				# print(event)
				if event is not "":
					if event not in self.event_dic.keys():
						self.event_dic[event] = 1
					else:
						self.event_dic[event] = self.event_dic[event] + 1
		# Movie 3722
		self.cursor.execute("SELECT emotion, event FROM movies_ner Where id >= 1 and id <= 3722")
		movies = self.cursor.fetchall()
		for movie in movies:
			emotions = movie[0]
			events = movie[1]
			for emotion in emotions.split(" "):
				# print(emotion)
				if emotion is not "":
					if emotion not in self.emotion_dic.keys():
						self.emotion_dic[emotion] = 1
					else:
						self.emotion_dic[emotion] = self.emotion_dic[emotion] + 1
			for event in events.split(" "):
				# print(event)
				if event is not "":
					if event not in self.event_dic.keys():
						self.event_dic[event] = 1
					else:
						self.event_dic[event] = self.event_dic[event] + 1
		print(sorted(self.emotion_dic.items(), key = lambda x:x[1], reverse = True), end = "\n\n")
		print(sorted(self.event_dic.items(), key = lambda x:x[1], reverse = True))
		# 移除模糊的詞彙
		self.emotion_dic.pop('知道', None)
		self.event_dic.pop('不知道', None) 
		self.event_dic.pop('有人', None) 
		self.event_dic.pop('不好', None)
		mask = np.array(Image.open(path.join(getcwd(), "mask.png")))
		self.generate_wordcloud("emotion_cloud", self.emotion_dic, mask)
		mask = np.array(Image.open(path.join(getcwd(), "mask.png")))
		self.generate_wordcloud("event_cloud", self.event_dic, mask)
	# generate word cloud
	def generate_wordcloud(self, name, entity_dic, mask):
		word_cloud = WordCloud(font_path = "msyh.ttf", background_color = 'black', mask = mask).generate_from_frequencies(frequencies = Counter(entity_dic))
		plt.figure(figsize=(6,4),facecolor = 'white', edgecolor='blue')
		plt.imshow(word_cloud, interpolation = "bilinear")
		plt.axis("off")
		plt.tight_layout(pad=0)
		plt.savefig('image/' + name + '.png')
		plt.close()
	# 將每個頻繁的 entity 透過不同 model 產生一個數量級的排序 
	def insert_ranking(self, embedding_model, frequent, rank):
		if embedding_model == 'e2v_w2v_sg':	
			self.w2v_algorithm(150, 0, frequent, rank)
			self.w2v_algorithm(300, frequent, frequent*2, rank)
		elif embedding_model == 'e2v_bert':
			self.bert_algorithm(768, frequent*2, frequent*3, rank)
	# focus on word2vec algorithm
	def w2v_algorithm(self, dimension, start, end, rank):
		t = w2v()
		t.hyperparameter(dimension = dimension)
		t.train_file_setting("segmentation.txt", "e2v_w2v_sg")
		t.load_model()
		count = start
		print(len(self.emotion_dic))
		sql = "INSERT INTO experiment_entity2vec (id, emotion_entity, emotion_similarity) VALUES (%s, %s, %s)"
		for emotion in sorted(self.emotion_dic.items(), key = lambda x:x[1], reverse = True):
			print(emotion)
			emotion_entity = emotion[0]
			emotion_similarity = ""
			for similarity in t.term_ranking_in_corpus(emotion_entity, rank):
				emotion_similarity += similarity[0] + ":" + " "
			count += 1
			val = (count, emotion_entity, emotion_similarity)
			try:
				self.cursor.execute(sql, val)
			except:
				print("Emotion Term Insert Error")
			if count == end:
				print("emotion finish...", end = "\n\n")
				count = start
				break
		print(len(self.event_dic))
		sql = "UPDATE experiment_entity2vec SET event_entity=%s, event_similarity=%s WHERE id=%s and event_entity = ''"
		for event in sorted(self.event_dic.items(), key = lambda x:x[1], reverse = True):
			print(event)
			event_entity = event[0]
			event_similarity = ""
			for similarity in t.term_ranking_in_corpus(event_entity, rank):
				event_similarity += similarity[0] + ":" + " "
			count += 1
			val = (event_entity, event_similarity, count)
			self.cursor.execute(sql, val)
			if count == end:
				print("event finish...", end = "\n\n")
				break
		self.db.commit()
	# focus on bert algorithm
	def bert_algorithm(self, dimension, start, end, rank):
		entity_vector_table = {}
		with codecs.open('e2v_bert_table.txt', encoding = 'utf-8') as table:
			for entity_vector_line in table:
				entity_vector = []
				for s in entity_vector_line.split(':')[1][1:-1].split(', '):
					try:
						if s != "":
							entity_vector.append(float(s))
					except:
						pass
				entity_vector = np.array(entity_vector).astype(np.float32)
				entity_vector_table[entity_vector_line.split(':')[0]] = entity_vector
		# for entity, vector in entity_vector_table.items():
			# print(entity + ":" + str(vector.shape) + ":", end = "")
			# print(vector[:5])	 
		count = start
		print(len(self.emotion_dic))
		sql = "INSERT INTO experiment_entity2vec (id, emotion_entity, emotion_similarity) VALUES (%s, %s, %s)"
		for emotion in sorted(self.emotion_dic.items(), key = lambda x:x[1], reverse = True):
			print(emotion)
			emotion_entity = emotion[0]
			emotion_similarity = ""
			for similarity in self.term_ranking_in_corpus_about_bert(entity_vector_table, emotion_entity, rank):
				emotion_similarity += similarity[0] + ":" + " "
			# print(emotion_similarity)
			count += 1
			val = (count, emotion_entity, emotion_similarity)
			try:
				self.cursor.execute(sql, val)
			except:
				print("Emotion Term Insert Error")
			if count == end:
				print("emotion finish...", end = "\n\n")
				count = start
				break
				print(len(self.event_dic))
		sql = "UPDATE experiment_entity2vec SET event_entity=%s, event_similarity=%s WHERE id=%s and event_entity = ''"
		for event in sorted(self.event_dic.items(), key = lambda x:x[1], reverse = True):
			print(event)
			event_entity = event[0]
			event_similarity = ""
			for similarity in self.term_ranking_in_corpus_about_bert(entity_vector_table, event_entity, rank):
				event_similarity += similarity[0] + ":" + " "
			count += 1
			val = (event_entity, event_similarity, count)
			self.cursor.execute(sql, val)
			if count == end:
				print("event finish...", end = "\n\n")
				break
		self.db.commit()
	# Ranking about bert
	def term_ranking_in_corpus_about_bert(self, entity_vector_table, specific_entiy, rank):
		entity_vector_rank_table = {}
		for entity, vector in entity_vector_table.items():
			entity_vector_rank_table[entity] = 1 - distance.cosine(entity_vector_table[specific_entiy], vector)
		entity_vector_rank_table = sorted(entity_vector_rank_table.items(), key=lambda d: d[1], reverse = True)
		for i, entity_similarity in enumerate(entity_vector_rank_table):
			# print(i)
			if i > 0 and i <= rank:
				print(entity_similarity[0] + ":", end = "")
				print(entity_similarity[1])
				yield entity_similarity
	# extract database socre 
	def extract_score(self, start, end):
		sql = "SELECT emotion_similarity, event_similarity From experiment_entity2vec WHERE id>= %s and id <= %s"
		val = (start, end)
		self.cursor.execute(sql, val)
		results = self.cursor.fetchall()
		scores = []
		for result in results:
			emotions = result[0]
			events = result[1]
			print(emotions)
			print(events)
			score = []
			for e in emotions.split(" "):
				# print(e)
				if e != "":
					score.append(int(e.split(":")[1]))
			scores.append(score)
			score = []
			for e in events.split(" "):
				# print(e)
				if e != "":
					score.append(int(e.split(":")[1]))
			scores.append(score)
		return scores
	# calculate score about precision and ndcg. and show result image
	def calculate_score_and_show_result(self, w2v_150_socres, w2v_300_scores, bert_768_scores):
		e = Evaluation()
		w2v_precision_150 = e.average_precision(w2v_150_socres, 2)
		w2v_ndcg_150 = e.average_ndcg(w2v_150_socres)
		w2v_precision_300 = e.average_precision(w2v_300_scores, 2)
		w2v_ndcg_300 = e.average_ndcg(w2v_300_scores)
		bert_precision_768 = e.average_precision(bert_768_scores, 2)
		bert_ndcg_768 = e.average_ndcg(bert_768_scores)
		print(w2v_precision_150)
		print(w2v_ndcg_150)
		print(w2v_precision_300)
		print(w2v_ndcg_300)
		print(bert_precision_768)
		print(bert_ndcg_768)
		plt.title("Semantic Prediction in Frequent Emotions and Events")
		plt.xlabel("The number of predict semantic for each emotions or events")
		plt.ylabel("Average Precision")       
		plt.plot(range(1, 11), w2v_precision_150, "-o", color = 'r', label = "e2v-w2v-sg 150 dimension")# 畫出平均數值 
		plt.plot(range(1, 11), w2v_precision_300, "-o", color = 'b', label = "e2v-w2v-sg 300 dimension")# 畫出平均數值   
		plt.plot(range(1, 11), bert_precision_768, "-o", color = 'g', label = "e2v-bert 768 dimension")# 畫出平均數值  
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/precision.png')
		plt.close()
		plt.title("Semantic Prediction in Frequent Emotions and Events")
		plt.xlabel("The number of predict semantic for each emotions or events")
		plt.ylabel("Average NDCG")       
		plt.plot(range(1, 11), w2v_ndcg_150, "-o", color = 'r', label = "e2v-w2v-sg 150 dimension")# 畫出平均數值
		plt.plot(range(1, 11), w2v_ndcg_300, "-o", color = 'b', label = "e2v-w2v-sg 300 dimension")# 畫出平均數值  
		plt.plot(range(1, 11), bert_ndcg_768, "-o", color = 'g', label = "e2v-bert 768 dimension")# 畫出平均數值 
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/ndcg.png')
		plt.close()

if __name__ == "__main__":
    main_embedding_experiment = Main_Embedding_Experiment()
    main_embedding_experiment.frequent_entity_ranking()