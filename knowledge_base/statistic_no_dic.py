import MySQLdb

# 針對 articles_ner 資料表進行 character_object, time, location 以及 emotion, event 的統計數據
class Statistic():
	# Initialize
	def __init__(self):
		self.db = MySQLdb.connect(host = "localhost", user = "root", passwd = "wmmkscsie", db = "recommender_system", charset = "utf8")
		self.cursor = self.db.cursor()
		self.character_object = {}
		self.time = {}
		self.location = {}
		self.emotion = {}
		self.event = {}
		self.storyline_event = {}
	# 主要做分類統計
	def main(self):
		# articles
		self.cursor.execute("SELECT id FROM articles Where id >= 1")
		articles = self.cursor.fetchall()
		for article in articles:
			article_id = article[0]
			print("id:" + str(article_id))
			try:
				self.article_statistic(article_id)
			except:
				print("An exception occurred")
		self.character_object = sorted(self.character_object.items(), key = lambda x:x[1], reverse = True)
		self.time = sorted(self.time.items(), key = lambda x:x[1], reverse = True)
		self.location = sorted(self.location.items(), key = lambda x:x[1], reverse = True)
		self.emotion = sorted(self.emotion.items(), key = lambda x:x[1], reverse = True)
		self.event = sorted(self.event.items(), key = lambda x:x[1], reverse = True)
		# movies
		self.cursor.execute("SELECT id FROM movies Where id >= 1")
		movies = self.cursor.fetchall()
		for movie in movies:
			movie_id = movie[0]
			print("id:" + str(movie_id))
			try:
				self.movie_statistic(movie_id)
			except:
				print("An exception occurred")
		self.storyline_event = sorted(self.storyline_event.items(), key = lambda x:x[1], reverse = True)

	# 進行 article character_object, time, location 以及 emotion, event 的統計
	def article_statistic(self, id):
		self.cursor.execute("SELECT person_object, time, location, emotion, event FROM articles_ner Where id = '" + str(id) + "'")
		entitys = self.cursor.fetchone()
		po = entitys[0]
		ti = entitys[1]
		lo = entitys[2]
		em = entitys[3]
		ev = entitys[4]
		for p in po.split(' '):
			if p != '':
				if p not in self.character_object.keys():
					self.character_object[p] = 1
				else :
					self.character_object[p] = self.character_object[p] + 1
		for t in ti.split(' '):
			if t != '':
				if t not in self.time.keys():
					self.time[t] = 1
				else :
					self.time[t] = self.time[t] + 1
		for l in lo.split(' '):
			if l != '':
				if l not in self.location.keys():
					self.location[l] = 1
				else :
					self.location[l] = self.location[l] + 1
		for e in em.split(' '):
			if e != '':
				if e not in self.emotion.keys():
					self.emotion[e] = 1
				else :
					self.emotion[e] = self.emotion[e] + 1
		for e in ev.split(' '):
			if e != '':
				if e not in self.event.keys():
					self.event[e] = 1
				else :
					self.event[e] = self.event[e] + 1
	# 進行 movie event 的統計
	def movie_statistic(self, id):
		self.cursor.execute("SELECT event FROM movies_ner Where id = '" + str(id) + "'")
		entitys = self.cursor.fetchone()
		ev = entitys[0]
		for e in ev.split(' '):
			if e != '':
				if e not in self.storyline_event.keys():
					self.storyline_event[e] = 1
				else :
					self.storyline_event[e] = self.storyline_event[e] + 1

	def produce_dictionary(self):
		'''with open("dict_observation/character_object.txt", "w", encoding='UTF-8') as character_object_file:
			for co in self.character_object:
				try:
					character_object_file.write(co[0])
					character_object_file.write('\n')
				except:
					print("An exception occurred")'''
		with open("dict_observation/time.txt", "w", encoding='UTF-8') as time_file:
			for ti in self.time:
				try:
					time_file.write(ti[0])
					time_file.write('\n')
				except:
					print("An exception occurred")
		with open("dict_observation/location.txt", "w", encoding='UTF-8') as location_file:
			for lo in self.location:
				try:
					location_file.write(lo[0])
					location_file.write('\n')
				except:
					print("An exception occurred")	
		'''with open("dict_observation/emotion.txt", "w", encoding='UTF-8') as emotion_file:
			for em in self.emotion:
				try:
					emotion_file.write(em[0])
					emotion_file.write('\n')
				except:
					print("An exception occurred")	'''
		with open("dict_observation/event.txt", "w", encoding='UTF-8') as event_file:
			for ev in self.event:
				try:
					event_file.write(ev[0])
					event_file.write('\n')
				except:
					print("An exception occurred")
		# storyline event	
		with open("dict_observation/storyline_event.txt", "w", encoding='UTF-8') as event_file:
			for ev in self.storyline_event:
				try:
					event_file.write(ev[0])
					event_file.write('\n')
				except:
					print("An exception occurred")		
if __name__ == '__main__':
	statistic = Statistic()
	statistic.main()
	print("character_object:")
	print(statistic.character_object, end = "\n\n")
	print("time:")
	print(statistic.time, end = "\n\n")
	print("location:")
	print(statistic.location, end = "\n\n")
	print("emotion:")
	print(statistic.emotion, end = "\n\n")
	print("event:")
	print(statistic.event, end = "\n\n")
	print("storyline event:")
	print(statistic.storyline_event, end = "\n\n")
	statistic.produce_dictionary()