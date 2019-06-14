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
		# 計算數量並產生文字雲並將排序進行插入
		self.frequent_entity_cloud()
		self.insert_ranking(embedding_model = 'e2v_w2v_sg', frequent = 50, rank = 10)
		# 將分數提取出來並計算 ndcg 和 precision 以及畫出圖
		# w2v_150_scores = self.extract_score(start = 1, end = 50)
		# w2v_300_scores = self.extract_score(start = 51, end = 100)
		# bert_768_scores = []
		# self.calculate_score_and_show_result(w2v_150_scores, w2v_300_scores, bert_768_scores)
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
			# self.w2v_algorithm(300, frequent, frequent + frequent, rank)
		elif embedding_model == 'e2v_bert':
			pass
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
		print(w2v_precision_150)
		print(w2v_ndcg_150)
		print(w2v_precision_300)
		print(w2v_ndcg_300)
		plt.title("Semantic Prediction in Frequent Emotions and Events")
		plt.xlabel("The number of predict semantic for each emotions or events")
		plt.ylabel("Average Precision")       
		plt.plot(range(1, 11), w2v_precision_150, "-o", color = 'r', label = "e2v-w2v-sg 150 dimension")# 畫出平均數值 
		plt.plot(range(1, 11), w2v_precision_300, "-o", color = 'b', label = "e2v-w2v-sg 300 dimension")# 畫出平均數值   
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/precision.png')
		plt.close()
		plt.title("Semantic Prediction in Frequent Emotions and Events")
		plt.xlabel("The number of predict semantic for each emotions or events")
		plt.ylabel("Average NDCG")       
		plt.plot(range(1, 11), w2v_ndcg_150, "-o", color = 'r', label = "e2v-w2v-sg 150 dimension")# 畫出平均數值
		plt.plot(range(1, 11), w2v_ndcg_300, "-o", color = 'b', label = "e2v-w2v-sg 300 dimension")# 畫出平均數值  
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/ndcg.png')
		plt.close()
if __name__ == "__main__":
    main_embedding_experiment = Main_Embedding_Experiment()
    main_embedding_experiment.frequent_entity_ranking()