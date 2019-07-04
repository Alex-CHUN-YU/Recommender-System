# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
import MySQLdb
import numpy as np
from scipy.spatial import distance
# System Experiments
class SystemExperiment:
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		# system type 1
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic = {}
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic = {}
		# system type 2
		self.movies_rstr_vector_relationship_dic = {}
		self.articles_rstr_vector_relationship_dic = {}

	def system_experiment(self):
		self.load_movies_vector()
		self.load_articles_vector()
		self.experiment()

	def load_movies_vector(self):
		# 3722
		movies_sum_w2v_w2v_sg_vector_kinship_dic = {}
		movies_sum_w2v_w2v_sg_vector_romantic_relationship_dic = {}
		movies_sum_w2v_w2v_sg_vector_friendship_dic = {}
		movies_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic = {}
		movies_sum_w2v_w2v_sg_vector_business_relationship_dic = {}
		movies_sum_w2v_w2v_sg_vector_others_dic = {}
		movies_scenario_e2v_w2v_sg_vector_kinship_dic = {}
		movies_scenario_e2v_w2v_sg_vector_romantic_relationship_dic = {}
		movies_scenario_e2v_w2v_sg_vector_friendship_dic = {}
		movies_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic = {}
		movies_scenario_e2v_w2v_sg_vector_business_relationship_dic = {}
		movies_scenario_e2v_w2v_sg_vector_others_dic = {}
		sql = "SELECT b.id, b.sum_w2v_w2v_sg, b.scenario_e2v_w2v_sg, a.relationship_type FROM movies as a, movies_vector as b Where a.id=b.id and a.id >= 1 and a.id <= 3722 and a.relationship_type !='' and a.scenario_type != '' and b.scenario_e2v_w2v_sg != ''"
		self.cursor.execute(sql)
		movies_id_vector = self.cursor.fetchall()
		for movie_id_vector in movies_id_vector:
			movie_sum_w2v_w2v_sg_vector = []
			movie_scenario_e2v_w2v_sg_vector = []
			try:
				movie_id = movie_id_vector[0]
				sum_w2v_w2v_sg_vector = movie_id_vector[1]
				scenario_e2v_w2v_sg_vector = movie_id_vector[2]
				movie_relationship_type = movie_id_vector[3]
			except:
				print("vector no exist!")
				continue
			for s in sum_w2v_w2v_sg_vector[1:-1].split(', '):
				try:
					if s != "":
						movie_sum_w2v_w2v_sg_vector.append(float(s))
				except:
					pass		
			for s in scenario_e2v_w2v_sg_vector[1:-1].split(', '):
				try:
					if s != "":
						movie_scenario_e2v_w2v_sg_vector.append(float(s))
				except:
					pass			
			if movie_sum_w2v_w2v_sg_vector == [] or movie_scenario_e2v_w2v_sg_vector == []:
				continue
			if (np.max(movie_sum_w2v_w2v_sg_vector) == 0.0 and np.min(movie_sum_w2v_w2v_sg_vector) == 0.0) or (np.max(movie_scenario_e2v_w2v_sg_vector) == 0.0 and np.min(movie_scenario_e2v_w2v_sg_vector)):
				continue
			movie_sum_w2v_w2v_sg_vector = np.array(movie_sum_w2v_w2v_sg_vector).astype(np.float32)
			movie_scenario_e2v_w2v_sg_vector = np.array(movie_scenario_e2v_w2v_sg_vector).astype(np.float32)
			if '1' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_kinship_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_kinship_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
			if '2' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_romantic_relationship_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_romantic_relationship_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
			if '3' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_friendship_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_friendship_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
			if '4' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
			if '5' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_business_relationship_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_business_relationship_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
			if '6' in movie_relationship_type:
				movies_sum_w2v_w2v_sg_vector_others_dic[movie_id] = movie_sum_w2v_w2v_sg_vector
				movies_scenario_e2v_w2v_sg_vector_others_dic[movie_id] = movie_scenario_e2v_w2v_sg_vector
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[1] = movies_sum_w2v_w2v_sg_vector_kinship_dic
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[2] = movies_sum_w2v_w2v_sg_vector_romantic_relationship_dic
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[3] = movies_sum_w2v_w2v_sg_vector_friendship_dic
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[4] = movies_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[5] = movies_sum_w2v_w2v_sg_vector_business_relationship_dic
		self.movies_sum_w2v_w2v_sg_vector_relationship_dic[6] = movies_sum_w2v_w2v_sg_vector_others_dic
		self.movies_rstr_vector_relationship_dic[1] = movies_scenario_e2v_w2v_sg_vector_kinship_dic
		self.movies_rstr_vector_relationship_dic[2] = movies_scenario_e2v_w2v_sg_vector_romantic_relationship_dic
		self.movies_rstr_vector_relationship_dic[3] = movies_scenario_e2v_w2v_sg_vector_friendship_dic
		self.movies_rstr_vector_relationship_dic[4] = movies_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic
		self.movies_rstr_vector_relationship_dic[5] = movies_scenario_e2v_w2v_sg_vector_business_relationship_dic
		self.movies_rstr_vector_relationship_dic[6] = movies_scenario_e2v_w2v_sg_vector_others_dic
	def load_articles_vector(self):
		articles_sum_w2v_w2v_sg_vector_kinship_dic = {}
		articles_sum_w2v_w2v_sg_vector_romantic_relationship_dic = {}
		articles_sum_w2v_w2v_sg_vector_friendship_dic = {}
		articles_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic = {}
		articles_sum_w2v_w2v_sg_vector_business_relationship_dic = {}
		articles_sum_w2v_w2v_sg_vector_others_dic = {}
		articles_scenario_e2v_w2v_sg_vector_kinship_dic = {}
		articles_scenario_e2v_w2v_sg_vector_romantic_relationship_dic = {}
		articles_scenario_e2v_w2v_sg_vector_friendship_dic = {}
		articles_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic = {}
		articles_scenario_e2v_w2v_sg_vector_business_relationship_dic = {}
		articles_scenario_e2v_w2v_sg_vector_others_dic = {}
		for i in range(1, 7):
			sql = "SELECT b.id, b.sum_w2v_w2v_sg, b.scenario_e2v_w2v_sg FROM articles as a, articles_vector as b Where a.id=b.id and a.id >= 1 and b.scenario_e2v_w2v_sg != '' and a.relationship_type=" + str(i) + " LIMIT 5"
			# print(sql)
			self.cursor.execute(sql)
			articles_id_vector = self.cursor.fetchall()
			for article_id_vector in articles_id_vector:
				article_sum_w2v_w2v_sg_vector = []
				article_scenario_e2v_w2v_sg_vector = []
				try:
					article_id = article_id_vector[0]
					sum_w2v_w2v_sg_vector = article_id_vector[1]
					scenario_e2v_w2v_sg_vector = article_id_vector[2]
				except:
					print("vector no exist!")
					continue
				for s in sum_w2v_w2v_sg_vector[1:-1].split(', '):
					try:
						if s != "":
							article_sum_w2v_w2v_sg_vector.append(float(s))
					except:
						pass
				for s in scenario_e2v_w2v_sg_vector[1:-1].split(', '):
					try:
						if s != "":
							article_scenario_e2v_w2v_sg_vector.append(float(s))
					except:
						pass				
				if article_sum_w2v_w2v_sg_vector == [] or article_scenario_e2v_w2v_sg_vector == []:
					continue
				if (np.max(article_sum_w2v_w2v_sg_vector) == 0.0 and np.min(article_sum_w2v_w2v_sg_vector) == 0.0) or (np.max(article_scenario_e2v_w2v_sg_vector) == 0.0 and np.min(article_scenario_e2v_w2v_sg_vector)):
					continue
				article_sum_w2v_w2v_sg_vector = np.array(article_sum_w2v_w2v_sg_vector).astype(np.float32)
				article_scenario_e2v_w2v_sg_vector = np.array(article_scenario_e2v_w2v_sg_vector).astype(np.float32)
				if i == 1:
					articles_sum_w2v_w2v_sg_vector_kinship_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_kinship_dic[article_id] = article_scenario_e2v_w2v_sg_vector
				if i == 2:
					articles_sum_w2v_w2v_sg_vector_romantic_relationship_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_romantic_relationship_dic[article_id] = article_scenario_e2v_w2v_sg_vector
				if i == 3:
					articles_sum_w2v_w2v_sg_vector_friendship_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_friendship_dic[article_id] = article_scenario_e2v_w2v_sg_vector
				if i == 4:
					articles_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic[article_id] = article_scenario_e2v_w2v_sg_vector
				if i == 5:
					articles_sum_w2v_w2v_sg_vector_business_relationship_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_business_relationship_dic[article_id] = article_scenario_e2v_w2v_sg_vector
				if i == 6:
					articles_sum_w2v_w2v_sg_vector_others_dic[article_id] = article_sum_w2v_w2v_sg_vector
					articles_scenario_e2v_w2v_sg_vector_others_dic[article_id] = article_scenario_e2v_w2v_sg_vector
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[1] = articles_sum_w2v_w2v_sg_vector_kinship_dic
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[2] = articles_sum_w2v_w2v_sg_vector_romantic_relationship_dic
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[3] = articles_sum_w2v_w2v_sg_vector_friendship_dic
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[4] = articles_sum_w2v_w2v_sg_vector_teacher_student_relationship_dic
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[5] = articles_sum_w2v_w2v_sg_vector_business_relationship_dic
		self.articles_sum_w2v_w2v_sg_vector_relationship_dic[6] = articles_sum_w2v_w2v_sg_vector_others_dic
		self.articles_rstr_vector_relationship_dic[1] = articles_scenario_e2v_w2v_sg_vector_kinship_dic
		self.articles_rstr_vector_relationship_dic[2] = articles_scenario_e2v_w2v_sg_vector_romantic_relationship_dic
		self.articles_rstr_vector_relationship_dic[3] = articles_scenario_e2v_w2v_sg_vector_friendship_dic
		self.articles_rstr_vector_relationship_dic[4] = articles_scenario_e2v_w2v_sg_vector_teacher_student_relationship_dic
		self.articles_rstr_vector_relationship_dic[5] = articles_scenario_e2v_w2v_sg_vector_business_relationship_dic
		self.articles_rstr_vector_relationship_dic[6] = articles_scenario_e2v_w2v_sg_vector_others_dic
	def experiment(self):
		# print("movies:")
		# for movies_relatinship_type, movies_id_vector in self.movies_sum_w2v_w2v_sg_vector_relationship_dic.items():
		# 	if movies_relatinship_type == 1:
		# 		for key, value in movies_id_vector.items():
		# 			print(str(key) + ":" + str(value[:3]))
		# print("articles:")
		# for articles_relatinship_type, articles_id_vector in self.articles_sum_w2v_w2v_sg_vector_relationship_dic.items():
		# 	if articles_relatinship_type == 6:
		# 		for key, value in articles_id_vector.items():
		# 			print(str(key) + ":" + str(value[:3]))
		# print("movies:")
		# for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
		# 	if movies_relatinship_type == 1:
		# 		for key, value in movies_id_vector.items():
		# 			print(str(key) + ":" + str(value[:3]))
		# print("articles:")
		# for articles_relatinship_type, articles_id_vector in self.articles_rstr_vector_relationship_dic.items():
		# 	if articles_relatinship_type == 6:
		# 		for key, value in articles_id_vector.items():
		# 			print(str(key) + ":" + str(value[:3]))
		articles_movies_similarity = {}
		candidates = {}
		for articles_relatinship_type, articles_id_vector in self.articles_rstr_vector_relationship_dic.items():
			if articles_relatinship_type == 1:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 1:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
			if articles_relatinship_type == 2:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 2:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
			if articles_relatinship_type == 3:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 3:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
			if articles_relatinship_type == 4:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 4:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
			if articles_relatinship_type == 5:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 5:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
			if articles_relatinship_type == 6:
				for article_key, article_value in articles_id_vector.items():
					# print("article id:")
					# print(str(article_key) + ":" + str(article_value[:3]))
					candidates = {}
					for movies_relatinship_type, movies_id_vector in self.movies_rstr_vector_relationship_dic.items():
						if movies_relatinship_type == 6:
							for movie_key, movie_value in movies_id_vector.items():
								similarity = 1 - distance.cosine(article_value, movie_value)
								# print(str(movie_key) + ":" + str(similarity))
								candidates[movie_key] = similarity
								# print(str(movie_key) + ":" + str(movie_value[:3]))
					candidates = sorted(candidates, key = candidates.get, reverse = True)
					# print("top 3:")
					# print(candidates[:3])
					articles_movies_similarity[article_key] = candidates[:5]
		sql = "INSERT INTO experiment_system (id, system_type, article_id, movie_id1, movie_id2, movie_id3, movie_id4, movie_id5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		system_type = 2
		id = 1
		for article_id, movies_id_similarity in articles_movies_similarity.items():
			print(str(article_id) + ":" + str(movies_id_similarity))
			val = (id, system_type, article_id, movies_id_similarity[0], movies_id_similarity[1], movies_id_similarity[2], movies_id_similarity[3], movies_id_similarity[4])	
			self.cursor.execute(sql, val)
			self.db.commit()
			id += 2

		articles_movies_similarity = {}
		candidates = {}
		for articles_relatinship_type, articles_id_vector in self.articles_sum_w2v_w2v_sg_vector_relationship_dic.items():
			for article_key, article_value in articles_id_vector.items():
				# print("article id:")
				# print(str(article_key) + ":" + str(article_value[:3]))
				candidates = {}
				for movies_relatinship_type, movies_id_vector in self.movies_sum_w2v_w2v_sg_vector_relationship_dic.items():
					for movie_key, movie_value in movies_id_vector.items():
						similarity = 1 - distance.cosine(article_value, movie_value)
						# print(str(movie_key) + ":" + str(similarity))
						candidates[movie_key] = similarity
						# print(str(movie_key) + ":" + str(movie_value[:3]))
				candidates = sorted(candidates, key = candidates.get, reverse = True)
				# print("top 3:")
				# print(candidates[:3])
				articles_movies_similarity[article_key] = candidates[:5]
		system_type = 1
		id = 2
		for article_id, movies_id_similarity in articles_movies_similarity.items():
			print(str(article_id) + ":" + str(movies_id_similarity))
			val = (id, system_type, article_id, movies_id_similarity[0], movies_id_similarity[1], movies_id_similarity[2], movies_id_similarity[3], movies_id_similarity[4])	
			self.cursor.execute(sql, val)
			self.db.commit()
			id += 2
		

if __name__ == "__main__":
	system_experiment = SystemExperiment()
	system_experiment.system_experiment()

