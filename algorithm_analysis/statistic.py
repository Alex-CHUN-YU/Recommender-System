import MySQLdb

# 針對 movies_ner 資料表進行 emotion 和 event 的統計數據
class Statistic():
	# Initialize
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.kinship_filial_emotion_event_dic = {}
		self.kinship_love_emotion_event_dic = {}
		self.kinship_betray_emotion_event_dic = {}
		self.romantic_relationship_in_love_emotion_event_dic = {}
		self.romantic_relationship_lost_love_emotion_event_dic = {}
		self.romantic_relationship_sex_emotion_event_dic = {}
		self.friendship_support_emotion_event_dic = {}
		self.friendship_betray_emotion_event_dic = {}
		self.friendship_memory_emotion_event_dic = {}	
		self.teacher_student_relationship_learning_emotion_event_dic = {}	
		self.business_relationship_competition_emotion_event_dic = {}
		self.business_relationship_task_emotion_event_dic = {}
		self.business_relationship_betray_emotion_event_dic = {}
		self.business_relationship_reveal_emotion_event_dic = {}	
		self.other_pursuit_of_self_emotion_event_dic = {}	
		self.other_others_emotion_event_dic = {}
	# 主要做分類統計
	def main(self):
		self.cursor.execute("SELECT id, relationship_type, scenario_type FROM movies Where id >= 1 and id < 286 and relationship_type !=''")
		movies = self.cursor.fetchall()
		for movie in movies:
			movies_id = movie[0]
			print("id:" + str(movies_id))
			relationship_type = movie[1]
			relationship_type_list = relationship_type.split(',')
			print("relationship_type:" + relationship_type)
			scenario_type = movie[2]
			scenario_type_list = scenario_type.split(',')
			print("scenario_type:" + scenario_type)
			for idx, rt in enumerate(relationship_type_list):
				if rt == '1':
					if scenario_type_list[idx] == '1':
						self.kinship_filial_emotion_event_dic = self.statisitic(movies_id, self.kinship_filial_emotion_event_dic)
					elif scenario_type_list[idx] == '2':
						self.kinship_love_emotion_event_dic = self.statisitic(movies_id, self.kinship_love_emotion_event_dic)
					elif scenario_type_list[idx] == '3':
						self.kinship_betray_emotion_event_dic = self.statisitic(movies_id, self.kinship_betray_emotion_event_dic)
				elif rt == '2':
					if scenario_type_list[idx] == '1':
						self.romantic_relationship_in_love_emotion_event_dic = self.statisitic(movies_id, self.romantic_relationship_in_love_emotion_event_dic)
					elif scenario_type_list[idx] == '2':
						self.romantic_relationship_lost_love_emotion_event_dic = self.statisitic(movies_id, self.romantic_relationship_lost_love_emotion_event_dic)
					elif scenario_type_list[idx] == '3':
						self.romantic_relationship_sex_emotion_event_dic = self.statisitic(movies_id, self.romantic_relationship_sex_emotion_event_dic)
				elif rt == '3':
					if scenario_type_list[idx] == '1':
						self.friendship_support_emotion_event_dic = self.statisitic(movies_id, self.friendship_support_emotion_event_dic)
					elif scenario_type_list[idx] == '2':
						self.friendship_betray_emotion_event_dic = self.statisitic(movies_id, self.friendship_betray_emotion_event_dic)
					elif scenario_type_list[idx] == '3':
						self.friendship_memory_emotion_event_dic = self.statisitic(movies_id, self.friendship_memory_emotion_event_dic)
				elif rt == '4':
					if scenario_type_list[idx] == '1':
						self.teacher_student_relationship_learning_emotion_event_dic = self.statisitic(movies_id, self.teacher_student_relationship_learning_emotion_event_dic)
				elif rt == '5':
					if scenario_type_list[idx] == '1':
						self.business_relationship_competition_emotion_event_dic = self.statisitic(movies_id, self.business_relationship_competition_emotion_event_dic)
					elif scenario_type_list[idx] == '2':
						self.business_relationship_task_emotion_event_dic = self.statisitic(movies_id, self.business_relationship_task_emotion_event_dic)
					elif scenario_type_list[idx] == '3':
						self.business_relationship_betray_emotion_event_dic = self.statisitic(movies_id, self.business_relationship_betray_emotion_event_dic)
					elif scenario_type_list[idx] == '4':
						self.business_relationship_reveal_emotion_event_dic = self.statisitic(movies_id, self.business_relationship_reveal_emotion_event_dic)
				elif rt == '6':
					if scenario_type_list[idx] == '1':
						self.other_pursuit_of_self_emotion_event_dic = self.statisitic(movies_id, self.other_pursuit_of_self_emotion_event_dic)
					elif scenario_type_list[idx] == '2':
						self.other_others_emotion_event_dic = self.statisitic(movies_id, self.other_others_emotion_event_dic)
		self.kinship_filial_emotion_event_dic = sorted(self.kinship_filial_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_love_emotion_event_dic = sorted(self.kinship_love_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_betray_emotion_event_dic = sorted(self.kinship_betray_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_in_love_emotion_event_dic = sorted(self.romantic_relationship_in_love_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_lost_love_emotion_event_dic = sorted(self.romantic_relationship_lost_love_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_sex_emotion_event_dic = sorted(self.romantic_relationship_sex_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_support_emotion_event_dic = sorted(self.friendship_support_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_betray_emotion_event_dic = sorted(self.friendship_betray_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_memory_emotion_event_dic = sorted(self.friendship_memory_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.teacher_student_relationship_learning_emotion_event_dic = sorted(self.teacher_student_relationship_learning_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_competition_emotion_event_dic = sorted(self.business_relationship_competition_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_task_emotion_event_dic = sorted(self.business_relationship_task_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_betray_emotion_event_dic = sorted(self.business_relationship_betray_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_reveal_emotion_event_dic = sorted(self.business_relationship_reveal_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.other_pursuit_of_self_emotion_event_dic = sorted(self.other_pursuit_of_self_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.other_others_emotion_event_dic = sorted(self.other_others_emotion_event_dic.items(), key = lambda x:x[1], reverse = True)
	# 進行 emotion 和 event 統計
	def statisitic(self, id, statisitic_dic):
		self.cursor.execute("SELECT emotion, event FROM movies_ner Where id = '" + str(id) + "'")
		entitys = self.cursor.fetchone()
		emotions = entitys[0]
		events = entitys[1]
		for emotion in emotions.split(' '):
			if emotion != '':
				if emotion not in statisitic_dic.keys():
					statisitic_dic[emotion] = 1
				else :
					statisitic_dic[emotion] = statisitic_dic[emotion] + 1
		for event in events.split(' '):
			if event != '':
				if event not in statisitic_dic.keys():
					statisitic_dic[event] = 1
				else :
					statisitic_dic[event] = statisitic_dic[event] + 1
		return statisitic_dic

if __name__ == '__main__':
	statisitic = Statistic()
	statisitic.main()
	print("kinship_filial_emotion_event_dic:")
	print(statisitic.kinship_filial_emotion_event_dic, end = "\n\n")
	print("kinship_love_emotion_event_dic:")
	print(statisitic.kinship_love_emotion_event_dic, end = "\n\n")	
	print("kinship_betray_emotion_event_dic:")
	print(statisitic.kinship_betray_emotion_event_dic, end = "\n\n")
	print("romantic_relationship_in_love_emotion_event_dic:")
	print(statisitic.romantic_relationship_in_love_emotion_event_dic, end = "\n\n")
	print("romantic_relationship_lost_love_emotion_event_dic:")
	print(statisitic.romantic_relationship_lost_love_emotion_event_dic, end = "\n\n")
	print("romantic_relationship_sex_emotion_event_dic:")
	print(statisitic.romantic_relationship_sex_emotion_event_dic, end = "\n\n")
	print("friendship_support_emotion_event_dic:")
	print(statisitic.friendship_support_emotion_event_dic, end = "\n\n")
	print("friendship_betray_emotion_event_dic:")
	print(statisitic.friendship_betray_emotion_event_dic, end = "\n\n")
	print("friendship_memory_emotion_event_dic:")
	print(statisitic.friendship_memory_emotion_event_dic, end = "\n\n")
	print("teacher_student_relationship_learning_emotion_event_dic:")
	print(statisitic.teacher_student_relationship_learning_emotion_event_dic, end = "\n\n")
	print("business_relationship_competition_emotion_event_dic:")
	print(statisitic.business_relationship_competition_emotion_event_dic, end = "\n\n")
	print("business_relationship_task_emotion_event_dic:")
	print(statisitic.business_relationship_task_emotion_event_dic, end = "\n\n")
	print("business_relationship_betray_emotion_event_dic:")
	print(statisitic.business_relationship_betray_emotion_event_dic, end = "\n\n")
	print("business_relationship_reveal_emotion_event_dic:")
	print(statisitic.business_relationship_reveal_emotion_event_dic, end = "\n\n")
	print("other_pursuit_of_self_emotion_event_dic:")
	print(statisitic.other_pursuit_of_self_emotion_event_dic, end = "\n\n")
	print("other_others_emotion_event_dic:")
	print(statisitic.other_others_emotion_event_dic, end = "\n\n")