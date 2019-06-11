# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import MySQLdb
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from word2vec import Word2Vec as w2v
from evaluation import Evaluation
import matplotlib.pyplot as plt

def main():
	# (1)Save Ranking Data
	db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
	cursor = db.cursor()
	'''cursor.execute("SELECT emotion, event FROM articles_ner Where id >= 1 and id <= 221269")
	results = cursor.fetchall()
	emotion_dic = {}
	event_dic = {}
	for result in results:
		emotions = result[0]
		events = result[1]
		for emotion in emotions.split(" "):
			# print(emotion)
			if emotion is not "":
				if emotion not in emotion_dic.keys():
					emotion_dic[emotion] = 1
				else :
					emotion_dic[emotion] = emotion_dic[emotion] + 1
		for event in events.split(" "):
			# print(event)
			if event is not "":
				if event not in event_dic.keys():
					event_dic[event] = 1
				else :
					event_dic[event] = event_dic[event] + 1
	cursor.execute("SELECT emotion, event FROM movies_ner Where id >= 1 and id <= 3722")
	results = cursor.fetchall()
	for result in results:
		emotions = result[0]
		events = result[1]
		for emotion in emotions.split(" "):
			# print(emotion)
			if emotion is not "":
				if emotion not in emotion_dic.keys():
					emotion_dic[emotion] = 1
				else :
					emotion_dic[emotion] = emotion_dic[emotion] + 1
		for event in events.split(" "):
			# print(event)
			if event is not "":
				if event not in event_dic.keys():
					event_dic[event] = 1
				else :
					event_dic[event] = event_dic[event] + 1
	# print(sorted(emotion_dic.items(), key = lambda x:x[1], reverse = True), end = "\n\n")
	# print(sorted(event_dic.items(), key = lambda x:x[1], reverse = True))
	t = w2v()
	t.train_file_setting("segmentation.txt", "result")
	# word2vec dimension(150 or 300)
	t.load_model()
	sql = "INSERT INTO experiment_entity2vec (id, emotion_entity, emotion_similarity) VALUES (%s, %s, %s)"
	# 0~50(150 dimension) or 50~100(300 dimension)
	start = 50
	end = 100
	count = start
	print(len(emotion_dic))
	for emotion in sorted(emotion_dic.items(), key = lambda x:x[1], reverse = True):
		print(emotion)
		emotion_entity = emotion[0]
		emotion_similarity = ""
		for similarity in t.term_ranking_in_corpus(emotion_entity, 10):
			emotion_similarity += similarity[0] + " "
		count += 1
		val = (count, emotion_entity, emotion_similarity)
		try:
			cursor.execute(sql, val)
		except:
			print("Emotion Term Insert Error")
		if count == end:
			print("emotion finish...", end = "\n\n")
			count = start
			break
	sql = "UPDATE experiment_entity2vec SET event_entity=%s, event_similarity=%s WHERE id=%s and event_entity = ''"
	print(len(event_dic))
	for event in sorted(event_dic.items(), key = lambda x:x[1], reverse = True):
		print(event)
		event_entity = event[0]
		event_similarity = ""
		for similarity in t.term_ranking_in_corpus(event_entity, 10):
			event_similarity += similarity[0] + " "
		count += 1
		val = (event_entity, event_similarity, count)
		cursor.execute(sql, val)
		if count == end:
			print("event finish...", end = "\n\n")
			break
	db.commit()
	emo_wordcloud = WordCloud(font_path = "msyh.ttf")  #做中文時務必加上字形檔
	eve_wordcloud = WordCloud(font_path = "msyh.ttf")  #做中文時務必加上字形檔
	emo_wordcloud.generate_from_frequencies(frequencies = Counter(emotion_dic))
	eve_wordcloud.generate_from_frequencies(frequencies = Counter(event_dic))
	plt.figure(figsize = (6, 6))
	plt.imshow(emo_wordcloud, interpolation = "bilinear")
	plt.axis("off")
	plt.savefig('image/emotions.png')
	plt.close()
	plt.figure(figsize = (6, 6))
	plt.imshow(eve_wordcloud, interpolation = "bilinear")
	plt.axis("off")
	plt.savefig('image/events.png')
	plt.close()
	# plt.show()'''
	# (2)Calculate Score
	sql = "SELECT emotion_similarity, event_similarity From experiment_entity2vec WHERE id>= 1 and id <= 50"
	cursor.execute(sql)
	results = cursor.fetchall()
	scores_150 = []
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
		scores_150.append(score)
		score = []
		for e in events.split(" "):
			# print(e)
			if e != "":
				score.append(int(e.split(":")[1]))
		scores_150.append(score)
	sql = "SELECT emotion_similarity, event_similarity From experiment_entity2vec WHERE id>= 51 and id <= 100"
	cursor.execute(sql)
	results = cursor.fetchall()
	scores_300 = []
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
		scores_300.append(score)
		score = []
		for e in events.split(" "):
			# print(e)
			if e != "":
				score.append(int(e.split(":")[1]))
		scores_300.append(score)
	e = Evaluation()
	precision_150 = e.average_precision(scores_150, 2)
	ndcg_150 = e.average_ndcg(scores_150)
	precision_300 = e.average_precision(scores_300, 2)
	ndcg_300 = e.average_ndcg(scores_300)
	print(precision_150)
	print(ndcg_150)
	print(precision_300)
	print(ndcg_300)
	plt.title("Semantic Prediction in Frequent Emotions and Events")
	plt.xlabel("The number of predict semantic for each emotions or events")
	plt.ylabel("Average Precision")       
	plt.plot(range(1, 11), precision_150, "-o", color = 'r', label = "150 dimension")# 畫出平均數值 
	plt.plot(range(1, 11), precision_300, "-o", color = 'b', label = "300 dimension")# 畫出平均數值   
	plt.legend(loc = "best")
	# save image
	plt.savefig('image/precision.png')
	plt.close()
	plt.title("Semantic Prediction in Frequent Emotions and Events")
	plt.xlabel("The number of predict semantic for each emotions or events")
	plt.ylabel("Average NDCG")       
	plt.plot(range(1, 11), ndcg_150, "-o", color = 'r', label = "150 dimension")# 畫出平均數值
	plt.plot(range(1, 11), ndcg_300, "-o", color = 'b', label = "300 dimension")# 畫出平均數值  
	plt.legend(loc = "best")
	# save image
	plt.savefig('image/ndcg.png')
	plt.close()

if __name__ == "__main__":
    main()