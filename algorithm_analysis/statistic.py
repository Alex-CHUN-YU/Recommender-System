import MySQLdb

# 針對 movies_ner 資料表進行 emotion 和 event 的統計數據, 並透過 article 的 emotion 和 event 做過濾
class Statistic():
	# Initialize
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		with open("dict_observation/emotion.txt", 'r', encoding='UTF-8') as fp:
			self.emotions = fp.readlines()
			self.emotions = [emotion.strip('\n') for emotion in self.emotions]
		with open("dict_observation/event.txt", 'r', encoding='UTF-8') as fp:
			self.events = fp.readlines()
			self.events = [event.strip('\n') for event in self.events]
		with open("dict_observation/filter_term.txt", 'r', encoding='UTF-8') as fp:
			self.filter_term = fp.readlines()
			self.filter_term = [term.strip('\n') for term in self.filter_term]
		self.kinship_filial_emotion_dic = {}
		self.kinship_filial_event_dic = {}
		self.kinship_love_emotion_dic = {}
		self.kinship_love_event_dic = {}
		self.kinship_betray_emotion_dic = {}
		self.kinship_betray_event_dic = {}

		self.romantic_relationship_in_love_emotion_dic = {}
		self.romantic_relationship_in_love_event_dic = {}
		self.romantic_relationship_lost_love_emotion_dic = {}
		self.romantic_relationship_lost_love_event_dic = {}
		self.romantic_relationship_sex_emotion_dic = {}
		self.romantic_relationship_sex_event_dic = {}

		self.friendship_support_emotion_dic = {}
		self.friendship_support_event_dic = {}
		self.friendship_betray_emotion_dic = {}
		self.friendship_betray_event_dic = {}
		self.friendship_memory_emotion_dic = {}	
		self.friendship_memory_event_dic = {}

		self.teacher_student_relationship_learning_emotion_dic = {}	
		self.teacher_student_relationship_learning_event_dic = {}	

		self.business_relationship_competition_emotion_dic = {}
		self.business_relationship_competition_event_dic = {}
		self.business_relationship_task_emotion_dic = {}
		self.business_relationship_task_event_dic = {}
		self.business_relationship_betray_emotion_dic = {}
		self.business_relationship_betray_event_dic = {}
		self.business_relationship_reveal_emotion_dic = {}	
		self.business_relationship_reveal_event_dic = {}

		self.other_pursuit_of_self_emotion_dic = {}
		self.other_pursuit_of_self_event_dic = {}		
		self.other_others_emotion_dic = {}
		self.other_others_event_dic = {}
	# 主要做分類統計
	def main(self):
		self.cursor.execute("SELECT id, relationship_type, scenario_type FROM movies Where id >= 1 and id < 551 and relationship_type !=''")
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
						self.kinship_filial_emotion_dic = self.statistic(movies_id, self.kinship_filial_emotion_dic, 'emotion')
						self.kinship_filial_event_dic = self.statistic(movies_id, self.kinship_filial_event_dic, 'event')
					elif scenario_type_list[idx] == '2':
						self.kinship_love_emotion_dic = self.statistic(movies_id, self.kinship_love_emotion_dic, 'emotion')
						self.kinship_love_event_dic = self.statistic(movies_id, self.kinship_love_event_dic, 'event')
					elif scenario_type_list[idx] == '3':
						self.kinship_betray_emotion_dic = self.statistic(movies_id, self.kinship_betray_emotion_dic, 'emotion')
						self.kinship_betray_event_dic = self.statistic(movies_id, self.kinship_betray_event_dic, 'event')
				elif rt == '2':
					if scenario_type_list[idx] == '1':
						self.romantic_relationship_in_love_emotion_dic = self.statistic(movies_id, self.romantic_relationship_in_love_emotion_dic, 'emotion')
						self.romantic_relationship_in_love_event_dic = self.statistic(movies_id, self.romantic_relationship_in_love_event_dic, 'event')
					elif scenario_type_list[idx] == '2':
						self.romantic_relationship_lost_love_emotion_dic = self.statistic(movies_id, self.romantic_relationship_lost_love_emotion_dic, 'emotion')
						self.romantic_relationship_lost_love_event_dic = self.statistic(movies_id, self.romantic_relationship_lost_love_event_dic, 'event')
					elif scenario_type_list[idx] == '3':
						self.romantic_relationship_sex_emotion_dic = self.statistic(movies_id, self.romantic_relationship_sex_emotion_dic, 'emotion')
						self.romantic_relationship_sex_event_dic = self.statistic(movies_id, self.romantic_relationship_sex_event_dic, 'event')
				elif rt == '3':
					if scenario_type_list[idx] == '1':
						self.friendship_support_emotion_dic = self.statistic(movies_id, self.friendship_support_emotion_dic, 'emotion')
						self.friendship_support_event_dic = self.statistic(movies_id, self.friendship_support_event_dic, 'event')
					elif scenario_type_list[idx] == '2':
						self.friendship_betray_emotion_dic = self.statistic(movies_id, self.friendship_betray_emotion_dic, 'emotion')
						self.friendship_betray_event_dic = self.statistic(movies_id, self.friendship_betray_event_dic, 'event')
					elif scenario_type_list[idx] == '3':
						self.friendship_memory_emotion_dic = self.statistic(movies_id, self.friendship_memory_emotion_dic, 'emotion')
						self.friendship_memory_event_dic = self.statistic(movies_id, self.friendship_memory_event_dic, 'event')
				elif rt == '4':
					if scenario_type_list[idx] == '1':
						self.teacher_student_relationship_learning_emotion_dic = self.statistic(movies_id, self.teacher_student_relationship_learning_emotion_dic, 'emotion')
						self.teacher_student_relationship_learning_event_dic = self.statistic(movies_id, self.teacher_student_relationship_learning_event_dic, 'event')
				elif rt == '5':
					if scenario_type_list[idx] == '1':
						self.business_relationship_competition_emotion_dic = self.statistic(movies_id, self.business_relationship_competition_emotion_dic, 'emotion')
						self.business_relationship_competition_event_dic = self.statistic(movies_id, self.business_relationship_competition_event_dic, 'event')
					elif scenario_type_list[idx] == '2':
						self.business_relationship_task_emotion_dic = self.statistic(movies_id, self.business_relationship_task_emotion_dic, 'emotion')
						self.business_relationship_task_event_dic = self.statistic(movies_id, self.business_relationship_task_event_dic, 'event')
					elif scenario_type_list[idx] == '3':
						self.business_relationship_betray_emotion_dic = self.statistic(movies_id, self.business_relationship_betray_emotion_dic, 'emotion')
						self.business_relationship_betray_event_dic = self.statistic(movies_id, self.business_relationship_betray_event_dic, 'event')
					elif scenario_type_list[idx] == '4':
						self.business_relationship_reveal_emotion_dic = self.statistic(movies_id, self.business_relationship_reveal_emotion_dic, 'emotion')
						self.business_relationship_reveal_event_dic = self.statistic(movies_id, self.business_relationship_reveal_event_dic, 'event')
				elif rt == '6':
					if scenario_type_list[idx] == '1':
						self.other_pursuit_of_self_emotion_dic = self.statistic(movies_id, self.other_pursuit_of_self_emotion_dic, 'emotion')
						self.other_pursuit_of_self_event_dic = self.statistic(movies_id, self.other_pursuit_of_self_event_dic, 'event')
					elif scenario_type_list[idx] == '2':
						self.other_others_emotion_dic = self.statistic(movies_id, self.other_others_emotion_dic, 'emotion')
						self.other_others_event_dic = self.statistic(movies_id, self.other_others_event_dic, 'event')
		self.kinship_filial_emotion_dic = sorted(self.kinship_filial_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_filial_event_dic = sorted(self.kinship_filial_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_love_emotion_dic = sorted(self.kinship_love_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_love_event_dic = sorted(self.kinship_love_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_betray_emotion_dic = sorted(self.kinship_betray_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.kinship_betray_event_dic = sorted(self.kinship_betray_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.kinship_filial_emotion_dic, "kinship_filial_emotion_dic")
		self.produce_dictionary(self.kinship_filial_event_dic, "kinship_filial_event_dic")
		self.produce_dictionary(self.kinship_love_emotion_dic, "kinship_love_emotion_dic")
		self.produce_dictionary(self.kinship_love_event_dic, "kinship_love_event_dic")
		self.produce_dictionary(self.kinship_betray_emotion_dic, "kinship_betray_emotion_dic")
		self.produce_dictionary(self.kinship_betray_event_dic, "kinship_betray_event_dic")

		self.romantic_relationship_in_love_emotion_dic = sorted(self.romantic_relationship_in_love_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_in_love_event_dic = sorted(self.romantic_relationship_in_love_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_lost_love_emotion_dic = sorted(self.romantic_relationship_lost_love_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_lost_love_event_dic = sorted(self.romantic_relationship_lost_love_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_sex_emotion_dic = sorted(self.romantic_relationship_sex_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.romantic_relationship_sex_event_dic = sorted(self.romantic_relationship_sex_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.romantic_relationship_in_love_emotion_dic, "romantic_relationship_in_love_emotion_dic")
		self.produce_dictionary(self.romantic_relationship_in_love_event_dic, "romantic_relationship_in_love_event_dic")
		self.produce_dictionary(self.romantic_relationship_lost_love_emotion_dic, "romantic_relationship_lost_love_emotion_dic")
		self.produce_dictionary(self.romantic_relationship_lost_love_event_dic, "romantic_relationship_lost_love_event_dic")
		self.produce_dictionary(self.romantic_relationship_sex_emotion_dic, "romantic_relationship_sex_emotion_dic")
		self.produce_dictionary(self.romantic_relationship_sex_event_dic, "romantic_relationship_sex_event_dic")

		self.friendship_support_emotion_dic = sorted(self.friendship_support_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_support_event_dic = sorted(self.friendship_support_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_betray_emotion_dic = sorted(self.friendship_betray_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_betray_event_dic = sorted(self.friendship_betray_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_memory_emotion_dic = sorted(self.friendship_memory_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.friendship_memory_event_dic = sorted(self.friendship_memory_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.friendship_support_emotion_dic, "friendship_support_emotion_dic")
		self.produce_dictionary(self.friendship_support_event_dic, "friendship_support_event_dic")
		self.produce_dictionary(self.friendship_betray_emotion_dic, "friendship_betray_emotion_dic")
		self.produce_dictionary(self.friendship_betray_event_dic, "friendship_betray_event_dic")
		self.produce_dictionary(self.friendship_memory_emotion_dic, "friendship_memory_emotion_dic")
		self.produce_dictionary(self.friendship_memory_event_dic, "friendship_memory_event_dic")

		self.teacher_student_relationship_learning_emotion_dic = sorted(self.teacher_student_relationship_learning_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.teacher_student_relationship_learning_event_dic = sorted(self.teacher_student_relationship_learning_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.teacher_student_relationship_learning_emotion_dic, "teacher_student_relationship_learning_emotion_dic")
		self.produce_dictionary(self.teacher_student_relationship_learning_event_dic, "teacher_student_relationship_learning_event_dic")

		self.business_relationship_competition_emotion_dic = sorted(self.business_relationship_competition_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_competition_event_dic = sorted(self.business_relationship_competition_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_task_emotion_dic = sorted(self.business_relationship_task_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_task_event_dic = sorted(self.business_relationship_task_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_betray_emotion_dic = sorted(self.business_relationship_betray_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_betray_event_dic = sorted(self.business_relationship_betray_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_reveal_emotion_dic = sorted(self.business_relationship_reveal_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.business_relationship_reveal_event_dic = sorted(self.business_relationship_reveal_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.business_relationship_competition_emotion_dic, "business_relationship_competition_emotion_dic")
		self.produce_dictionary(self.business_relationship_competition_event_dic, "business_relationship_competition_event_dic")
		self.produce_dictionary(self.business_relationship_task_emotion_dic, "business_relationship_task_emotion_dic")
		self.produce_dictionary(self.business_relationship_task_event_dic, "business_relationship_task_event_dic")
		self.produce_dictionary(self.business_relationship_betray_emotion_dic, "business_relationship_betray_emotion_dic")
		self.produce_dictionary(self.business_relationship_betray_event_dic, "business_relationship_betray_event_dic")
		self.produce_dictionary(self.business_relationship_reveal_emotion_dic, "business_relationship_reveal_emotion_dic")
		self.produce_dictionary(self.business_relationship_reveal_event_dic, "business_relationship_reveal_event_dic")

		self.other_pursuit_of_self_emotion_dic = sorted(self.other_pursuit_of_self_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.other_pursuit_of_self_event_dic = sorted(self.other_pursuit_of_self_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.other_others_emotion_dic = sorted(self.other_others_emotion_dic.items(), key = lambda x:x[1], reverse = True)
		self.other_others_event_dic = sorted(self.other_others_event_dic.items(), key = lambda x:x[1], reverse = True)
		self.produce_dictionary(self.other_pursuit_of_self_emotion_dic, "other_pursuit_of_self_emotion_dic")
		self.produce_dictionary(self.other_pursuit_of_self_event_dic, "other_pursuit_of_self_event_dic")
		self.produce_dictionary(self.other_others_emotion_dic, "other_others_emotion_dic")
		self.produce_dictionary(self.other_others_event_dic, "other_others_event_dic")

		# 代表 all emotions
		aaaa = dict(self.kinship_filial_emotion_dic)
		aaaa.update(dict(self.kinship_love_emotion_dic))
		aaaa.update(dict(self.kinship_betray_emotion_dic))
		aaaa.update(dict(self.romantic_relationship_in_love_emotion_dic))
		aaaa.update(dict(self.romantic_relationship_lost_love_emotion_dic))
		aaaa.update(dict(self.romantic_relationship_sex_emotion_dic))
		aaaa.update(dict(self.friendship_support_emotion_dic))
		aaaa.update(dict(self.friendship_betray_emotion_dic))
		aaaa.update(dict(self.friendship_memory_emotion_dic))
		aaaa.update(dict(self.teacher_student_relationship_learning_emotion_dic))
		aaaa.update(dict(self.business_relationship_competition_emotion_dic))
		aaaa.update(dict(self.business_relationship_task_emotion_dic))
		aaaa.update(dict(self.business_relationship_betray_emotion_dic))
		aaaa.update(dict(self.business_relationship_reveal_emotion_dic))
		aaaa.update(dict(self.other_pursuit_of_self_emotion_dic))
		aaaa.update(dict(self.other_others_emotion_dic))
		self.produce_dictionary(aaaa, "aaaa")
		# 代表 all events
		bbbb = dict(self.kinship_filial_event_dic)
		bbbb.update(dict(self.kinship_love_event_dic))
		bbbb.update(dict(self.kinship_betray_event_dic))
		bbbb.update(dict(self.romantic_relationship_in_love_event_dic))
		bbbb.update(dict(self.romantic_relationship_lost_love_event_dic))
		bbbb.update(dict(self.romantic_relationship_sex_event_dic))
		bbbb.update(dict(self.friendship_support_event_dic))
		bbbb.update(dict(self.friendship_betray_event_dic))
		bbbb.update(dict(self.friendship_memory_event_dic))
		bbbb.update(dict(self.teacher_student_relationship_learning_event_dic))
		bbbb.update(dict(self.business_relationship_competition_event_dic))
		bbbb.update(dict(self.business_relationship_task_event_dic))
		bbbb.update(dict(self.business_relationship_betray_event_dic))
		bbbb.update(dict(self.business_relationship_reveal_event_dic))
		bbbb.update(dict(self.other_pursuit_of_self_event_dic))
		bbbb.update(dict(self.other_others_event_dic))
		self.produce_dictionary(bbbb, "bbbb")
	# 進行 emotion 和 event 統計
	def statistic(self, id, statistic_dic, feature):
		if feature == 'emotion':
			self.cursor.execute("SELECT emotion FROM movies_ner Where id = '" + str(id) + "'")
		elif feature == 'event':
			self.cursor.execute("SELECT event FROM movies_ner Where id = '" + str(id) + "'")
		entitys = self.cursor.fetchone()
		entitys = entitys[0]
		for entity in entitys.split(' '):
			if entity != '':
				if entity not in statistic_dic.keys():
					statistic_dic[entity] = 1
				else :
					statistic_dic[entity] = statistic_dic[entity] + 1
		return statistic_dic
	# 產生辭典
	def produce_dictionary(self, statistic_dic, name):
		with open("dict_observation/" + name + ".txt", "w", encoding='UTF-8') as file:
			for statistic in statistic_dic:
				try:
					if 'emotion' in name:
						if statistic[0] in self.emotions:
							file.write(statistic[0])
							file.write('\n')
					elif 'event' in name:
						if statistic[0] in self.events:
							file.write(statistic[0])
							file.write('\n')
					elif 'aaaa' in name:
						if statistic in self.emotions and statistic not in self.filter_term:
							file.write(statistic)
							file.write('\n')
					elif 'bbbb' in name:
						if statistic in self.events and statistic not in self.filter_term:
							file.write(statistic)
							file.write('\n')
				except:
					print("An exception occurred")
if __name__ == '__main__':
	statistic = Statistic()
	statistic.main()
	# print("kinship_filial_emotion_event_dic:")
	# print(statistic.kinship_filial_emotion_event_dic, end = "\n\n")
	# print("kinship_love_emotion_event_dic:")
	# print(statistic.kinship_love_emotion_event_dic, end = "\n\n")	
	# print("kinship_betray_emotion_event_dic:")
	# print(statistic.kinship_betray_emotion_event_dic, end = "\n\n")
	# print("romantic_relationship_in_love_emotion_event_dic:")
	# print(statistic.romantic_relationship_in_love_emotion_event_dic, end = "\n\n")
	# print("romantic_relationship_lost_love_emotion_event_dic:")
	# print(statistic.romantic_relationship_lost_love_emotion_event_dic, end = "\n\n")
	# print("romantic_relationship_sex_emotion_event_dic:")
	# print(statistic.romantic_relationship_sex_emotion_event_dic, end = "\n\n")
	# print("friendship_support_emotion_event_dic:")
	# print(statistic.friendship_support_emotion_event_dic, end = "\n\n")
	# print("friendship_betray_emotion_event_dic:")
	# print(statistic.friendship_betray_emotion_event_dic, end = "\n\n")
	# print("friendship_memory_emotion_event_dic:")
	# print(statistic.friendship_memory_emotion_event_dic, end = "\n\n")
	# print("teacher_student_relationship_learning_emotion_event_dic:")
	# print(statistic.teacher_student_relationship_learning_emotion_event_dic, end = "\n\n")
	# print("business_relationship_competition_emotion_event_dic:")
	# print(statistic.business_relationship_competition_emotion_event_dic, end = "\n\n")
	# print("business_relationship_task_emotion_event_dic:")
	# print(statistic.business_relationship_task_emotion_event_dic, end = "\n\n")
	# print("business_relationship_betray_emotion_event_dic:")
	# print(statistic.business_relationship_betray_emotion_event_dic, end = "\n\n")
	# print("business_relationship_reveal_emotion_event_dic:")
	# print(statistic.business_relationship_reveal_emotion_event_dic, end = "\n\n")
	# print("other_pursuit_of_self_emotion_event_dic:")
	# print(statistic.other_pursuit_of_self_emotion_event_dic, end = "\n\n")
	# print("other_others_emotion_event_dic:")
	# print(statistic.other_others_emotion_event_dic, end = "\n\n")