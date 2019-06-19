# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from word2vec import Word2Vec as w2v
import MySQLdb
import numpy as np
from bert_embedding import BertEmbedding
import codecs
import re
# Entity to Vector
class E2V_BERT:
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.articles_ner_tag = []
		self.movies_ner_tag = []
		# 產生詞典以供後序 experiment 使用
		self.entity_and_vector = []
	# main function
	def e2v_bert(self):
		# 透過 bert embedding 產生向量並將生成的 relationship feature 和 scenario feature 存入		
		self.load_data()
		self.extract_vector_and_save_vector(dimension = 768)
		self.produce_entity_vector_table()
	# load data
	def load_data(self):
		# articles ner 221269
		self.cursor.execute("SELECT a.id, a.content_ner_tag FROM articles_ner as a, articles as b Where a.id = b.id and a.id >= 1 and a.id <= 221269 and b.relationship_type != ''")
		self.articles_ner_tag = self.cursor.fetchall()
		# movies ner 3722
		self.cursor.execute("SELECT a.id, a.storyline_ner_tag FROM movies_ner as a, movies as b Where a.id = b.id and a.id >= 1 and a.id <= 3722 and b.scenario_type != ''")
		self.movies_ner_tag = self.cursor.fetchall()
	# 取得向量(Using bert) 並產生 relationship feature 和 scenario feature 存入
	def extract_vector_and_save_vector(self, dimension):
		bert_embedding = BertEmbedding(model = 'bert_12_768_12', dataset_name='wiki_cn', max_seq_length = 50)
		# self.articles_ner_tag = [[1, "人:none 失戀:em 悲觀:em 房間:lo 感到:none 難過:em @ 戀情:em 感到:none 傷心:em 值得:none 人:none 人:none 失戀:em@後會:none 傷害自己:ev 事業:none 失敗:ev 事情:none 失敗:em 忘:ev 走:ev"]]
		# self.movies_ner_tag = [[1, "戀情:ev 感到:none "], [2, "人:none 失戀:em 悲觀:em 房間:lo 感到:none 難過:em @ 戀情:ev 感到:none "]]		
		for article_ner_tag in self.articles_ner_tag:
			article_id = article_ner_tag[0]
			sentences_ner_tag = article_ner_tag[1]
			print("article_id:", end = '')
			print(article_id)
			relationship_e2v_bert = []
			scenario_e2v_bert = []
			sentences = []
			entity_type_position_length_in_sentences = []
			for sentence_ner_tag in sentences_ner_tag.split('@'):
				if sentences_ner_tag != "":
					sentence = ""
					entity_type_position_length_in_sentence = []
					position = 0
					for term_ner_tag in sentence_ner_tag.split(' '):
						if " " not in term_ner_tag and term_ner_tag != "":
							term = term_ner_tag.split(':')[0]
							tag = term_ner_tag.split(':')[1]
							# 由於連續的英文或數字會在 bert embedding 變成一個字故必須做此處理
							en_re = re.compile(r'[A-Za-z]')
							chi = True
							length = 0
							for t in term:							
								if bool(re.match(en_re, t)) or t.isdigit():
									chi = False
								else:
									if chi != True:
										length += 2
										chi = True
									else:
										length += 1
							if chi != True:
								length += 1
							entity_type_position_length_in_sentence.append([term, tag, position, length])
							sentence += term
							position += length
					sentences.append(sentence)
					# print(len(entity_type_position_length_in_sentence))
					entity_type_position_length_in_sentences.append(entity_type_position_length_in_sentence)
			print(sentences)
			print(entity_type_position_length_in_sentences)
			results = bert_embedding(sentences)
			print("文章長度:", end = "")
			print(len(results))
			po_vector = np.zeros(dimension)
			em_vector = np.zeros(dimension)
			ev_vector = np.zeros(dimension)
			lo_vector = np.zeros(dimension)
			ti_vector = np.zeros(dimension)
			po_count = 0
			em_count = 0
			ev_count = 0
			lo_count = 0
			ti_count = 0
			for i, result in enumerate(results):
				print(sentences[i])
				print(entity_type_position_length_in_sentences[i])
				print(result[0])
				for i, entity in enumerate(entity_type_position_length_in_sentences[i]): 
					entity_vector = np.zeros(dimension)
					try:
						for i in range(entity[3]):
							entity_vector += result[1][entity[2] + 1 + i]
					except:
						print("some illegal characters")
						break
					if entity[1] == 'none':
						pass
					elif entity[1] == 'po':
						po_vector += entity_vector
						po_count += 1
					elif entity[1] == 'em':
						em_vector += entity_vector
						em_count += 1
					elif entity[1] == 'ev':
						ev_vector += entity_vector
						ev_count += 1
					elif entity[1] == 'lo':
						lo_vector += entity_vector
						lo_count += 1
					elif entity[1] == 'ti':
						ti_vector += entity_vector
						ti_count += 1
					self.entity_and_vector.append([entity[0], entity_vector])
				print(po_vector[:5])
				print(em_vector[:5])
				print(ev_vector[:5])
				print(lo_vector[:5])
				print(ti_vector[:5])
			# print(po_count)
			# print(em_count)
			# print(ev_count)
			# print(lo_count)
			# print(ti_count)
			if po_count == 0:
				po_count = 1
			if em_count == 0:
				em_count = 1
			if ev_count == 0:
				ev_count = 1
			if lo_count == 0:
				lo_count = 1
			if ti_count == 0:
				ti_count = 1
			relationship_e2v_bert = np.append(relationship_e2v_bert, po_vector/po_count)
			relationship_e2v_bert = np.append(relationship_e2v_bert, em_vector/em_count)
			relationship_e2v_bert = np.append(relationship_e2v_bert, ev_vector/ev_count)
			relationship_e2v_bert = np.append(relationship_e2v_bert, lo_vector/lo_count)
			relationship_e2v_bert = np.append(relationship_e2v_bert, ti_vector/ti_count)
			scenario_e2v_bert = np.append(scenario_e2v_bert, em_vector/em_count)
			scenario_e2v_bert = np.append(scenario_e2v_bert, ev_vector/ev_count)
			print(relationship_e2v_bert.shape)
			print(scenario_e2v_bert.shape)
			# print(relationship_e2v_bert[1536])
			# print(relationship_e2v_bert[2304])
			sql = "UPDATE articles_vector SET relationship_e2v_bert=%s, scenario_e2v_bert=%s WHERE id=%s" 
			val = (str(list(relationship_e2v_bert)), str(list(scenario_e2v_bert)), article_id)
			self.cursor.execute(sql, val)
			self.db.commit()
			print("="*10)
		for movie_ner_tag in self.movies_ner_tag:
			movie_id = movie_ner_tag[0]
			sentences_ner_tag = movie_ner_tag[1]
			print("movie_id:", end = '')
			print(movie_id)
			scenario_e2v_bert = []
			sentences = []
			entity_type_position_length_in_sentences = []
			for sentence_ner_tag in sentences_ner_tag.split('@'):
				if sentence_ner_tag != "":
					sentence = ""
					entity_type_position_length_in_sentence = []
					position = 0
					for term_ner_tag in sentence_ner_tag.split(' '):
						if " " not in term_ner_tag and term_ner_tag != "":
							term = term_ner_tag.split(':')[0]
							tag = term_ner_tag.split(':')[1]
							# 由於連續的英文或數字會在 bert embedding 變成一個字故必須做此處理
							en_re = re.compile(r'[A-Za-z]')
							chi = True
							length = 0
							for t in term:							
								if bool(re.match(en_re, t)) or t.isdigit():
									chi = False
								else:
									if chi != True:
										length += 2
										chi = True
									else:
										length += 1
							if chi != True:
								length += 1
							entity_type_position_length_in_sentence.append([term, tag, position, length])
							sentence += term
							position += length
					sentences.append(sentence)
					# print(len(entity_type_position_length_in_sentence))
					entity_type_position_length_in_sentences.append(entity_type_position_length_in_sentence)
			print(sentences)
			print(entity_type_position_length_in_sentences)
			results = bert_embedding(sentences)
			print("故事情節長度:", end = "")
			print(len(results))
			em_vector = np.zeros(dimension)
			ev_vector = np.zeros(dimension)
			em_count = 0
			ev_count = 0
			for i, result in enumerate(results):
				print(sentences[i])
				print(entity_type_position_length_in_sentences[i])
				print(result[0])
				for i, entity in enumerate(entity_type_position_length_in_sentences[i]): 
					entity_vector = np.zeros(dimension)
					try:
						for i in range(entity[3]):
							entity_vector += result[1][entity[2] + 1 + i]
					except:
						print("some illegal characters")
						break
					if entity[1] == 'none':
						pass
					elif entity[1] == 'po':
						pass
					elif entity[1] == 'em':
						em_vector += entity_vector
						em_count += 1
					elif entity[1] == 'ev':
						ev_vector += entity_vector
						ev_count += 1
					elif entity[1] == 'lo':
						pass
					elif entity[1] == 'ti':
						pass
					self.entity_and_vector.append([entity[0], entity_vector])
				print(em_vector[:5])
				print(ev_vector[:5])
			# print(em_count)
			# print(ev_count)
			if em_count == 0:
				em_count = 1
			if ev_count == 0:
				ev_count = 1
			scenario_e2v_bert = np.append(scenario_e2v_bert, em_vector/em_count)
			scenario_e2v_bert = np.append(scenario_e2v_bert, ev_vector/ev_count)
			print(scenario_e2v_bert.shape)
			sql = "UPDATE movies_vector SET scenario_e2v_bert=%s WHERE id=%s" 
			val = (str(list(scenario_e2v_bert)), movie_id)
			self.cursor.execute(sql, val)
			self.db.commit()
			print("="*10)
	# 產生 entity 對應的 vector 表(entity 不可重複)
	def produce_entity_vector_table(self):
		entity_dict = {}
		entity_count = {}
		mode = "w"
		file = "e2v_bert_table.txt"
		with codecs.open(file, mode = mode, encoding = 'utf8') as vector_table:
			for entity_vector in self.entity_and_vector:
				if entity_vector[0] not in entity_dict.keys():
					entity_dict[entity_vector[0]] = entity_vector[1]
					entity_count[entity_vector[0]] = 1
				else:
					entity_dict[entity_vector[0]] = entity_dict[entity_vector[0]] + entity_vector[1]
					entity_count[entity_vector[0]] = entity_count[entity_vector[0]] + 1
			for entity, count in entity_count.items():
				entity_dict[entity] = entity_dict[entity]/count 
			for entity, vector in entity_dict.items():
				vector_table.write(entity + ":")
				vector_table.write(str(list(vector)))
				vector_table.write("\n")
			vector_table.close()

if __name__ == "__main__":
	e2v_bert = E2V_BERT()
	e2v_bert.e2v_bert()
