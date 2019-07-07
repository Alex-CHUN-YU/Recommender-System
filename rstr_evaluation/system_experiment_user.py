# -*- coding: utf-8 -*-
__author__ = "ALEX-CHUN-YU (P76064538@mail.ncku.edu.tw)"
from evaluation import Evaluation
import MySQLdb
import matplotlib.pyplot as plt
# Evaluate System Preference
class SystemEvaluationUser:
	# init
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
	def system_evaluation_user(self):
		self.whole_evaluation()
		self.individual_evaluation()
	# individual evaluation
	def individual_evaluation(self):
		e = Evaluation()
		sql = "SELECT article_id, score1, score2, score3, score4, score5 From experiment_system_user Where system_type = 2"
		self.cursor.execute(sql)
		e2v_score = []
		e2v_kinship_scores = []
		e2v_romantic_scores = []
		e2v_friendship_scores = []
		e2v_teacher_student_scores = []
		e2v_business_scores = []
		e2v_others_scores = []
		scores_list = self.cursor.fetchall()
		for score_list in scores_list:
			sql = "SELECT relationship_type From articles Where id = " + str(score_list[0]) 
			self.cursor.execute(sql)
			relationship_type = self.cursor.fetchone()
			relationship_type = relationship_type[0]
			print("article_id:" + str(score_list[0]) + " relationship_type:" + str(relationship_type))
			if relationship_type == '1':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_kinship_scores.append(e2v_score)
				e2v_score = []	
			if relationship_type == '2':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_romantic_scores.append(e2v_score)
				e2v_score = []
			if relationship_type == '3':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_friendship_scores.append(e2v_score)
				e2v_score = []
			if relationship_type == '4':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_teacher_student_scores.append(e2v_score)
				e2v_score = []
			if relationship_type == '5':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_business_scores.append(e2v_score)
				e2v_score = []
			if relationship_type == '6':
				e2v_score.append(score_list[1])
				e2v_score.append(score_list[2])
				e2v_score.append(score_list[3])
				e2v_score.append(score_list[4])
				e2v_score.append(score_list[5])
				e2v_others_scores.append(e2v_score)
				e2v_score = []
		print("kinship:" + str(e2v_kinship_scores))
		print("remantic:" + str(e2v_romantic_scores))
		print("friendship:" + str(e2v_friendship_scores))
		print("teacher student:" + str(e2v_teacher_student_scores))
		print("business:" + str(e2v_business_scores))
		print("others:" + str(e2v_others_scores))
		e2v_kinship_ndcg = e.average_ndcg(e2v_kinship_scores)
		e2v_romantic_ndcg = e.average_ndcg(e2v_romantic_scores)
		e2v_friendship_ndcg = e.average_ndcg(e2v_friendship_scores)
		e2v_teacher_student_ndcg = e.average_ndcg(e2v_teacher_student_scores)
		e2v_business_ndcg = e.average_ndcg(e2v_business_scores)
		e2v_others_ndcg = e.average_ndcg(e2v_others_scores)
		e2v_kinship_MAP = e.MAP(e2v_kinship_scores)
		e2v_romantic_MAP = e.MAP(e2v_romantic_scores)
		e2v_friendship_MAP = e.MAP(e2v_friendship_scores)
		e2v_teacher_student_MAP = e.MAP(e2v_teacher_student_scores)
		e2v_business_MAP = e.MAP(e2v_business_scores)
		e2v_others_MAP = e.MAP(e2v_others_scores)
		plt.title("Evaluate Different Relationship Performance NDCG@k")
		plt.xlabel("Top K Recommendation")
		plt.ylabel("NDCG@k")
		plt.plot(range(1, 6), e2v_kinship_ndcg, "-v", color = 'y', label = "kinship")
		plt.plot(range(1, 6), e2v_romantic_ndcg, "-v", color = 'm', label = "romantic relationship")
		plt.plot(range(1, 6), e2v_friendship_ndcg, "-v", color = 'g', label = "friendship")
		plt.plot(range(1, 6), e2v_teacher_student_ndcg, "-v", color = 'b', label = "teacher student relationship")
		plt.plot(range(1, 6), e2v_business_ndcg, "-v", color = 'c', label = "business relationship")
		plt.plot(range(1, 6), e2v_others_ndcg, "-v", color = 'k', label = "others")
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/Relationship_NDCG.png')
		plt.close()
		plt.title("Evaluate Different Relationship Performance MAP@k")
		plt.xlabel("Top K Recommendation")
		plt.ylabel("MAP@k")
		plt.plot(range(1, 6), e2v_kinship_MAP, "-v", color = 'y', label = "kinship")
		plt.plot(range(1, 6), e2v_romantic_MAP, "-v", color = 'm', label = "romantic relationship")
		plt.plot(range(1, 6), e2v_friendship_MAP, "-v", color = 'g', label = "friendship")
		plt.plot(range(1, 6), e2v_teacher_student_MAP, "-v", color = 'b', label = "teacher student relationship")
		plt.plot(range(1, 6), e2v_business_MAP, "-v", color = 'c', label = "business relationship")
		plt.plot(range(1, 6), e2v_others_MAP, "-v", color = 'k', label = "others")
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/Relationship_MAP.png')
		plt.close()
	# whole evaluation
	def whole_evaluation(self):
		e = Evaluation()
		sql = "SELECT score1, score2, score3, score4, score5 From experiment_system_user Where system_type = 1"
		self.cursor.execute(sql)
		w2v_score = []
		w2v_scores = []
		scores_list = self.cursor.fetchall()
		for score_list in scores_list:
			w2v_score.append(score_list[0])
			w2v_score.append(score_list[1])
			w2v_score.append(score_list[2])
			w2v_score.append(score_list[3])
			w2v_score.append(score_list[4])
			w2v_scores.append(w2v_score)
			w2v_score = []
		sql = "SELECT score1, score2, score3, score4, score5 From experiment_system_user Where system_type = 2"
		self.cursor.execute(sql)
		rstr_score = []
		rstr_scores = []
		scores_list = self.cursor.fetchall()
		for score_list in scores_list:
			rstr_score.append(score_list[0])
			rstr_score.append(score_list[1])
			rstr_score.append(score_list[2])
			rstr_score.append(score_list[3])
			rstr_score.append(score_list[4])
			rstr_scores.append(rstr_score)
			rstr_score = []
		print(w2v_scores)
		print(rstr_scores)
		w2v_ndcg = e.average_ndcg(w2v_scores)
		w2v_MAP = e.MAP(w2v_scores)
		rstr_ndcg = e.average_ndcg(rstr_scores)
		rstr_MAP = e.MAP(rstr_scores)
		print("\nNDCG:")
		print(w2v_ndcg)
		print(rstr_ndcg)
		plt.title("Evaluate System Performance NDCG@k")
		plt.xlabel("Top K Recommendation")
		plt.ylabel("NDCG@k")
		plt.plot(range(1, 6), w2v_ndcg, "-v", color = 'y', label = "W2V")
		plt.plot(range(1, 6), rstr_ndcg, "-v", color = 'm', label = "RSTR")
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/System_NDCG.png')
		plt.close()
		print("\nMAP:")
		print(w2v_MAP)
		print(rstr_MAP)
		plt.title("Evaluate System Performance MAP@k")
		plt.xlabel("Top K Recommendation")
		plt.ylabel("MAP@k")
		plt.plot(range(1, 6), w2v_MAP, "-v", color = 'y', label = "W2V")
		plt.plot(range(1, 6), rstr_MAP, "-v", color = 'm', label = "RSTR")
		plt.legend(loc = "best")
		# save image
		plt.savefig('image/System_MAP.png')
		plt.close()
if __name__ == "__main__":
	seu = SystemEvaluationUser()
	seu.system_evaluation_user()
